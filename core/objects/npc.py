import json
import math
import threading

import pygame

from core.objects.tile import Tile
from core.world import physic
from loads import load_image

# Определяем константы
GRAVITY = physic.GRAVITY
JUMP_COUNT_CONSTATE = 13

# Кадры для NPC
frames = {
    'default': (('npc_default.png', ((0, 0), (32, 32)), 4),
                ('npc_default.png', ((32, 0), (32, 32)), 4),
                ('npc_default.png', ((64, 0), (32, 32)), 4),
                ('npc_default.png', ((96, 0), (32, 32)), 4),
                ('npc_default.png', ((128, 0), (32, 32)), 4),
                ('npc_default.png', ((160, 0), (32, 32)), 4)),

    'walking': [('npc_walking.png', ((0, 0), (32, 32)), 4),
                ('npc_walking.png', ((32, 0), (32, 32)), 4),
                ('npc_walking.png', ((64, 0), (32, 32)), 4),
                ('npc_walking.png', ((96, 0), (32, 32)), 4),
                ('npc_walking.png', ((128, 0), (32, 32)), 4),
                ('npc_walking.png', ((160, 0), (32, 32)), 4),
                ('npc_walking.png', ((192, 0), (32, 32)), 4),
                ('npc_walking.png', ((224, 0), (32, 32)), 4)],

    'dying': [('npc_dying.png', ((0, 0), (32, 32)), 4),
              ('npc_dying.png', ((32, 0), (32, 32)), 4),
              ('npc_dying.png', ((64, 0), (32, 32)), 4),
              ('npc_dying.png', ((96, 0), (32, 32)), 4),
              ('npc_dying.png', ((128, 0), (32, 32)), 4),
              ('npc_dying.png', ((160, 0), (32, 32)), 4),
              ('npc_dying.png', ((192, 0), (32, 32)), 4),
              ('npc_dying.png', ((224, 0), (32, 32)), 4),
              ('npc_dying.png', ((256, 0), (32, 32)), 4)]
}

# ID Tile'ов, которые не будут иметь колизию с персонажем
behind_id = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 8]


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weapon, all_sprites, block_group, particle_group, *groups):
        """Создаем NPC для работы с ним, передаем в него координаты, оружие, группы"""
        super().__init__(*groups)

        # Создаем нужные группы
        self.all_sprites = all_sprites
        self.block_group = block_group
        self.particle_group = particle_group

        self.image = None
        # создаем статус персонажа и задержку на выстрел
        self.delay = 0
        self.status = 'default'

        # Создаем персонажу все картинки для кадровых анимация
        self.frames = dict()
        self.frames['default'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['default']]
        self.frames['walking'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['walking']]
        self.frames['jumping'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['walking']]
        self.frames['falling'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['default']]
        self.frames['damage'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['default']]
        self.frames['dying'] = [load_image(i[0], i[1], multi=i[2]) for i in frames['dying']]

        # создаем нужные параметры для анимации персонажа
        self.cur_frame = 0
        self.image = self.frames[self.status][self.cur_frame]
        self.need_iteration = 5

        # создаем surface для NPC
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.surf = self.image

        # Создаем параметры для прыжка
        self.pos_y = pos_y
        self.speed_y = 0
        self.jump_count = JUMP_COUNT_CONSTATE

        # создаем маску NPC
        self.mask = pygame.mask.from_surface(self.surf)

        # Создаем оружие (в разработке), скорость, количество здоровья
        self.speed = 4
        self.weapon = weapon
        self.hp = 100

        self.iteration = 5

        # Создаем в какую сторону изначально смотрит персонажа, скорость падения, скорость перемещения при уроне
        self.side = 'right'
        self.fall_speed = 5
        self.speed_from_damage = 0

        # создаем переменную куда идти и силу NPC
        self.walk_to = 0
        self.power = 33

        if self.get_difficult() == 1:
            self.power = 25

        if self.get_difficult() == 2:
            self.power = 45

        if self.get_difficult() == 3:
            self.power = 70

    def changepos(self):
        """Метод для передвижения персонажа"""
        if self.walk_to == 0:
            self.check_status('default')
        else:
            self.check_status('walking')
            if self.walk_to < self.rect.x:
                if not self.try_move('x', -self.speed):
                    pass
            elif self.walk_to > self.rect.x:
                if not self.try_move('x', self.speed):
                    pass

    def check_shoot(self):
        """Метод проверки возможности стрелять, если ее нет, то включаем эту возможность"""
        if self.delay == 1000:
            self.delay = 0

    def update(self, player, kills):
        """Метод обновления NPC"""

        if self.hp <= 0:
            # проверка здоровья
            self.status = 'dying'

        # Смена кадра
        if self.iteration == self.need_iteration:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.status])
            self.surf = self.frames[self.status][self.cur_frame]
            self.iteration = 0
            if self.side == 'left':
                self.surf = pygame.transform.flip(self.surf, True, False)

            # если статус погибания и последний кадр, то NPC удаляется
            if self.cur_frame == 8 and self.status == 'dying':
                self.kill()

        # Если получил урон, то NPC передвигается
        if self.status == 'damage':
            damage_x = [3, 4, 5, 9, 13, 15, 14, 12, 10, 9, 5]
            damage_y = [1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
            if self.speed_from_damage == 10:
                self.status = 'default'
                self.speed_from_damage = 0
                return

            if self.side == 'right':
                self.try_move('x', -damage_x[self.speed_from_damage])
            else:
                self.try_move('x', damage_x[self.speed_from_damage])

            self.try_move('y', -damage_y[self.speed_from_damage])

            self.speed_from_damage += 1
            return

        # проверка соприкосания с другими Tile, если да, то персонаж падает
        if (not any([False if j is None else True for j in
                     [pygame.sprite.collide_mask(self, i) for i in
                      list(filter(lambda x: isinstance(x, Tile) and int(x.type) not in behind_id,
                                  self.block_group.sprites()))]]) and self.status != 'jumping'):
            self.check_status('falling')

        # если статус падения, то перемещаем персонажа
        if self.status == 'falling':
            self.speed_y += GRAVITY
            if not self.try_move('y', self.speed_y):
                y = self.try_move('y', self.speed_y, True).rect.y - 105
                self.rect.y = y
                self.status = 'default'
                self.speed_y = 0

            self.rect.y += int(self.speed_y)

            if self.speed_y > 10:
                self.hp -= 30

        # если статус смерти, то все остальные действия пропускаются при помощи return
        if self.status == 'dying':
            self.iteration += 1
            return

        # если статус jumping, то выполняем прыжок
        elif self.status == 'jumping':
            if self.jump_count >= -JUMP_COUNT_CONSTATE:
                if self.jump_count > 0:
                    self.rect.y -= int((self.jump_count ** 2) // 5)
                else:
                    self.jump_count = JUMP_COUNT_CONSTATE
                    self.status = 'default'

                self.jump_count -= 1

        # если у игрок жив, то вычесляем расстояние до него
        if not player.hp <= 0:
            player_distance = math.hypot(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            if player_distance <= 800:
                # поворачаем NPC в сторону игрока
                if player.rect.x < self.rect.x:
                    self.side = 'left'

                else:
                    self.side = 'right'

            # атакуем игрока, если расстояние подходящее
            if player_distance <= 10 and self.delay == 0:
                self.attack(player)

            # идем к игроку, если Y примерно одинаковый
            if 20 > self.rect.y - player.rect.y > -20:
                self.walk_to = player.rect.x

            else:
                self.walk_to = 0

        # выполняем смещение, если оно требуется
        self.changepos()

        self.iteration += 1

    def check_status(self, status):
        """Проверяем статус и при подходящих условиях заменяем"""
        if self.status == 'dying' or self.status == 'falling' or self.status == 'jumping':
            return False
        if self.status != status:
            self.status = status
            self.cur_frame = 0
            return self.status

    def try_move(self, axis, value, get=False):
        """Пытаемся переместиться, если возможно"""
        objects = list(
            filter(lambda x: isinstance(x, Tile) and int(x.type) not in behind_id, self.block_group.sprites()))

        old_y = self.rect.y

        # если ось Y, то пробуем переместить NPC
        if axis == 'y':
            self.rect.y += int(value)
            if any([pygame.sprite.collide_mask(self, i) for i in objects]):
                if get:
                    return [i for i in objects if pygame.sprite.collide_mask(self, i)][0]

                self.rect.y = int(old_y)
                return False

        # если ось X, то пробуем переместить NPC
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

    def health(self, value):
        """Метод для изменения здоровья"""
        self.hp += value

    def attack(self, player):
        """Метод атаки игрока, если возможно"""
        self.delay = 1000
        player.hp -= self.power
        player.status = 'damage'
        threading.Timer(1, self.check_shoot).start()

    def show_hp(self, screen):
        """Показываем Здоровье"""
        hp_to_show = self.hp // 10
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x + 32, self.rect.y + 10, 60, 10))
        pygame.draw.rect(screen, (176, 0, 0), (self.rect.x + 37, self.rect.y + 12, 5 * hp_to_show, 6))

    @staticmethod
    def get_difficult():
        """Получаем сложность игры"""
        with open('resource/settings.json', 'r') as obj:
            data = json.load(obj)

        return int(data['difficult'])

