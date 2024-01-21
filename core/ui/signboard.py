import pygame


class Signboard(pygame.sprite.Sprite):
    def __init__(self, position, size, text, screen, *groups, type='attention', step=15, coutdown=30):
        """Создаем плашку для текста"""
        super().__init__(*groups)

        self.text = text
        self.position = (position[0], position[1])
        self.size = size
        self.screen = screen
        self.rotate = 0
        self.color = (139, 23, 255)
        self.type = type
        self.step = step
        self.alpha = 0

        self.iteration_to_die = 0
        self.coutdown = coutdown

        if self.type == 'kill':
            self.alpha = step

    def generate(self):
        """Генерируем плашку и работаем с ней"""
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

        fontObj = pygame.font.Font('resource/fonts/bitcell.ttf', 32)
        text_surface = fontObj.render(self.text, True, (255, 255, 255), None)
        text_rect = text_surface.get_rect(
            center=(self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2))

        fontObj2 = pygame.font.Font('resource/fonts/bitcell.ttf', 32)
        text_surface2 = fontObj2.render(self.text, True, self.color, None)
        text_rect2 = text_surface2.get_rect(
            center=(self.position[0] + self.size[0] / 2 + 2, self.position[1] + self.size[1] / 2 + 2))

        if self.type == 'attention':
            text_surface.set_alpha(self.alpha)

        if self.type == 'attention':
            text_surface2.set_alpha(self.alpha)

        pygame.draw.rect(self.screen, (0, 0, 0), (self.position[0], self.position[1], self.size[0], self.size[1]))

        self.screen.blit(text_surface2, text_rect)
        self.screen.blit(text_surface, text_rect2)
