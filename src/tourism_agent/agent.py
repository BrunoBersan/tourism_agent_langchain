from langchain.llms import OpenAI

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain

import logging

logging.basicConfig(level=logging.DEBUG)


class TravelTemplate:
    def __init__(self):
        self.system_template = """
        You are a travel agent who helps users make exciting travel plans.

        The user's request will be denoted by four hashtags. Convert the
        user's request into a detailed itinerary describing the places
        they should visit and the things they should do.

        Try to include the specific address of each location.

        Remember to take the user's preferences and timeframe into account,
        and give them an itinerary that would be fun and doable given their constraints.

        Return the itinerary as a bulleted list with clear start and end locations.
        Be sure to mention the type of transit for the trip.
        If specific start and end locations are not given,
        choose ones that you think are suitable and give specific addresses.
        Your output must be the list and nothing else.
        """

        self.human_template = """
        #### {request}
        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt,
                                                             self.human_message_prompt])
        
        
class MappingTemplate:
    def __init__(self):
        self.system_template = """
        You an agent system who converts detailed travel plans
        into a list of coordinates

        The itinerary will be denoted by four hashtags.
        Convert it into a list containing dictionaries with the latitude,
        longitude, address and name of each location.

        Retrieve a clean JSON object, no markdown notation.

        For example:

        ####
        Itinerary for a 2-day driving trip within London:
        - Day 1:
            - Start at Buckingham Palace (The Mall, London SW1A 1AA)
            - Visit the Tower of London (Tower Hill, London EC3N 4AB)
            - Explore the British Museum (Great Russell St, Bloomsbury, London WC1B 3DG)
            - Enjoy shopping at Oxford Street (Oxford St, London W1C 1JN)
            - End the day at Covent Garden (Covent Garden, London WC2E 8RF)
        - Day 2:
            - Start at Westminster Abbey (20 Deans Yd, Westminster, London SW1P 3PA)
            - Visit the Churchill War Rooms (Clive Steps, King Charles St, London SW1A 2AQ)
            - Explore the Natural History Museum (Cromwell Rd, Kensington, London SW7 5BD)
            - End the trip at the Tower Bridge (Tower Bridge Rd, London SE1 2UP)
        ####
        Output:
        {{
            "days": [
                {{
                "day": 1,
                "locations": [
                        {{"lat": 51.5014, "lon": -0.1419, "address": "The Mall, London SW1A 1AA", "name": "Buckingham Palace"}},
                        {{"lat": 51.5081, "lon": -0.0759, "address": "Tower Hill, London EC3N 4AB", "name": "Tower of London"}},
                        {{"lat": 51.5194, "lon": -0.1270, "address": "Great Russell St, Bloomsbury, London WC1B 3DG", "name": "British Museum"}},
                        {{"lat": 51.5145, "lon": -0.1444, "address": "Oxford St, London W1C 1JN", "name": "Oxford Street"}},
                        {{"lat": 51.5113, "lon": -0.1223, "address": "Covent Garden, London WC2E 8RF", "name": "Covent Garden"}},
                    ]
                }}, {{
                    "day": 2,
                    "locations": [
                        {{"lat": 51.4994, "lon": -0.1272, "address": "20 Deans Yd, Westminster, London SW1P 3PA", "name": "Westminster Abbey"}},
                        {{"lat": 51.5022, "lon": -0.1299, "address": "Clive Steps, King Charles St, London SW1A 2AQ", "name": "Churchill War Rooms"}},
                        {{"lat": 51.4966, "lon": -0.1764, "address": "Cromwell Rd, Kensington, London SW7 5BD", "name": "Natural History Museum"}},
                        {{"lat": 51.5055, "lon": -0.0754, "address": "Tower Bridge Rd, London SE1 2UP", "name": "Tower Bridge"}}
                    ]
                }}
            ]
        }}        
        """
        self.human_template = """
        #### {itinerary}
        """
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.system_template)
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)
        self.chat_prompt = ChatPromptTemplate.from_messages([self.system_message_prompt,
                                                             self.human_message_prompt])
        
class Agent:
    def __init__(self, open_ai_key, model="gpt-4-turbo", temperature=0.1):
        self.open_ai_key = open_ai_key
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatOpenAI(model=self.model,
                                     temperature=self.temperature,
                                     openai_api_key=self.open_ai_key)

    def get_tips(self, request):
        travel_prompt = TravelTemplate()
        coordinates_prompt = MappingTemplate()
        
        parser = LLMChain(
            llm=self.chat_model,
            prompt=travel_prompt.chat_prompt,
            output_key="itinerary"
        )
        coordinates_converter = LLMChain(
            llm=self.chat_model,
            prompt= coordinates_prompt.chat_prompt,
            output_key="coordinates"
        )

        chain = SequentialChain(
            chains=[parser, coordinates_converter],
            input_variables=["request"],
            output_variables=["itinerary", "coordinates"],
            verbose=True
        )
        return chain(
            {"request": request},
            return_only_outputs=True
        )