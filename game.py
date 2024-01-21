import pygame
from menu import Menu
from core.world.world import World


size = width, height = 1920, 1080
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption('RedHood')

programIcon = pygame.image.load('resource/img/icon.png')
pygame.display.set_icon(programIcon)


screen.get_width()

running = True
output = 'menu'
world = None
menu = Menu(screen, width, height)

while running:
    """Работаем с циклом, если статус (output) menu, то отображаем меню, иначе отображаем игру"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if output == 'menu':
        responce = menu.tickuptade()
        if responce == 'exit':
            break

        if responce is not None:
            world = World(screen, width, height, level=responce)
            output = 'game'
    else:
        responce = world.tickuptade()
        if responce == 'end':
            menu = Menu(screen, width, height)
            output = 'menu'

# Завершение работы pygame
pygame.quit()
