import pygame


class InviseButton(pygame.sprite.Sprite):
    def __init__(self, position, size, text, screen, *groups, callback=None):
        """Создаем кнопку"""
        super().__init__(*groups)

        self.text = text
        self.position = (position[0], position[1])
        self.size = size
        self.screen = screen
        self.callback = callback

    def generate(self):
        """Генерируем кнопку"""
        fontObj = pygame.font.Font('resource/fonts/bitcell.ttf', 32)
        text_surface = fontObj.render(self.text, True, (255, 255, 255), None)
        text_rect = text_surface.get_rect(
            center=(self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2))
        self.screen.blit(text_surface, text_rect)

    def check_pressed(self, pressed_coord):
        """Проверяем если нажали"""
        if (pressed_coord[0] >= self.position[0] and pressed_coord[0] <= self.position[0] + self.size[0]) \
                and (pressed_coord[1] >= self.position[1] and pressed_coord[1] <= self.position[1] + self.size[1]):
            return self.callback
