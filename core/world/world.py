import json
import random
import threading

import pygame

from core.objects.npc import NPC
from core.objects.player import Player
from core.objects.sky import Sky
from core.objects.sound import sound_start, sound_start_level, sound_end, sound_background
from core.objects.tile import Tile
from core.ui.frame_animation import CloseAnim
from core.ui.kills_ui import KillsUI
from core.ui.label import Label
from core.ui.signboard import Signboard
from core.world.camera import Camera
from core import sql

# from core.objects.particle import Particle

clock = pygame.time.Clock()

tips = ['Держите дистанцию с врагами, чтобы не потерять здоровье',
        'Здоровье восстанавливается после победой над врагом',
        'Сложность игры можно изменить в настройках',
        'Стоит попробовать еще раз..',
        'У тебя все получится, попробуй еще!']

tips_win = ['Отличная победа! Заслужена!',
            'Уровень пройден. Отлично!']


class World:
    def __init__(self, screen, width, height, level='LEVEL 1'):
        """Объявляем параметры мира и экрана"""
        pygame.init()

        self.screen = screen
        self.width, self.height = width, height

        self.all_sprites = pygame.sprite.Group()
        self.blocks_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        self.signboard_group = pygame.sprite.Group()
        self.label_group = pygame.sprite.Group()

        self.sky = Sky(self.screen)
        self.sky2 = Sky(self.screen)
        self.sky2.sky_x += 1920

        self.level = level
        self.levels = {}

        with open('resource/levels.json') as json_file:
            self.levels = json.load(json_file)

        self.load_level(self.level)
        self.status = 'game'
        self.close_game_now = False

        self.player = Player(960, 480, 'fist', self.all_sprites, self.blocks_group, self.particle_group,
                             self.all_sprites)

        self.kills_need = 0
        self.load_npc(self.level)
        self.camera = Camera(self.screen)

        self.kills = KillsUI(self.kills_need, self.screen)
        self.closeAnim = CloseAnim(status='show')
        self.closeAnim.change()

        self.is_stop: bool = False
        pygame.mouse.set_visible(False)

        threading.Timer(1.5, self.show_start_text).start()

        self.closeAnim_final = CloseAnim()

        self.already_stop = False
        self.end_label = None
        sound_start_level()
        sound_background()

    def load_level(self, level):
        """Загружаем объекты уровня"""
        for i in self.levels[level]['obj']:
            if i[0] != '9':
                if i[3] == 'default':
                    Tile(i[0], i[1], i[2], self.all_sprites, self.blocks_group, rotate=i[4])
                elif i[3] == 'behind':
                    Tile(i[0], i[1], i[2], self.all_sprites, rotate=i[4])

    def load_npc(self, level):
        """Загружаем все NPC"""
        count = 0
        for i in self.levels[level]['obj']:
            if i[0] == '9':
                count += 1
                NPC(i[1], i[2], 'fist', self.all_sprites, self.blocks_group, self.particle_group, self.all_sprites,
                    self.npc_group)
        self.kills_need = count

    def tickuptade(self):
        """Обновляем все события в мире, игрока, кнопки, тексты, нпс, объекты, камера"""
        if self.close_game_now:
            return 'end'

        if self.is_stop:
            self.closeAnim_final.show(self.screen)

            for signboard in self.signboard_group.sprites():
                signboard.generate()

            for label in self.label_group.sprites():
                label.generate()

        pressed = list(pygame.key.get_pressed())

        if True in pressed and self.is_stop:
            pressed = list(pygame.key.get_pressed())
            pressed_keys = [i for i in range(len(pressed)) if pressed[i] is True]

            if 21 in pressed_keys and self.status == 'lose':
                self.end_label.kill()
                self.restart_level()

            if 9 in pressed_keys and (self.status == 'lose' or self.status == 'win') and not self.already_stop:
                if self.status == 'win':
                    sql.open_next_level()
                self.closeAnim_final.change()
                self.end_label.kill()
                sound_start()
                threading.Timer(8, self.close_game).start()
                for obj in self.label_group:
                    obj.kill()
                threading.Timer(1, self.levellabel).start()
                threading.Timer(0, self.clear_level).start()
                self.already_stop = True

        if self.is_stop:
            pygame.display.flip()
            clock.tick(60)
            return

        self.sky.skyfill()
        pressed = list(pygame.key.get_pressed())
        mouse_pressed = pygame.mouse.get_pressed()

        if True in pressed:
            # Обработка передвижения персонажа
            pressed = list(pygame.key.get_pressed())
            pressed_keys = [i for i in range(len(pressed)) if pressed[i] is True]

            if 79 in pressed_keys or 7 in pressed_keys:
                self.player.changepos('x', self.player.speed)
            if 80 in pressed_keys or 4 in pressed_keys:
                self.player.changepos('x', -self.player.speed)

            if self.player.status == 'walking' or self.player.status == 'default':
                if 82 in pressed_keys or 26 in pressed_keys:
                    self.player.check_status('jumping')
        else:
            self.player.check_status('default')

        for obj in self.all_sprites:
            if not isinstance(obj, KillsUI) and not isinstance(obj, Label) and not isinstance(obj, Signboard):
                self.screen.blit(obj.surf, obj.rect)
                self.camera.apply(obj)

        if mouse_pressed[0] is True:
            if self.player.delay_fight == 0:
                self.player.delay_fight = 300
                threading.Timer(0.4, self.player.check_shoot).start()
                if self.player.attack(self.npc_group):

                    if self.kills.kills + 1 == self.kills.maxkills:
                        sound_end()
                        threading.Timer(1, self.stop_game).start()
                        self.end_game_ui('win')
                    self.kills.kills += 1

        self.player.update()
        self.player.show_hp(self.screen)

        if self.player.hp <= 0:
            sound_end()
            threading.Timer(1, self.stop_game).start()
            self.end_game_ui('lose')

        self.camera.update(self.player)

        for npc in self.npc_group:
            npc.update(self.player, self.kills.kills)
            npc.show_hp(self.screen)
            if npc.hp <= 0 and npc.status != 'dying':
                npc.kill()
                self.kills.kills += 1

        for particle in self.particle_group:
            particle.update()

        self.kills.generate()
        self.closeAnim.show(self.screen)

        for signboard in self.signboard_group.sprites():
            signboard.generate()

        for label in self.label_group.sprites():
            label.generate()

        pygame.display.flip()
        clock.tick(60)

    def stop_game(self):
        """Останавливаем игру"""
        self.is_stop: bool = True

    def end_game_ui(self, type_event):
        """Создаем объекты для завершения игры"""
        if type_event == 'win':
            self.end_label = Label((800, 250), 'VICTORY', self.screen,
                                   self.label_group, self.all_sprites, size=64)

            Signboard((0, 800), (500, 40), 'Уровень пройден, нажми F', self.screen,
                      self.signboard_group, self.all_sprites)
            self.status = 'win'

        if type_event == 'lose':
            self.end_label = Label((800, 250), 'DEFEAT', self.screen,
                                   self.label_group, self.all_sprites, size=64)

            Signboard((0, 800), (500, 40), 'нажмите R для перезапуска уровня', self.screen,
                      self.signboard_group, self.all_sprites)
            self.status = 'lose'

    def restart_level(self):
        """Восстанавливаем уровень и начинаем все заново"""
        [i.kill() for i in self.all_sprites]
        self.load_level(self.level)
        self.status = 'game'
        self.end_label.kill()
        self.kills_need = 0
        self.load_npc(self.level)
        self.player = Player(960, 480, 'fist', self.all_sprites, self.blocks_group, self.particle_group,
                             self.all_sprites)

        self.kills = KillsUI(self.kills_need, self.screen)
        self.is_stop: bool = False
        sound_start_level()

    def show_start_text(self):
        """Показываем начальный текст"""
        Label((800, 250), str(self.level), self.screen,
              self.label_group, self.all_sprites, step=2.5, type='kill', size=64)

    def close_game(self):
        """Закрываем игру"""
        self.close_game_now = True

    def levellabel(self):
        """Генерируем текст для перехода в меню"""
        tip = random.choice(tips)
        if self.status == 'win':
            tip = random.choice(tips_win)
        label = Label((1920 // 2 - 150, 1080 // 2 - 100), tip, self.screen, self.label_group)
        self.closeAnim.label = label

    def clear_level(self):
        """Очищаем уровень"""
        for sprite in self.all_sprites:
            if not isinstance(sprite, Player) and not isinstance(sprite, Label):
                sprite.kill()
