import yfinance as yf
import openai
import json
import pandas as pd


client = openai.Client()


def retorna_cotacao(ticker, periodo="1mo"):
    ticker_obj = yf.Ticker(f"{ticker}.SA")
    hist = ticker_obj.history(period=periodo)["Close"]
    hist = round(hist, 2)

    # Garante que o índice é datetime
    hist.index = pd.to_datetime(hist.index)
    hist.index = hist.index.strftime("%Y-%m-%d")

    # Limitar a 30 resultados
    if len(hist) > 30:
        slice_size = max(1, len(hist) // 30)
        hist = hist.iloc[::slice_size].iloc[::-1]

    return hist.to_json()

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
                        "description": "O ticker da ação. Ex: BBAS3, BBDC4, etc"
                    },
                    "periodo": {
                        "type": "string",
                        "description": "Período retornado dos dados históricos da cotação, sendo que '1mo' equivale a um mês,\
                            '1d' equivale a um dia, '1y' equivale a um ano \
                                e 'ytd' equivale ao ano atual",
                        "enum": ["1d", "5d", "1mo", "6mo", "1y", "5y", "ytd", "max"]
                    }
                },
                "required": ["ticker"]
            }
        }
    }
]

funcao_disponivel = {"retorna_cotacao": retorna_cotacao}

mensagens = [{"role":"user", "content": "Qual é a cotação do Petrobras no ultimo Ano ?"}]

resposta = client.chat.completions.create(
    messages=mensagens,
    model="gpt-3.5-turbo-0125",
    tools=tools,
    tool_choice = "auto"
    
)

tools_calls = resposta.choices[0].message.tool_calls
# print(tools_calls)

if tools_calls:
    mensagens.append(resposta.choices[0].message)
    for tool_call in tools_calls:
        function_name = tool_call.function.name
        function_to_call = funcao_disponivel[function_name]
        function_args = json.loads(tool_call.function.arguments)
        function_return = function_to_call(**function_args) 
        
        mensagens.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_return            
            })
        
        segunda_resposta = client.chat.completions.create(
                  messages=mensagens,
                  model="gpt-3.5-turbo-0125",                 
                )
        
        mensagens.append(segunda_resposta.choices[0].message)
        print(segunda_resposta.choices[0].message.content)
        
        

