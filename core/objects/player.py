import pygame
import math
import json

import threading

from core.objects.tile import Tile
from core.world import physic

from core.objects.sound import sound_fight, sound_step
from loads import load_image


GRAVITY = physic.GRAVITY
JUMP_COUNT_CONSTATE = 13


frames = {
    'default': (('player_default.png', ((0, 0), (32, 32)), 4),
                ('player_default.png', ((32, 0), (32, 32)), 4),
                ('player_default.png', ((64, 0), (32, 32)), 4),
                ('player_default.png', ((96, 0), (32, 32)), 4),
                ('player_default.png', ((128, 0), (32, 32)), 4),
                ('player_default.png', ((160, 0), (32, 32)), 4)),

    'walking': [('player_walking.png', ((0, 0), (32, 32)), 4),
                ('player_walking.png', ((32, 0), (32, 32)), 4),
                ('player_walking.png', ((64, 0), (32, 32)), 4),
                ('player_walking.png', ((96, 0), (32, 32)), 4),
                ('player_walking.png', ((128, 0), (32, 32)), 4),
                ('player_walking.png', ((160, 0), (32, 32)), 4),
                ('player_walking.png', ((192, 0), (32, 32)), 4),
                ('player_walking.png', ((224, 0), (32, 32)), 4)],

    'falling': [('player_falling.png', ((0, 0), (32, 32)), 4),
                ('player_falling.png', ((32, 0), (32, 32)), 4),
                ('player_falling.png', ((64, 0), (32, 32)), 4)],

    'jumping': [('player_jumping.png', ((0, 0), (32, 32)), 4),
                ('player_jumping.png', ((32, 0), (32, 32)), 4),
                ('player_jumping.png', ((64, 0), (32, 32)), 4)],

    'dying': [('player_dying.png', ((0, 0), (32, 32)), 4),
              ('player_dying.png', ((32, 0), (32, 32)), 4),
              ('player_dying.png', ((64, 0), (32, 32)), 4),
              ('player_dying.png', ((96, 0), (32, 32)), 4),
              ('player_dying.png', ((128, 0), (32, 32)), 4),
              ('player_dying.png', ((160, 0), (32, 32)), 4),
              ('player_dying.png', ((192, 0), (32, 32)), 4),
              ('player_dying.png', ((224, 0), (32, 32)), 4),
              ('player_dying.png', ((256, 0), (32, 32)), 4)]
}

behind_id = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 8]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weapon, all_sprites, block_group, particle_group, *groups):
        """Создаем Player для работы с ним, передаем в него координаты, оружие, группы"""
        super().__init__(*groups)

        self.all_sprites = all_sprites
        self.block_group = block_group
        self.particle_group = particle_group

        self.image = None

        self.delay_fight = 0
        self.delay_jump = 0
        self.status = 'default'

        self.frames = dict()
        self.frames['default'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['default']]
        self.frames['walking'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['walking']]
        self.frames['falling'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['falling']]
        self.frames['damage'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['falling']]
        self.frames['dying'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['dying']]
        self.frames['jumping'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['jumping']]

        self.cur_frame = 0
        self.image = self.frames[self.status][self.cur_frame]
        self.need_iteration = 5

        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.surf = self.image

        self.pos_y = pos_y
        self.speed_y = 0
        self.jump_count = JUMP_COUNT_CONSTATE

        self.mask = pygame.mask.from_surface(self.surf)

        self.speed = 8
        self.weapon = weapon
        self.hp = 100

        self.iteration = 5

        self.side = 'right'
        self.fall_speed = 5
        self.frame_from_damage = 0
        self.sound_step_can_play = True
        self.power = 33

        if self.get_difficult() == 1:
            self.power = 65

        if self.get_difficult() == 2:
            self.power = 33

        if self.get_difficult() == 3:
            self.power = 12

    def changepos(self, coord, value):
        """Меняем позицию игрока"""
        if coord == 'x':
            self.try_move('x', value)
            if value < 0 and self.side == 'right':
                self.side = 'left'
            elif value > 0 and self.side == 'left':
                self.side = 'right'

        self.check_status('walking')
        if self.sound_step_can_play and self.status == ('walking' or 'default'):
            sound_step()
            self.sound_step_can_play = False
            threading.Timer(0.35, self.allow_sound_step).start()

    def check_shoot(self):
        """Проверяем возможность выстрела, если невозможно, то разрешаем"""
        if self.delay_fight == 300:
            self.delay_fight = 0

    def update(self):
        """Производим обновление персонажа. поворот, анимация, падение/прыжок/смерть, соприкосновение с Tile"""
        if self.iteration == self.need_iteration:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.status])
            self.surf = self.frames[self.status][self.cur_frame]
            self.iteration = 0
            if self.side == 'left':
                self.surf = pygame.transform.flip(self.surf, True, False)

            if self.cur_frame == 8 and self.status == 'dying':
                self.kill()

        if self.hp <= 0:
            self.check_status('dying')
            self.iteration += 1
            return

        if self.status == 'damage':
            damage_x = [3, 4, 5, 9, 13, 15, 14, 12, 10, 9, 5]
            damage_y = [1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
            if self.frame_from_damage == 10:
                self.status = 'default'
                self.frame_from_damage = 0
                return
            if self.side == 'right':
                self.try_move('x', -damage_x[self.frame_from_damage])
            else:
                self.try_move('x', damage_x[self.frame_from_damage])

            self.try_move('y', -damage_y[self.frame_from_damage])

            self.frame_from_damage += 1
            return

        if (not any([False if j is None else True for j in
                     [pygame.sprite.collide_mask(self, i) for i in
                      list(filter(lambda x: isinstance(x, Tile) and int(x.type) not in behind_id,
                                  self.block_group.sprites()))]]) and self.status != 'jumping'):
            self.check_status('falling')

        if self.status == 'falling':
            self.speed_y += GRAVITY
            if not self.try_move('y', self.speed_y):
                y = self.try_move('y', self.speed_y, True).rect.y - 105
                self.rect.y = y
                self.status = 'default'
                self.speed_y = 0

            self.rect.y += int(self.speed_y)

            if self.pos_y > 1080:
                self.kill()

            if self.speed_y > 20:
                self.status = 'default'
                self.speed_y = 0
                self.hp -= 60

        elif self.status == 'jumping':
            if self.jump_count >= -JUMP_COUNT_CONSTATE:
                if self.jump_count > 0:
                    if not self.try_move('y', -int((self.jump_count ** 2) // 3.5)):
                        self.jump_count = JUMP_COUNT_CONSTATE
                        self.status = 'falling'
                else:
                    self.jump_count = JUMP_COUNT_CONSTATE
                    self.status = 'falling'

                self.jump_count -= 1

        self.iteration += 1

    def check_status(self, status):
        """Проверяем статус и при необходимости изменяем его"""
        if status == 'dying' and self.status != 'dying':
            self.status = 'dying'
        if self.status == 'dying' or self.status == 'falling' or self.status == 'jumping'\
                or self.status == 'damage':
            return False
        if self.status != status:
            self.status = status
            self.cur_frame = 0
            return self.status

    def try_move(self, axis, value, get=False):
        """Проверка успешного передвижения, передвигаем, если возможно"""
        objects = list(filter(lambda x: isinstance(x, Tile) and int(x.type) not in behind_id, self.block_group.sprites()))

        old_y = self.rect.y

        if axis == 'y':
            self.rect.y += int(value)
            if any([pygame.sprite.collide_mask(self, i) for i in objects]):
                if get:
                    return [i for i in objects if pygame.sprite.collide_mask(self, i)][0]
                self.rect.y = int(old_y)
                return False

        if axis == 'x':
            old_x = self.rect.x
            old_y = self.rect.y
            self.rect.x += int(value)
            self.rect.y -= 10
            if any([pygame.sprite.collide_mask(self, i) for i in objects]):
                self.rect.x = int(old_x)
                self.rect.y = old_y
                return False
            self.rect.y = old_y

        return True

    def attack(self, npc_group):
        """Пытаемся атаковать NPC, если близко"""
        for npc in npc_group.sprites():
            if npc.status == 'dying':
                continue
            distance = math.hypot(npc.rect.x - self.rect.x, npc.rect.y - self.rect.y)
            if distance <= 100:
                npc.hp -= self.power
                sound_fight()
                if self.hp + 10 >= 100:
                    self.hp += 100 - self.hp
                else:
                    self.hp += 10
                npc.status = 'damage'
                if npc.hp <= 0:
                    return True

    def health(self, value):
        """Изменяем здоровье"""
        self.hp += value

    def show_hp(self, screen):
        """Показываем здоровье"""
        hp_to_show = self.hp // 10
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x + 32, self.rect.y + 10, 60, 10))
        pygame.draw.rect(screen, (76, 187, 23), (self.rect.x + 37, self.rect.y + 12, 5 * hp_to_show, 6))

    def allow_sound_step(self):
        """Включаем звук шага"""
        self.sound_step_can_play = True

    @staticmethod
    def get_difficult():
        """Получаем сложность игры"""
        with open('resource/settings.json', 'r') as obj:
            data = json.load(obj)

        return int(data['difficult'])
