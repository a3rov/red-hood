import random
import json

import pygame

from core.ui.invise_button import InviseButton
from core.ui.button import Button
from core.ui.label import Label
from core.ui.image import Image
from core.objects.sky import Sky
from core.ui.frame_animation import CloseAnim
from core.objects.sound import sound_start, sound_tap, stop_sounds
from core import sql

import threading

clock = pygame.time.Clock()
pygame.init()

tips = ['Держите дистанцию с врагами, чтобы не потерять здоровье',
        'Здоровье восстанавливается после победой над врагом',
        'Сложность игры можно изменить в настройках',
        'Факт: Основатель игры - ученик Yandex Lyceum']


class Menu:
    def __init__(self, screen, width, height):
        """Создаем все меню"""
        self.status = 'menu'

        self.menu_sprites = pygame.sprite.Group()
        self.settings_sprites = pygame.sprite.Group()
        self.levels_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.screen = screen
        self.width, self.height = width, height

        self.sky = Sky(self.screen)
        self.sky2 = Sky(self.screen)
        self.sky2.sky_x += 1920

        pygame.mouse.set_visible(True)

        self.mouse_click_can = True

        self.create_ui(self.status)

        self.closeAnim = CloseAnim()

        self.allow_close = 0
        self.event = None

        self.closeAnim2 = CloseAnim(status='show')
        self.closeAnim2.change()
        stop_sounds()

    def tickuptade(self):
        """Обновляем меню"""
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] is True:
            event = self.click_event(pygame.mouse.get_pos())
            if event == 'exit' or (event is not None and 'LEVEL' in event):
                if event == 'exit':
                    return 'exit'
                self.event = event
                threading.Timer(6, self.start_game).start()

        if self.allow_close == 1:
            return self.event

        self.sky.skyfill()

        if self.status == 'menu':
            self.show_menu()

        if self.status == 'settings':
            self.show_settings()

        if self.status == 'levels':
            self.show_levels()

        self.closeAnim.show(self.screen)
        self.closeAnim2.show(self.screen)

        pygame.display.flip()
        clock.tick(60)

    def show_menu(self):
        "Генерируем меню"
        for sprite in self.menu_sprites:
            sprite.generate()

    def show_settings(self):
        """Генерируем настройки"""
        for sprite in self.settings_sprites:
            sprite.generate()

    def show_levels(self):
        """Генерируем уровни"""
        for sprite in self.levels_sprites:
            sprite.generate()

    def click_event(self, coords):
        """Проверяем событие клика мышкой"""
        if self.mouse_click_can is True:
            self.mouse_click_can = False
            group = [i for i in self.get_group() if isinstance(i, InviseButton) or isinstance(i, Button)]
            callback = [i.callback for i in group if i.check_pressed(coords)]
            if len(callback) != 0:
                threading.Timer(0.5, self.mouse_allow).start()
                return self.callback_event(callback[0])
            else:
                threading.Timer(0.5, self.mouse_allow).start()

    def callback_event(self, callback):
        """Обработка событий, если кнопка нажата"""
        sound_tap()
        if callback == 'settings':
            self.create_ui('settings')

        if callback == 'play':
            self.create_ui('levels')

        if callback == 'back':
            self.create_ui('menu')

        if callback == 'exit':
            return 'exit'

        if callback == '1':
            self.set_difficult(1)
            self.all_buttons_switch_color()
            self.settings_1.color = (44, 130, 136)

        if callback == '2':
            self.set_difficult(2)
            self.all_buttons_switch_color()
            self.settings_2.color = (44, 130, 136)

        if callback == '3':
            self.set_difficult(3)
            self.all_buttons_switch_color()
            self.settings_3.color = (44, 130, 136)

        if 'LEVEL' in callback:
            if sql.can_level(int(callback.split()[-1])):
                self.closeAnim.change()
                threading.Timer(8, self.closeAnim.change).start()
                threading.Timer(1, self.levelLabel).start()
                sound_start()
                return callback

    def create_ui(self, type):
        """Создаем UI для нужной группы"""
        if type == 'menu':
            Image((0, 0), 'menu_background', self.screen, self.menu_sprites,
                  multi=3.4)

            Button((200, 500), (200, 50), 'Играть', self.screen, self.menu_sprites, callback='play')
            Button((200, 570), (200, 50), 'Настройки', self.screen, self.menu_sprites, callback='settings')
            Button((200, 640), (200, 50), 'Выход', self.screen, self.menu_sprites, callback='exit')

            Label((400, 200), 'RedHood', self.screen, self.menu_sprites, size=256)

        if type == 'settings':
            Image((0, 0), 'settings_background', self.screen, self.settings_sprites,
                  multi=3.4)

            Label((830, 470), 'Уровень сложности игры', self.screen, self.settings_sprites, type='Once', alpha=255)
            InviseButton((300, 420), (310, 110), 'Основные', self.screen, self.settings_sprites, callback='main_settings')
            InviseButton((300, 600), (310, 110), 'В разработке..', self.screen, self.settings_sprites, callback='sound_settings')
            InviseButton((300, 770), (310, 110), 'В разработке..', self.screen, self.settings_sprites, callback='info')
            InviseButton((1050, 350), (220, 55), '', self.screen, self.settings_sprites, callback='back')

            self.settings_3 = Button((700, 500), (100, 50), '3', self.screen, self.settings_sprites, callback='3',
                   color=(33, 80, 94))
            self.settings_2 = Button((820, 500), (100, 50), '2', self.screen, self.settings_sprites, callback='2',
                   color=(33, 80, 94))
            self.settings_1 = Button((940, 500), (100, 50), '1', self.screen, self.settings_sprites, callback='1',
                   color=(33, 80, 94))

            if self.get_difficult() == str(1):
                self.all_buttons_switch_color()
                self.settings_1.color = (44, 130, 136)

            if self.get_difficult() == str(2):
                self.all_buttons_switch_color()
                self.settings_2.color = (44, 130, 136)

            if self.get_difficult() == str(3):
                self.all_buttons_switch_color()
                self.settings_3.color = (44, 130, 136)

        if type == 'levels':
            Image((0, 0), 'play_background', self.screen, self.levels_sprites,
                  multi=3.4)

            InviseButton((295, 555), (175, 100), '', self.screen, self.levels_sprites, callback='LEVEL 1')
            InviseButton((635, 525), (175, 100), '', self.screen, self.levels_sprites, callback='LEVEL 2')
            InviseButton((920, 585), (175, 100), '', self.screen, self.levels_sprites, callback='LEVEL 3')
            InviseButton((1200, 550), (175, 100), '', self.screen, self.levels_sprites, callback='LEVEL 4')
            InviseButton((105, 460), (150, 55), '', self.screen, self.levels_sprites, callback='back')

        self.status = type

    def get_group(self):
        """Получаем текущую группу"""
        if self.status == 'menu':
            return self.menu_sprites

        if self.status == 'settings':
            return self.settings_sprites

        return self.levels_sprites

    def mouse_allow(self):
        """Проверяем возможность клика мышки"""
        if self.mouse_click_can is False:
            self.mouse_click_can = True

    def levelLabel(self):
        """Запускаем уровень в сопровождении TIP"""
        tip = random.choice(tips)
        label = Label((1920 // 2 - 150, 1080 // 2 - 100), tip, self.screen, self.levels_sprites)
        self.closeAnim.label = label

    def start_game(self):
        """Начинаем игру и разрешаем закрыть меню"""
        self.allow_close = 1

    @staticmethod
    def get_difficult():
        """Получаем сложность игры"""
        with open('resource/settings.json', 'r') as obj:
            data = json.load(obj)

        return data['difficult']

    def all_buttons_switch_color(self):
        """Меняем цвета кнопок в настройках"""
        self.settings_1.color = (33, 80, 94)
        self.settings_2.color = (33, 80, 94)
        self.settings_3.color = (33, 80, 94)

    @staticmethod
    def set_difficult(num):
        """Устанавливаем сложность"""
        with open('resource/settings.json', 'r') as obj:
            data = json.load(obj)

        with open('resource/settings.json', 'w') as obj:
            data['difficult'] = str(num)
            json.dump(data, obj)

