import pygame

pygame.init()

pygame.mixer.init()

# Создаем каналы со звуками
channel = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
channel3 = pygame.mixer.Channel(2)
channel4 = pygame.mixer.Channel(3)

# Загружаем звуки
step = pygame.mixer.Sound("resource/sounds/step.wav")
hit = pygame.mixer.Sound("resource/sounds/hit.wav")
died = pygame.mixer.Sound("resource/sounds/died.wav")
start = pygame.mixer.Sound("resource/sounds/start.wav")
tap = pygame.mixer.Sound("resource/sounds/tap.wav")
start_level = pygame.mixer.Sound("resource/sounds/start_level.wav")
end = pygame.mixer.Sound("resource/sounds/end.wav")
background = pygame.mixer.Sound("resource/sounds/background.wav")

# В функциях играем звуки


def sound_step():
    channel.play(step)


def sound_fight():
    channel2.play(hit)


def sound_died():
    channel2.play(died)


def sound_start():
    channel3.play(start)


def sound_tap():
    channel3.play(tap)


def sound_start_level():
    channel3.play(start_level)


def sound_end():
    channel3.play(end)


def sound_background():
    channel4.play(background)


def stop_sounds():
    """Останавливаем все звуки"""
    channel3.stop()
    channel.stop()
    channel2.stop()
    channel4.stop()
