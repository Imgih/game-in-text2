def iniciar_puzzle_troll(root, callback_atualizar_tela):
    puzzle_window = tk.Toplevel(root)
    puzzle_window.title("Puzzle do Troll")
    puzzle_window.geometry("600x300")

    descricao_puzzle = tk.Label(
        puzzle_window,
        text="O troll exige que você resolva seu enigma para atravessar a ponte.",
        font=("Arial", 14)
    )
    descricao_puzzle.pack(pady=10)

    entrada = tk.Entry(puzzle_window, font=("Arial", 12))
    entrada.pack(pady=10)

    pergunta = {
        "texto": "Eu ando sem pés, voo sem asas e nunca paro de correr. O que sou eu?",
        "resposta": "rio",
        "mensagem": "Resposta correta! O troll permite que você passe.",
    }

    descricao_pergunta = tk.Label(puzzle_window, text=pergunta["texto"], font=("Arial", 12))
    descricao_pergunta.pack(pady=10)

    def verificar_resposta():
        resposta = entrada.get().strip().lower()
        if resposta == pergunta["resposta"]:
            messagebox.showinfo("Vitória!", pergunta["mensagem"])
            puzzle_window.destroy()
            callback_atualizar_tela()  # Atualizar a tela após resolver o puzzle
        else:
            messagebox.showerror("Erro", "Resposta incorreta! Tente novamente.")

    tk.Button(puzzle_window, text="Verificar", font=("Arial", 12), command=verificar_resposta).pack(pady=10)
    tk.Button(puzzle_window, text="Cancelar", font=("Arial", 12), command=puzzle_window.destroy).pack(pady=10)
