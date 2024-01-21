import pygame
from loads import load_image


blocks_params = {
    '0': ('fields.png', ((0, 144), (16, 16))),
    '1': ('fields.png', ((16, 144), (48, 16))),
    '2': ('fields.png', ((64, 144), (16, 16))),
    '3': ('fields.png', ((80, 144), (16, 16))),
    '4': ('fields.png', ((96, 144), (96, 16))),
    '5': ('fields.png', ((192, 144), (32, 16))),
    '6': ('fields.png', ((224, 144), (48, 16))),
    '7': ('fields.png', ((272, 144), (16, 16))),
    '8': ('fields.png', ((160, 0), (128, 144))),
    '9': ('npc_default.png', ((0, 0), (32, 32))),
    '10': ('fields.png', ((80, 64), (32, 16))),
    '11': ('fields.png', ((112, 64), (16, 16))),
    '12': ('fields.png', ((128, 64), (32, 16))),
    '13': ('fields.png', ((0, 64), (16, 16))),
    '14': ('fields.png', ((16, 48), (16, 16))),
    '15': ('fields.png', ((48, 48), (32, 32))),
    '16': ('fields.png', ((64, 80), (16, 16))),
    '17': ('fields.png', ((64, 96), (16, 16))),
    '18': ('fields.png', ((80, 96), (16, 16))),
    '19': ('fields.png', ((96, 96), (16, 16))),
    '20': ('fields.png', ((112, 80), (48, 32))),
    '21': ('fields.png', ((80, 80), (16, 16))),
    '22': ('fields.png', ((96, 80), (16, 16))),

}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups, rotate=0):
        """Передаем тип тайла, координаты, позицию, группы"""
        super().__init__(*groups)
        self.surf = load_image(blocks_params[tile_type][0], blocks_params[tile_type][1], multi=6)
        self.type = tile_type
        self.rect = self.surf.get_rect().move(pos_x, pos_y)
        self.surf = pygame.transform.rotate(self.surf, rotate)

        self.mask = pygame.mask.from_surface(self.surf)
