import pygame


class CloseAnim(pygame.sprite.Sprite):
    def __init__(self, status='close', label=None):
        """Создаем анимацию для закрытия/открытия экрана"""
        super().__init__()

        self.status = status
        self.complete = 1
        if status == 'show':
            self.lines = ([0, 0, 1920, 216, 0], [0, 216, 1920, 216, 0],
                          [0, 432, 1920, 216, 0], [0, 648, 1920, 216, 0], [0, 864, 1920, 216, 0])

        else:
            self.lines = ([1920, 0, 1920, 216, 0], [-1920, 216, 1920, 216, 0],
                          [1920, 432, 1920, 216, 0], [-1920, 648, 1920, 216, 0], [1920, 864, 1920, 216, 0])

        self.speed_rect = 0
        self.speed = [100, 100, 100, 100, 100, 75, 75, 75, 75, 75, 75, 50, 50, 50, 50, 50, 50, 50, 50,
                      30, 30, 30, 30, 30, 30, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 10, 10, 10, 10, 10, 10, 10, 10,
                      10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

        self.label = label

    def show(self, screen):
        """Генерируем анимацию"""
        if self.status == 'show' and self.complete != 1:
            self.speed_rect -= 2
            if self.lines[0][0] != 0:
                self.lines[0][0] -= self.speed[self.speed_rect]

            if self.lines[1][0] != 0:
                self.lines[1][0] += self.speed[self.speed_rect]

            if self.lines[2][0] != 0:
                self.lines[2][0] -= self.speed[self.speed_rect]

            if self.lines[3][0] != 0:
                self.lines[3][0] += self.speed[self.speed_rect]

            if self.lines[4][0] != 0:
                self.lines[4][0] -= self.speed[self.speed_rect]
            else:
                self.complete = 1
                self.speed_rect = 0

            self.speed_rect += 1

        if self.status == 'close' and self.complete != 1:
            if self.lines[0][0] != 1920:
                self.lines[0][0] += self.speed[self.speed_rect]

            if self.lines[1][0] != -1920:
                self.lines[1][0] -= self.speed[self.speed_rect]

            if self.lines[2][0] != 1920:
                self.lines[2][0] += self.speed[self.speed_rect]

            if self.lines[3][0] != -1920:
                self.lines[3][0] -= self.speed[self.speed_rect]

            if self.lines[4][0] != -1920:
                self.lines[4][0] += self.speed[self.speed_rect]
            else:
                self.complete = 1
                self.speed_rect = 0
                self.lines = ([1920, 0, 1920, 216, 0], [-1920, 216, 1920, 216, 0],
                              [1920, 432, 1920, 216, 0], [-1920, 648, 1920, 216, 0])

            self.speed_rect += 1
            if self.speed_rect == len(self.speed) - 1:
                self.speed_rect -= 1

        for i in self.lines:
            pygame.draw.rect(screen, (0, 0, 0), (i[0], i[1], i[2], i[3]))

        if self.label is not None:
            self.label.generate()

    def change(self):
        """Меняем статус открытия или закрытия"""
        if self.status == 'show':
            self.status = 'close'
        else:
            self.status = 'show'

        self.complete = 0
