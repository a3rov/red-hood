import pygame


class Label(pygame.sprite.Sprite):
    def __init__(self, position, text, screen, *groups, type=None, step=2.5, coutdown=30, size=32, alpha=0):
        """Создаем текст"""
        super().__init__(*groups)
        self.text = text
        self.position = position
        self.screen = screen
        self.alpha = alpha
        self.type = type
        self.step = step

        self.iteration_to_die = 0
        self.coutdown = coutdown

        if self.type == 'kill':
            self.alpha = step

        self.size = size

    def generate(self):
        """Генерируем текст"""
        if self.iteration_to_die == self.coutdown:
            self.alpha -= self.step
            if self.alpha == 0:
                self.kill()
        elif self.type == 'kill' and self.alpha == 255:
            self.iteration_to_die += 1
        else:
            if self.alpha < 255:
                self.alpha += self.step
            else:
                if self.type != 'Once':
                    self.alpha = 0

        fontObj = pygame.font.Font('resource/fonts/bitcell.ttf', self.size)
        text_surface = fontObj.render(self.text, True, (255, 255, 255), None)
        text_surface.set_alpha(self.alpha)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.position[0], self.position[1])
        self.screen.blit(text_surface, text_rect)