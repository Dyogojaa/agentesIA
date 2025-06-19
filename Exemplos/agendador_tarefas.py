import os
import sys

# Nome do arquivo onde as tarefas serão salvas
NOME_ARQUIVO = "tarefas.txt"

def carregar_tarefas():
    """Carrega as tarefas do arquivo de texto."""
    tarefas = []
    # Usamos 'utf-8' explicitamente para garantir a leitura correta de caracteres especiais
    if os.path.exists(NOME_ARQUIVO):
        try:
            with open(NOME_ARQUIVO, 'r', encoding='utf-8') as f:
                for linha in f:
                    partes = linha.strip().split('|')
                    if len(partes) == 2:
                        descricao = partes[0].strip()
                        status = partes[1].strip().lower() == 'concluída'
                        tarefas.append({"descricao": descricao, "concluida": status})
        except Exception as e:
            print(f"Erro ao carregar tarefas: {e}. O arquivo pode estar corrompido ou ter codificação incorreta.")
            print("Tentando criar um novo arquivo de tarefas.")
            return [] # Retorna lista vazia para evitar quebra do programa
    return tarefas

def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo de texto."""
    # Usamos 'utf-8' explicitamente para garantir a escrita correta de caracteres especiais
    try:
        with open(NOME_ARQUIVO, 'w', encoding='utf-8') as f:
            for tarefa in tarefas:
                status_str = "Concluída" if tarefa["concluida"] else "Pendente"
                f.write(f"{tarefa['descricao']} | {status_str}\n")
    except Exception as e:
        print(f"Erro ao salvar tarefas: {e}. Verifique as permissões de escrita.")

def adicionar_tarefa(tarefas):
    """Adiciona uma nova tarefa à lista."""
    descricao = input("Digite a descrição da nova tarefa: ").strip()
    if descricao:
        tarefas.append({"descricao": descricao, "concluida": False})
        print(f"Tarefa '{descricao}' adicionada com sucesso!")
    else:
        print("A descrição da tarefa não pode ser vazia.")

def listar_tarefas(tarefas):
    """Lista todas as tarefas, mostrando o status."""
    if not tarefas:
        print("\nNenhuma tarefa na lista. Adicione uma nova tarefa!")
        return

    print("\n--- SUAS TAREFAS ---")
    for i, tarefa in enumerate(tarefas):
        status = "[X]" if tarefa["concluida"] else "[ ]"
        print(f"{i + 1}. {status} {tarefa['descricao']}")
    print("--------------------")

def marcar_tarefa_concluida(tarefas):
    """Marca uma tarefa existente como concluída."""
    listar_tarefas(tarefas)
    if not tarefas:
        return

    try:
        numero_tarefa = int(input("Digite o número da tarefa a ser marcada como concluída: "))
        if 1 <= numero_tarefa <= len(tarefas):
            tarefas[numero_tarefa - 1]["concluida"] = True
            print(f"Tarefa '{tarefas[numero_tarefa - 1]['descricao']}' marcada como concluída!")
        else:
            print("Número de tarefa inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")

def remover_tarefa(tarefas):
    """Remove uma tarefa da lista."""
    listar_tarefas(tarefas)
    if not tarefas:
        return

    try:
        numero_tarefa = int(input("Digite o número da tarefa a ser removida: "))
        if 1 <= numero_tarefa <= len(tarefas):
            tarefa_removida = tarefas.pop(numero_tarefa - 1)
            print(f"Tarefa '{tarefa_removida['descricao']}' removida com sucesso!")
        else:
            print("Número de tarefa inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")

def exibir_menu():
    """Exibe o menu de opções para o usuário."""
    print("\n--- GERENCIADOR DE TAREFAS ---")
    print("1. Adicionar Tarefa")
    print("2. Listar Tarefas")
    print("3. Marcar Tarefa como Concluída")
    print("4. Remover Tarefa")
    print("5. Sair")
    print("------------------------------")

def main():
    """Função principal que executa o aplicativo."""
    # Define a codificação padrão de entrada/saída para UTF-8.
    # Isso ajuda o Python a lidar corretamente com caracteres especiais no console.
    # Note: Isso pode não funcionar em todos os ambientes/versões de Python de forma consistente,
    # mas é uma boa prática. A melhor solução é configurar o terminal.
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

    tarefas = carregar_tarefas()

    while True:
        exibir_menu()
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            adicionar_tarefa(tarefas)
        elif escolha == '2':
            listar_tarefas(tarefas)
        elif escolha == '3':
            marcar_tarefa_concluida(tarefas)
        elif escolha == '4':
            remover_tarefa(tarefas)
        elif escolha == '5':
            salvar_tarefas(tarefas) # Salva antes de sair
            print("Saindo do aplicativo. Suas tarefas foram salvas!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()