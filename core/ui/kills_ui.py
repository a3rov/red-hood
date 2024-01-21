import pygame
from loads import load_image


blocks_params = {
    'background': ('countkills.png', ((0, 0), (128, 64))),

}


class KillsUI(pygame.sprite.Sprite):
    def __init__(self, max, screen):
        """Создаем табличку с убийствами"""
        super().__init__()
        self.surf = load_image(blocks_params['background'][0], blocks_params['background'][1], multi=4)
        self.rect = self.surf.get_rect().move(1300, 700)

        self.mask = pygame.mask.from_surface(self.surf)

        self.maxkills: int = max
        self.kills: int = 0

        self.screen = screen

    def generate(self):
        """Генерируем табличку"""
        fontObj = pygame.font.Font('resource/fonts/bitcell.ttf', 92)
        textSufaceObj = fontObj.render(f'{self.kills}/{self.maxkills}', True, (63, 40, 50), None)
        self.screen.blit(self.surf, (1100, 600))
        self.screen.blit(textSufaceObj, (1308, 685))
