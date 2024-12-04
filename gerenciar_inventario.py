import pygame

# Função para desenhar o inventário com o botão "Sair"
def desenhar_inventario(tela, inventario):
    tela.fill((0, 0, 0))  # Limpar a tela
    font = pygame.font.SysFont("Arial", 30)
    y_pos = 50  # Posição inicial no eixo Y
    
    # Exibir todos os itens do inventário
    for item in inventario:
        texto = font.render(f"{item.capitalize()}", True, (255, 255, 255))
        tela.blit(texto, (50, y_pos))
        y_pos += 40  # Espaçamento entre os itens

    # Botão "Sair" para fechar o inventário
    botao_sair = font.render("Sair", True, (255, 0, 0))  # Cor vermelha para o botão
    tela.blit(botao_sair, (650, 500))  # Posição do botão "Sair"

    pygame.display.update()
    
# gerenciar_inventario.py

def adicionar_item(inventario, item):
    """
    Adiciona um item ao inventário.
    """
    if item not in inventario:
        inventario.append(item)
        return f"Item '{item}' adicionado ao inventário!"
    return f"Item '{item}' já está no inventário."

def remover_item(inventario, item):
    """
    Remove um item do inventário.
    """
    if item in inventario:
        inventario.remove(item)
        return f"Item '{item}' removido do inventário!"
    return f"Item '{item}' não está no inventário."

def listar_inventario(inventario):
    """
    Lista os itens no inventário.
    """
    if not inventario:
        return "O inventário está vazio."
    return "Itens no inventário: " + ", ".join(inventario)
