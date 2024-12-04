import pygame
import pygame.mixer
from gerenciar_inventario import desenhar_inventario

# Inicializar o Pygame e o mixer do pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Aventura em Texto com Sons")

# Carregar os sons
sons = {
    "floresta": "sons/floresta.wav",
    "cabana": "sons/cabana.wav",
    "rio": "sons/rio.wav",
    "caverna": "sons/caverna.wav",
    "pontoon": "sons/pontoon.wav"
}

# Configurações iniciais
localizacao = "floresta"
caminho = []  # Pilha para armazenar o histórico de localizações
inventario = []

# Carregar as imagens dos locais e redimensioná-las
def carregar_imagem(localizacao):
    imagem = pygame.image.load(f"{localizacao}.jpg")
    imagem = pygame.transform.scale(imagem, (LARGURA_TELA, ALTURA_TELA))  # Redimensiona para a tela
    return imagem

imagens = {
    "floresta": carregar_imagem("floresta"),
    "cabana": carregar_imagem("cabana"),
    "rio": carregar_imagem("rio"),
    "caverna": carregar_imagem("caverna"),
    "pontoon": carregar_imagem("pontoon")
}

# Itens disponíveis
itens = {
    "chave": "Você encontrou uma chave enferrujada!",
    "lanterna": "Você encontrou uma lanterna. Agora pode explorar a caverna!",
    "corda": "Você encontrou uma corda. Pode ser útil para atravessar o rio!"
}

# Função para tocar o som do local
def tocar_som(localizacao):
    """Toca o som correspondente à localização."""
    if localizacao in sons:
        pygame.mixer.music.load(sons[localizacao])
        pygame.mixer.music.play(loops=-1)

# Variável para controlar se o jogador está no inventário
no_inventario = False
localizacao_antes_inventario = None  # Variável para armazenar o local antes de abrir o inventário

# Função para processar os comandos ao clicar nos botões
def processar_comando(comando):
    global localizacao, caminho, inventario, no_inventario, localizacao_antes_inventario

    if comando == "n":
        if localizacao == "floresta":
            caminho.append(localizacao)  # Adiciona o local atual ao caminho
            localizacao = "cabana"
        elif localizacao == "cabana":
            caminho.append(localizacao)
            localizacao = "caverna"
        elif localizacao == "caverna" and "lanterna" in inventario:
            caminho.append(localizacao)
            localizacao = "pontoon"
        atualizar_texto()
    elif comando == "l":
        if localizacao == "floresta":
            caminho.append(localizacao)
            localizacao = "rio"
        elif localizacao == "rio" and "corda" in inventario:
            caminho.append(localizacao)
            localizacao = "caverna"
        atualizar_texto()
    elif comando == "b":
        if caminho:
            localizacao = caminho.pop()  # Remove o último local do caminho e volta para ele
        atualizar_texto()
    elif comando == "i":
        localizacao_antes_inventario = localizacao  # Armazena o local antes de entrar no inventário
        no_inventario = True  # Entrando no inventário
        desenhar_inventario(tela, inventario)
    elif comando == "q":
        pygame.quit()
        quit()

    tocar_som(localizacao)
    explorar_localizacao()

# Função para atualizar o texto da narrativa
def atualizar_texto():
    tela.fill((0, 0, 0))  # Limpar a tela
    tela.blit(imagens[localizacao], (0, 0))  # Mostrar a imagem do local
    font = pygame.font.SysFont("Arial", 30)
    texto = font.render(f"Você está em: {localizacao}", True, (255, 255, 255))
    tela.blit(texto, (50, 50))  # Exibir o nome do local
    desenhar_botoes()  # Desenhar os botões
    pygame.display.update()

# Função para explorar a localização e adicionar itens ao inventário
def explorar_localizacao():
    global localizacao, inventario
    
    if localizacao == "cabana" and "chave" not in inventario:
        inventario.append("chave")
        print(itens["chave"])
    elif localizacao == "caverna" and "lanterna" not in inventario:
        inventario.append("lanterna")
        print(itens["lanterna"])
    elif localizacao == "rio" and "corda" not in inventario:
        inventario.append("corda")
        print(itens["corda"])
    elif localizacao == "pontoon" and "chave" in inventario:
        print("Você usou a chave para abrir o portão e atravessou a ponte!")
    elif localizacao == "pontoon" and "chave" not in inventario:
        print("Você precisa de uma chave para atravessar a ponte.")

# Função para desenhar os botões
def desenhar_botoes():
    font = pygame.font.SysFont("Arial", 24)
    
    # Obter posição do mouse
    mouse_pos = pygame.mouse.get_pos()

    # Definir cores de texto padrão e de hover
    cor_normal = (255, 255, 255)  # Cor normal do texto (branco)
    cor_hover = (255, 215, 0)  # Cor do texto quando o mouse passa sobre o botão (amarelo)
    
    # Botão "Norte"
    if 50 <= mouse_pos[0] <= 150 and 500 <= mouse_pos[1] <= 540:
        cor = cor_hover
    else:
        cor = cor_normal
    botao_norte = font.render("Norte", True, cor)
    tela.blit(botao_norte, (50, 500))

    # Botão "Leste"
    if 200 <= mouse_pos[0] <= 300 and 500 <= mouse_pos[1] <= 540:
        cor = cor_hover
    else:
        cor = cor_normal
    botao_leste = font.render("Leste", True, cor)
    tela.blit(botao_leste, (200, 500))
    
    # Botão "Voltar"
    if 350 <= mouse_pos[0] <= 450 and 500 <= mouse_pos[1] <= 540:
        cor = cor_hover
    else:
        cor = cor_normal
    botao_voltar = font.render("Voltar", True, cor)
    tela.blit(botao_voltar, (350, 500))

    # Botão "Inventário"
    if 500 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 540:
        cor = cor_hover
    else:
        cor = cor_normal
    botao_inventario = font.render("Inventário", True, cor)
    tela.blit(botao_inventario, (500, 500))
    
    # Botão "Sair"
    if 650 <= mouse_pos[0] <= 750 and 500 <= mouse_pos[1] <= 540:
        cor = cor_hover
    else:
        cor = cor_normal
    botao_sair = font.render("Sair", True, cor)
    tela.blit(botao_sair, (650, 500))

# Função para verificar cliques do mouse
def verificar_clique():
    global no_inventario, localizacao_antes_inventario  # Acessar a variável no_inventario

    mouse_pos = pygame.mouse.get_pos()

    # Verificar clique nos botões do menu principal
    if 50 <= mouse_pos[0] <= 150 and 500 <= mouse_pos[1] <= 540:
        processar_comando("n")
    elif 200 <= mouse_pos[0] <= 300 and 500 <= mouse_pos[1] <= 540:
        processar_comando("l")
    elif 350 <= mouse_pos[0] <= 450 and 500 <= mouse_pos[1] <= 540:
        processar_comando("b")
    elif 500 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 540:
        processar_comando("i")
    elif 650 <= mouse_pos[0] <= 750 and 500 <= mouse_pos[1] <= 540:
        if not no_inventario:  # Verifica se não está no inventário
            processar_comando("q")  # Fechar o jogo, se não estiver no inventário
        else:
            processar_comando("b")  # Voltar para a tela principal do jogo, se estiver no inventário

    # Se estiver no inventário, ao clicar no botão "Sair" do inventário
    if no_inventario and 650 <= mouse_pos[0] <= 750 and 500 <= mouse_pos[1] <= 540:
        no_inventario = False  # Sai do inventário
        localizacao = localizacao_antes_inventario  # Volta para o local de onde o jogador estava
        atualizar_texto()  # Atualiza a tela

# Loop principal do jogo
tocar_som(localizacao)
atualizar_texto()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            verificar_clique()

    pygame.display.update()