import yfinance as yf
import pandas as pd
import streamlit as st
import json
from openai import OpenAI

# Inicializa o cliente OpenAI (ou configure sua chave diretamente aqui)
client = OpenAI()  # ou OpenAI(api_key="sua-chave")

# Função que retorna a cotação
def retorna_cotacao(ticker, periodo="1mo"):
    ticker_obj = yf.Ticker(f"{ticker}.SA")
    hist = ticker_obj.history(period=periodo)["Close"]
    hist = round(hist, 2)

    # Garante que o índice é datetime e formata como string
    hist.index = pd.to_datetime(hist.index)
    hist.index = hist.index.strftime("%Y-%m-%d")

    # Limita para no máximo 30 resultados
    if len(hist) > 30:
        slice_size = max(1, len(hist) // 30)
        hist = hist.iloc[::slice_size].iloc[::-1]

    return hist.to_json()

# Ferramenta disponível para o modelo
tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao",
            "description": "Retorna a cotação de ações da Ibovespa",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Ticker da ação (ex: BBAS3, BBDC4)"
                    },
                    "periodo": {
                        "type": "string",
                        "description": "Período histórico da cotação",
                        "enum": ["1d", "5d", "1mo", "6mo", "1y", "5y", "ytd", "max"]
                    }
                },
                "required": ["ticker"]
            }
        }
    }
]

# Mapeamento de funções
funcoes_disponiveis = {"retorna_cotacao": retorna_cotacao}

# Função que conversa com a API da OpenAI
def gera_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="gpt-3.5-turbo-0125",
        tools=tools,
        tool_choice="auto"
    )

    tools_calls = resposta.choices[0].message.tool_calls

    if tools_calls:
        mensagens.append({
            "role": resposta.choices[0].message.role,
            "content": resposta.choices[0].message.content,
            "tool_calls": [tc.model_dump() for tc in tools_calls]
        })

        for tool_call in tools_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_to_call = funcoes_disponiveis.get(function_name)

            if function_to_call:
                resultado = function_to_call(**function_args)

                mensagens.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": resultado
                })

        segunda_resposta = client.chat.completions.create(
            messages=mensagens,
            model="gpt-3.5-turbo-0125"
        )

        mensagens.append({
            "role": segunda_resposta.choices[0].message.role,
            "content": segunda_resposta.choices[0].message.content
        })

    else:
        mensagens.append({
            "role": resposta.choices[0].message.role,
            "content": resposta.choices[0].message.content
        })

    return mensagens

# === Streamlit App ===

st.set_page_config(page_title="Chatbot Financeiro", page_icon="📈")
st.title("Chatbot de Cotação de Ações 🤖")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe histórico de mensagens
for msg in st.session_state.mensagens:
    if isinstance(msg, dict):
        if msg.get("role") == "user":
            st.chat_message("user").markdown(msg.get("content", ""))
        elif msg.get("role") == "assistant":
            st.chat_message("assistant").markdown(msg.get("content", ""))

# Campo de entrada
user_input = st.chat_input("Digite sua pergunta sobre cotação de ações:")

if user_input:
    st.session_state.mensagens.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)

    st.session_state.mensagens = gera_texto(st.session_state.mensagens)

    ultima_msg = st.session_state.mensagens[-1]
    if isinstance(ultima_msg, dict) and ultima_msg.get("role") == "assistant":
        st.chat_message("assistant").markdown(ultima_msg.get("content", ""))
