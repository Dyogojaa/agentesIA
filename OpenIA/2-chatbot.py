import openai

client = openai.Client()


def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="gpt-3.5-turbo-0125",
        temperature=0,
        max_tokens=1000,
        stream=True
    )
    
    print("Bot:", end="")
    
    texto_completo =""
    
    for resposta_stream in resposta:
        texto = resposta_stream.choices[0].delta.content
        if texto:
            print(texto, end="")
            texto_completo += texto

    
    print()
    mensagens.append({"role":"assistant", "content": texto_completo})        
    return mensagens

if __name__ == "__main__":
    print("Bem Vindo ao Chatbot🐼")
    mensagens = []
    
    while True:
        in_user = input("User: ")
        mensagens.append({"role":"user","content": in_user})
        mensagens = geracao_texto(mensagens)
        
            
            
    
    