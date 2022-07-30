import time
from random import randint
from sys import exit

import pygame

pygame.init()

screen = pygame.display.set_mode((1020, 670))
pygame.display.set_caption('Flappy Duck')
BG = pygame.image.load('Images/Background.png').convert_alpha()
clock = pygame.time.Clock()

score = 0
score_text = pygame.font.Font("C:/Windows/Fonts/impact.ttf", 25)
gravity = 0
d = 0
x = 0
# passed = 0


class Sprite:
    def __init__(self, name: str):
        self.surface = pygame.image.load(f'Images/{name}').convert_alpha()


class Bird(Sprite):
    def __init__(self):
        super().__init__('bird.png')
        self.rect = self.surface.get_rect(center=(50, 335))


class Pipe(Sprite):
    speed: int = 3

    def __init__(self, name):
        super().__init__(name)
        self.x = 1080


class PipeUp(Pipe):
    def __init__(self, name):
        super().__init__(name)
        self.y = 90
        self.rect = self.surface.get_rect(midbottom=(self.x, self.y))


class PipeDown(Pipe):
    def __init__(self, name):
        self.y = 290
        super().__init__(name)
        self.rect = self.surface.get_rect(midtop=(self.x, self.y))


bird = Bird()
pipe_up = PipeUp('pipeUp.png')
pipe_down = PipeDown('pipeDown.png')

start = False
running = True

if __name__ == '__main__':
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    gravity = 14
                    d = 1

        text_surf = score_text.render(f'Score: {score}', False, '#d3f5f5', '#26d1d1')
        text_rect = text_surf.get_rect(midtop=(510, 0))

        screen.blit(BG, (0, 0))
        screen.blit(bird.surface, bird.rect)
        screen.blit(pipe_up.surface, pipe_up.rect)
        screen.blit(pipe_down.surface, pipe_down.rect)
        screen.blit(text_surf, text_rect)

        bird.rect.y -= gravity
        gravity -= d

        # For when in area of middle of pipes
        if pipe_up.rect.left + 100 < bird.rect.centerx < pipe_up.rect.right:
            for i in range(22):
                if i == 20:
                    score += 1

                    rand_x = randint(890, 1280)
                    rand_top = randint(10, 650)
                    rand_bott = randint(10, 650)

                    # Invalid  * Overlapping sprites*,     *Too tight*   must be "re-rolled"
                    while not rand_top < rand_bott or not (rand_bott - rand_top) > 165:
                        rand_top = randint(10, 650)
                        rand_bott = randint(10, 650)

                    pipe_up.rect.midbottom = (rand_x, rand_top)
                    pipe_down.rect.midtop = (rand_x, rand_bott)
                else:
                    continue

        if start:
            pipe_up.rect.left -= pipe_up.speed
            pipe_down.rect.left -= pipe_down.speed

        if score in range(5, 201, 5):
            Pipe.speed += .009

        if_floor = bird.rect.y > 700
        if_ceiling = bird.rect.y < -30

        if bird.rect.colliderect(pipe_up.rect) or bird.rect.colliderect(pipe_down.rect) or if_floor or if_ceiling:
            Game_over = pygame.font.Font("C:/Windows/Fonts/impact.ttf", 50)

            Game_Over_surf = Game_over.render(r'Game over.', False, '#d62f2f')
            Game_Over_rect = Game_Over_surf.get_rect(center=(510, 305))

            Score_sayer = Game_over.render(f'You got {score} points.', False, '#d62f2f')
            Score_sayer_rect = Score_sayer.get_rect(center=(510, 375))

            screen.blit(Game_Over_surf, Game_Over_rect)
            screen.blit(Score_sayer, Score_sayer_rect)

            pygame.display.update()

            time.sleep(2)
            pygame.quit()
            exit()

        clock.tick(60)
        pygame.display.update()
