import pygame
import os
import sys

FPS = 30

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 700
    screen = pygame.display.set_mode(size)
    running = True
    cloak = pygame.time.Clock()

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    def draw_board():
        boar_image = load_image('Board.png')
        screen.blit(boar_image, (1, 1))

    def draw_ball():
        ball_sprite_grup = pygame.sprite.Group()
        ball_sprite = pygame.sprite.Sprite()
        ball_sprite.image = load_image("Ball.png")
        ball_sprite.rect = ball_sprite.image.get_rect()
        for x in range(3):
            for y in range(2):
                ball_sprite.rect.x = 388 + x * 83
                ball_sprite.rect.y = 53 + y * 84
                ball_sprite_grup.add(ball_sprite)
                ball_sprite_grup.draw(screen)
        for x in range(7):
            for y in range(3):
                ball_sprite.rect.x = 217 + x * 84.7
                ball_sprite.rect.y = 224 + y * 82.5
                ball_sprite_grup.add(ball_sprite)
                ball_sprite_grup.draw(screen)

    while running:
        cloak.tick(FPS)
        pygame.display.flip()
        draw_board()
        draw_ball()
    pygame.quit()
