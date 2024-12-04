import tkinter as tk
from tkinter import messagebox
from playsound import playsound
import threading
from PIL import Image, ImageTk
from puzzle_cabana import iniciar_puzzle
from puzzle_troll import iniciar_puzzle_troll
import pygame
import os

# Configurações da janela
LARGURA_TELA = 760
ALTURA_TELA = 400

# Inicializar a janela principal
root = tk.Tk()
root.title("Aventura em Texto com Sons")
root.geometry(f"{LARGURA_TELA}x{ALTURA_TELA}")

# Variáveis globais
localizacao = "floresta"
caminho = []  # Pilha para armazenar o histórico de localizações
inventario = []
no_inventario = False

# Caminho base para os arquivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dicionário de sons com caminhos absolutos
sons = {
    "fim": os.path.join(BASE_DIR, "sons", "fim.wav"),
    "floresta": os.path.join(BASE_DIR, "sons", "floresta.wav"),
    "cabana": os.path.join(BASE_DIR, "sons", "caverna.wav"),
    "caverna": os.path.join(BASE_DIR, "sons", "caverna.wav"),
    "voz_floresta": os.path.join(BASE_DIR, "sons", "voz_floresta.wav"),
    "voz_cabana": os.path.join(BASE_DIR, "sons", "voz_cabana.wav"),
    "voz_caverna": os.path.join(BASE_DIR, "sons", "voz_caverna.wav"),
    "voz_pontoon": os.path.join(BASE_DIR, "sons", "voz_pontoon.wav"),
}

imagens = {
    "floresta": os.path.join(BASE_DIR, "imagens", "floresta.jpg"),
    "cabana": os.path.join(BASE_DIR, "imagens", "cabana.jpg"),
    "rio": os.path.join(BASE_DIR, "imagens", "rio.jpg"),
    "caverna": os.path.join(BASE_DIR, "imagens", "caverna.jpg"),
    "pontoon": os.path.join(BASE_DIR, "imagens", "pontoon.jpg"),
}

# Elementos visuais
imagem_label = tk.Label(root)
imagem_label.pack(fill="both", expand=True)

texto_label = tk.Label(root, text="", font=("Arial", 16), bg="black", fg="white")
texto_label.pack(fill="x", pady=10)

def redimensionar_imagem(event=None):
    """Redimensiona a imagem para caber no tamanho atual da janela."""
    largura = root.winfo_width()
    altura = root.winfo_height() - texto_label.winfo_height() - 50  # Subtraí altura do texto e botões

    # Verificar se as dimensões são válidas
    if largura <= 0 or altura <= 0:
        return  # Não tenta redimensionar se as dimensões não forem válidas

    img_path = imagens[localizacao]
    img = Image.open(img_path)
    img = img.resize((largura, altura), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    imagem_label.configure(image=img)
    imagem_label.image = img

# Atualizar o texto e som da tela
def atualizar_tela(tocar=True):
    redimensionar_imagem()
    texto_label.configure(text=f"Você está em: {localizacao}")
    mostrar_historia()

    if tocar:
        tocar_som(sons[localizacao])

def tocar_som(caminho_som):
    if not os.path.exists(caminho_som):
        print(f"Erro: Arquivo de som não encontrado: {caminho_som}")
        return
    pygame.mixer.init()
    pygame.mixer.music.load(caminho_som)
    pygame.mixer.music.play()

# Função para mostrar a história
def mostrar_historia():
    historias = {
        "floresta": "Você está na floresta. Ouve o som das árvores ao vento.",
        "cabana": "Você chegou à cabana abandonada. A porta range.",
        "rio": "Você está à beira de um rio calmo. É necessário atravessar.",
        "caverna": "Você entrou na caverna escura. Um arrepio percorre sua espinha.",
        "pontoon": "Você alcançou a ponte. Parece instável, mas é a única maneira.",
        "fim": "Você cruzou a ponte e completou sua aventura com sucesso!"
    }
    historia = historias.get(localizacao, "Um lugar misterioso...")
    messagebox.showinfo("História", historia)

# Função para processar os comandos
def processar_comando(comando):
    global localizacao, caminho, inventario

    anterior = localizacao  # Salvar a localização anterior para comparar depois

    if comando == "n":
        if localizacao == "floresta":
            caminho.append(localizacao)
            localizacao = "cabana"
            if "lanterna" not in inventario or "corda" not in inventario:
                iniciar_puzzle(root, inventario, lambda: atualizar_tela(False))
                return
        elif localizacao == "cabana":
            caminho.append(localizacao)
            localizacao = "caverna"
        elif localizacao == "caverna":
            if "lanterna" in inventario:
                caminho.append(localizacao)
                localizacao = "pontoon"
            else:
                messagebox.showwarning("Aviso", "Você precisa de uma lanterna para explorar a caverna.")
        elif localizacao == "pontoon":
            iniciar_puzzle_troll(root, lambda: atualizar_tela(False))
            return
    elif comando == "l":
        if localizacao == "floresta":
            caminho.append(localizacao)
            localizacao = "rio"
        elif localizacao == "rio":
            if "corda" in inventario:
                caminho.append(localizacao)
                localizacao = "caverna"
            else:
                messagebox.showwarning("Aviso", "Você precisa de uma corda para atravessar o rio.")
    elif comando == "b":
        if caminho:
            localizacao = caminho.pop()
        else:
            messagebox.showinfo("Aviso", "Você já está no início do caminho.")
    elif comando == "i":
        abrir_inventario()
        return

    # Atualizar a tela apenas se a localização mudou
    if localizacao != anterior:
        atualizar_tela()

# Adicionar evento de redimensionamento para ajustar a imagem
root.bind("<Configure>", redimensionar_imagem)

# Iniciar o jogo com som do local inicial
tocar_som(sons[localizacao])
atualizar_tela(tocar=False)

def avancar_para_fim():
    global localizacao
    localizacao = "fim"
    atualizar_tela()
    finalizar_jogo()

def finalizar_jogo():
    messagebox.showinfo(
        "Parabéns!",
        "Você derrotou o troll e atravessou a ponte com segurança.\n\n"
        "Parabéns, você completou sua jornada e venceu o jogo!"
    )
    root.quit()  # Fecha a janela principal

# Função para abrir o inventário
def abrir_inventario():
    global no_inventario
    no_inventario = True
    inv_window = tk.Toplevel(root)
    inv_window.title("Inventário")
    inv_window.geometry("400x300")

    for item in inventario:
        tk.Label(inv_window, text=item, font=("Arial", 14)).pack(pady=5)
    tk.Button(inv_window, text="Fechar", command=inv_window.destroy).pack(pady=10)

# Adicionar controles
botoes_frame = tk.Frame(root, bg="gray")
botoes_frame.pack(fill="x")

botoes = {
    "Norte": lambda: processar_comando("n"),
    "Leste": lambda: processar_comando("l"),
    "Voltar": lambda: processar_comando("b"),
    "Inventário": lambda: abrir_inventario(),
}

for texto, comando in botoes.items():
    btn = tk.Button(botoes_frame, text=texto, command=comando, width=15, font=("Arial", 12))
    btn.pack(side="left", padx=5, pady=5)

# Inicializar a interface
atualizar_tela()
root.mainloop()
