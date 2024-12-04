import tkinter as tk
from tkinter import messagebox

def iniciar_puzzle(root, inventario, callback_atualizar_tela):
    """
    Puzzle da cabana para desbloquear itens no inventário.
    Resolve dois passos:
    1. Adiciona a lanterna.
    2. Adiciona a corda.
    """
    # Criar uma nova janela para o puzzle
    puzzle_window = tk.Toplevel(root)
    puzzle_window.title("Puzzle da Cabana")
    puzzle_window.geometry("600x300")

    # Variável para o texto do puzzle
    descricao_puzzle = tk.Label(
        puzzle_window, 
        text="Resolva o puzzle para ganhar itens!", 
        font=("Arial", 14)
    )
    descricao_puzzle.pack(pady=10)

    # Entrada para a resposta
    entrada = tk.Entry(puzzle_window, font=("Arial", 12))
    entrada.pack(pady=10)

    # Campo de dicas
    dica_label = tk.Label(puzzle_window, text="", font=("Arial", 12), fg="blue")
    dica_label.pack(pady=10)

    # Configurações de cada etapa do puzzle
    perguntas = [
        {
            "texto": "Digite o número que completa a sequência: 2, 4, 8, 16, ?",
            "resposta": "32",
            "item": "lanterna",
            "mensagem": "Você ganhou uma lanterna!",
            "dica": "Cada número é o dobro do anterior."
        },
        {
            "texto": "Digite o número que completa a sequência: 1, 1, 2, 3, 5, ?",
            "resposta": "8",
            "item": "corda",
            "mensagem": "Você ganhou uma corda!",
            "dica": "Soma os dois números anteriores para obter o próximo."
        }, 
        {
            "texto": "Qual numero não é par? 10, 29, 60, 28",
            "resposta": "29",
            "item": "chave",
            "mensagem": "Você ganhou uma chave!",
            "dica": "Esta bem facil."
        }
    ]
    etapa_atual = {"indice": 0}  # Dicionário para rastrear a etapa atual
    mensagens = []  # Lista para armazenar as mensagens dos itens ganhados

    # Atualizar o texto e a dica do puzzle
    def atualizar_puzzle():
        etapa = perguntas[etapa_atual["indice"]]
        descricao_puzzle.config(text=etapa["texto"])
        dica_label.config(text=f"Dica: {etapa['dica']}")
        entrada.delete(0, tk.END)  # Limpar a entrada
        
    # Função para verificar a resposta
    def verificar_resposta():
        resposta = entrada.get().strip()
        etapa = perguntas[etapa_atual["indice"]]
        if resposta == etapa["resposta"]:
            if etapa["item"] not in inventario:
                inventario.append(etapa["item"])
                mensagens.append(etapa["mensagem"])  # Adiciona a mensagem à lista
            etapa_atual["indice"] += 1

            # Verificar se existem mais etapas
            if etapa_atual["indice"] < len(perguntas):
                atualizar_puzzle()
            else:
                # Exibe todas as mensagens de uma vez após a última etapa
                messagebox.showinfo("Concluído!", "\n".join(mensagens) + "\nVocê completou o puzzle da cabana!")
                puzzle_window.destroy()
                callback_atualizar_tela()
        else:
            messagebox.showerror("Erro", "Resposta incorreta! Tente novamente.")

    # Botão de verificação
    tk.Button(puzzle_window, text="Verificar", font=("Arial", 12), command=verificar_resposta).pack(pady=10)

    # Botão de cancelar
    tk.Button(puzzle_window, text="Cancelar", font=("Arial", 12), command=puzzle_window.destroy).pack(pady=10)

    # Inicializar com a primeira etapa do puzzle
    atualizar_puzzle()
