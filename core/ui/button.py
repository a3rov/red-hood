import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, position, size, text, screen, *groups, callback=None, color=None):
        """Создаем саму кнопку"""
        super().__init__(*groups)
        self.text = text
        self.position = (position[0], position[1])
        self.size = size
        self.screen = screen
        self.callback = callback

        if color is not None:
            self.color = color
        else:
            self.color = (5, 32, 45)

    def generate(self):
        """Создаем кнопку и отрисовываем ее"""
        pygame.draw.rect(self.screen, self.color, (self.position[0], self.position[1], self.size[0], self.size[1]))
        font = pygame.font.Font('resource/fonts/bitcell.ttf', 32)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2))
        self.screen.blit(text_surface, text_rect)

    def check_pressed(self, pressed_coord):
        """Проверяем, что нажата"""
        if (pressed_coord[0] >= self.position[0] and pressed_coord[0] <= self.position[0] + self.size[0]) \
                and (pressed_coord[1] >= self.position[1] and pressed_coord[1] <= self.position[1] + self.size[1]):
            return self.callback