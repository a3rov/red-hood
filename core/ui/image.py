import pygame
from loads import load_image


blocks_params = {
    'menu_background': ('menu_background1.png', ((0, 0), (480, 270))),
    'settings_background': ('settings_background1.png', ((0, 0), (480, 270))),
    'play_background': ('levels_background1.png', ((0, 0), (480, 270)))

}


class Image(pygame.sprite.Sprite):
    def __init__(self, coords, image, screen, *groups, multi=4):
        """Создаем изображение"""
        super().__init__(*groups)
        self.surf = load_image(blocks_params[image][0], blocks_params[image][1], multi=multi)
        self.rect = self.surf.get_rect().move(coords[0], coords[1])
        self.mask = pygame.mask.from_surface(self.surf)

        self.coords = coords
        self.screen = screen

    def generate(self):
        """Генерируем изображение"""
        self.screen.blit(self.surf, (self.coords[0], self.coords[1]))