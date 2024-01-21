import json

import pygame

from core.objects.player import Player
from core.objects.sky import Sky
from core.objects.tile import Tile, blocks_params

from loads import load_image


clock = pygame.time.Clock()

FPS = 60

coef_x = 0
coef_y = 0

behind_id = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]


class TileForBuild(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        """Передаем тип тайла, координаты, позицию, группы"""
        super().__init__(*groups)
        self.surf = load_image(blocks_params[tile_type][0], blocks_params[tile_type][1], multi=6)
        self.type = tile_type
        self.rect = self.surf.get_rect().move(pos_x, pos_y)

        self.mask = pygame.mask.from_surface(self.surf)


class World:
    def __init__(self, screen, width, height, level='LEVEL 4'):
        """Объявляем параметры мира и экрана"""
        pygame.init()

        self.screen = screen
        self.width, self.height = width, height

        self.all_sprites = pygame.sprite.Group()
        self.blocks_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()

        self.sky = Sky(self.screen)
        self.sky2 = Sky(self.screen)
        self.sky2.sky_x += 1920

        self.level = level
        self.levels = {}

        with open('resource/levels.json') as json_file:
            self.levels = json.load(json_file)

        self.angle = 0

        self.current_block = 0
        self.tile_for_build: TileForBuild = TileForBuild('0', pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], self.all_sprites)

        self.load_level(self.level)

    def next_block(self):
        if self.current_block + 1 == len(blocks_params):
            self.current_block = 0
        else:
            self.current_block += 1

        if self.current_block in behind_id:
            self.tile_for_build: Tile = Tile(str(self.current_block), pygame.mouse.get_pos()[0],
                                             pygame.mouse.get_pos()[1],
                                             self.all_sprites, self.blocks_group)
        else:
            self.tile_for_build: Tile = Tile(str(self.current_block), pygame.mouse.get_pos()[0],
                                             pygame.mouse.get_pos()[1],
                                             self.all_sprites)

    def add_block(self, mouse):
        param = 'default'
        if str(self.current_block) in behind_id:
            param = 'behind'
        self.levels[self.level]['obj'].append([str(self.current_block), mouse[0] - coef_x, mouse[1] - coef_y, param, self.angle])
        with open('resource/levels.json', 'w') as f:
            json.dump(self.levels, f, indent=1)
            print('created')

        with open('resource/levels.json') as json_file:
            self.levels = json.load(json_file)

        self.load_level(self.level)

    def delete_block(self, mouse):
        for i in self.levels[self.level]['obj']:
            if (mouse[0]>= i[1] + coef_x and mouse[0] <= i[1] + coef_x + 50) \
                    and (mouse[1] >= i[2] + coef_y and mouse[1] <= i[2] + coef_y + 50):
                del self.levels[self.level]['obj'][self.levels[self.level]['obj'].index(i)]

        with open('resource/levels.json', 'w') as f:
            json.dump(self.levels, f, indent=1)
            print('deleted')

        with open('resource/levels.json') as json_file:
            self.levels = json.load(json_file)

        self.load_level(self.level)

    def load_level(self, level):
        for sprite in self.all_sprites:
            if not isinstance(sprite, Player) and not isinstance(sprite, TileForBuild):
                sprite.kill()

        for sprite in self.blocks_group:
            sprite.kill()

        for i in self.levels[level]['obj']:
            if i[0] != 'npc':
                if i[3] == 'default':
                    tile = Tile(i[0], i[1] + coef_x, i[2] + coef_y, self.all_sprites, self.blocks_group)
                    tile.surf = pygame.transform.rotate(tile.surf, i[4])
                elif i[3] == 'behind':
                    tile = Tile(i[0], i[1] + coef_x, i[2] + coef_y, self.all_sprites)
                    tile.surf = pygame.transform.rotate(tile.surf, i[4])

    def tickuptade(self):
        global coef_x
        global coef_y
        self.sky.skyfill()
        pressed = list(pygame.key.get_pressed())

        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                self.tile_for_build.rect.x = mouse_x
                self.tile_for_build.rect.y = mouse_y
                self.tile_for_build.surf = pygame.transform.rotate(self.tile_for_build.surf, self.angle)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button = event.button
                if button == 1:
                    self.add_block((mouse_x, mouse_y))

                if button == 3:
                    self.delete_block((mouse_x, mouse_y))

            if event.type == pygame.MOUSEWHEEL:
                self.tile_for_build.kill()
                self.next_block()

        if True in pressed:
            # Обработка передвижения персонажа
            pressed = list(pygame.key.get_pressed())
            pressed_keys = [i for i in range(len(pressed)) if pressed[i] is True]

            if 79 in pressed_keys or 7 in pressed_keys:
                coef_x -= 50
            if 80 in pressed_keys or 4 in pressed_keys:
                coef_x += 50

            if 82 in pressed_keys or 26 in pressed_keys:
                coef_y += 50

            if 22 in pressed_keys:
                coef_y -= 50

            if 20 in pressed_keys:
                self.angle -= 90

            if 8 in pressed_keys:
                self.angle += 90

            if 8 in pressed_keys:
                self.angle += 90

            if 30 in pressed_keys:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.add_block((mouse_x, mouse_y))

            if 31 in pressed_keys:
                self.tile_for_build.kill()
                self.next_block()

            self.load_level(self.level)

        for obj in self.all_sprites:
            self.screen.blit(obj.surf, obj.rect)

        self.screen.blit(self.tile_for_build.surf, self.tile_for_build.rect)

        pygame.display.flip()
        clock.tick(60)


size = width, height = 1920, 1080
screen = pygame.display.set_mode((1920, 1080))
screen.get_width()

world = World(screen, width, height)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление игрового мира
    world.tickuptade()

# Завершение работы pygame
pygame.quit()
