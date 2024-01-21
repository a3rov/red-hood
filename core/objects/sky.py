import pygame
from loads import load_image


class Sky(pygame.sprite.Sprite):
    def __init__(self, screen, *groups):
        """Передаем тип тайла, координаты, позицию, группы"""
        super().__init__(*groups)
        self.surf1 = load_image('background_0.png', ((0, 0), (288, 180)), multi=6)
        self.surf2 = load_image('background_1.png', ((0, 0), (288, 180)), multi=6)
        self.surf3 = load_image('background_2.png', ((0, 0), (288, 180)), multi=6)
        self.rect1 = self.surf1.get_rect().move(0, 0)
        self.rect2 = self.surf2.get_rect().move(0, 0)
        self.rect3 = self.surf3.get_rect().move(0, 0)
        self.screen = screen

        self.sky_x = 0

    def skyfill(self):
        """Заполняем небо"""
        self.screen.blit(self.surf1, (self.rect1.x + self.sky_x, self.rect1.y))
        self.screen.blit(self.surf2, (self.rect2.x + self.sky_x, self.rect2.y))
        self.screen.blit(self.surf3, (self.rect3.x + self.sky_x, self.rect3.y))


