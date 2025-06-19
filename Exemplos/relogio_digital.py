import tkinter as tk
import time

def atualizar_relogio():
    """
    Atualiza a hora exibida no relógio a cada segundo.
    """
    hora_atual = time.strftime("%H:%M:%S")
    label_relogio.config(text=hora_atual)
    label_relogio.after(1000, atualizar_relogio)

# --- Configuração da Janela (Root) ---
janela = tk.Tk()
janela.title("Relógio Digital")

# --- Define o tamanho fixo da janela do relógio ---
# Se for mudar o tamanho da fonte, ajuste esses valores para caber
largura_janela = 300
altura_janela = 100
janela.geometry(f"{largura_janela}x{altura_janela}")
janela.resizable(False, False) # Impede redimensionamento

# --- Obtém as dimensões da tela ---
# .winfo_screenwidth() e .winfo_screenheight() obtêm a resolução da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

# --- Calcula a posição para o canto superior direito ---
# Coordenada X: largura da tela - largura da janela - uma pequena margem (ex: 10 pixels)
x = largura_tela - largura_janela - 10
# Coordenada Y: uma pequena margem do topo (ex: 10 pixels)
y = 10

# --- Define a posição da janela ---
# A string de geometria é "Largura x Altura + X + Y"
janela.geometry(f"+{x}+{y}")

# --- Configuração do Label para exibir a hora ---
label_relogio = tk.Label(
    janela,
    font=("Arial", 40, "bold"),
    bg="black",
    fg="cyan"
)
label_relogio.pack(expand=True, fill="both")

# Inicia a atualização do relógio
atualizar_relogio()

# Inicia o loop principal da interface gráfica
janela.mainloop()