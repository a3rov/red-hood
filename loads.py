import pygame
import os
import sys

screen = pygame.display


def final_of_image(image, size, colorkey=None):
    """Идет финальное преобразование картинки"""
    image = pygame.transform.scale(image, size)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_image(name, coords, multi=1):
    """Здесь открывается картинка и вытаскивается по нужным строкам и столбцам
    Условием что размер картинки при делении на любой из параметров в остатке оставляет 0"""
    fullname = os.path.join('resource/img/', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    start = coords[0]
    size = coords[1]

    image = pygame.image.load(fullname)

    start_x = start[0]
    start_y = start[1]
    end_x = size[0]
    end_y = size[1]

    cropped_image = image.subsurface(pygame.Rect(start_x, start_y, end_x, end_y))

    return final_of_image(cropped_image, (cropped_image.get_width() * multi, cropped_image.get_height() * multi))


