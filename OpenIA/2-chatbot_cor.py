import openai
from colorama import Fore, Style, init

client = openai.Client()
init(autoreset=True)


def geracao_texto(mensagens):
    resposta = client.chat.completions.create(
        messages=mensagens,
        model="gpt-3.5-turbo-0125",
        temperature=0,
        max_tokens=1000,
        stream=True
    )
    
    print(f"{Fore.CYAN}Bot:", end="")
    
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
    print(f"{Fore.YELLOW}Bem Vindo ao Chatbot🐼")
    mensagens = []
    
    while True:
        in_user = input(f"{Fore.GREEN}User: {Style.RESET_ALL}")
        mensagens.append({"role":"user","content": in_user})
        mensagens = geracao_texto(mensagens)
    