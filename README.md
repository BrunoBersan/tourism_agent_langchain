
# Tourism Agent App

Esta aplicação é um agente inteligente de turismo que cria itinerários detalhados com base em solicitações dos usuários e os converte em coordenadas geográficas, exibindo-os em um mapa interativo.

## Funcionalidades

- Geração automática de itinerários com base na sua solicitação em linguagem natural.
- Conversão do itinerário em coordenadas geográficas (latitude/longitude).
- Visualização interativa das localizações em um mapa usando Streamlit e Folium.
- Suporte a múltiplos dias e rotas detalhadas, incluindo transporte.
- Integração com a API OpenAI via Langchain para processamento inteligente de linguagem.

## Como funciona

O sistema utiliza dois modelos LLM da OpenAI com o Langchain:

1. **Agente de Viagem (`TravelTemplate`)**: Constrói um itinerário com base na sua solicitação.
2. **Conversor de Coordenadas (`MappingTemplate`)**: Extrai os endereços do itinerário e converte em coordenadas geográficas.

O fluxo é:

- Usuário insere sua solicitação em linguagem natural.
- O `TravelTemplate` gera um itinerário detalhado, respeitando preferências e tempo disponível.
- O `MappingTemplate` converte esse itinerário em dados estruturados com latitude, longitude e nomes.
- O resultado é exibido em um mapa interativo com marcadores.

## Tecnologias utilizadas

- **Python 3.8+**
- **Streamlit**: Framework para construir a interface web interativa.
- **Folium**: Biblioteca para renderizar mapas Leaflet no Python.
- **Langchain**: Para construção e encadeamento dos prompts e chamadas ao modelo da OpenAI.
- **OpenAI API**: GPT-4-turbo para processamento e geração dos itinerários e coordenadas.
- **Dotenv**: Para gerenciamento de variáveis de ambiente (chave da API).

## Pré-requisitos

- Conta ativa na OpenAI e chave API válida.
- Python 3.8 ou superior instalado.
- Acesso à internet para chamadas à API OpenAI.

## Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/tourism-agent-app.git
cd tourism-agent-app
```

### 2. Crie e ative o ambiente virtual

Linux/macOS:
```bash
python -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave da OpenAI

Crie um arquivo `.env` na raiz do projeto com o conteúdo:

```
OPENAI_API_KEY=sua-chave-aqui
```

### 5. Execute a aplicação

```bash
streamlit run app.py
```

Abra o navegador no endereço mostrado pelo Streamlit (normalmente http://localhost:8501).

## Estrutura do projeto

```
tourism-agent-app/
│
├── agent.py          # Código dos templates e do agente que chama a API OpenAI
├── app.py            # Interface Streamlit e lógica da aplicação
├── requirements.txt  # Dependências do projeto
├── .env              # Arquivo com a variável de ambiente OPENAI_API_KEY (não versionado)
└── README.md         # Este arquivo de documentação
```

## Detalhes da implementação

- **agent.py**: Define os prompts para o modelo LLM (templates de viagem e de conversão de itinerário para coordenadas) usando Langchain, além da classe Agent que encapsula as chamadas sequenciais ao LLM.
- **app.py**: Usa Streamlit para receber entrada do usuário, aciona o agente para gerar itinerário e coordenadas, e exibe o resultado em um mapa com Folium.
- O mapa exibe marcadores para cada ponto do itinerário, agrupados por dias.

## Logs e debug

- O projeto utiliza logging básico configurado para nível DEBUG para facilitar o diagnóstico de erros e análise do fluxo.

## Possíveis melhorias futuras

- Suporte a outros idiomas além do português e inglês.
- Cache local dos itinerários para reduzir chamadas à API.
- Adição de transporte multimodal (metrô, ônibus, caminhada) com rotas otimizadas.
- Interface mais rica com filtros e customizações de rotas.
- Suporte a múltiplos usuários e sessões.
- Adição de avaliações e recomendações baseadas em reviews públicos.
- Uso de API de geocodificação externa para validação das coordenadas geradas.
- Deploy em nuvem com autenticação e dashboard de administração.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.
