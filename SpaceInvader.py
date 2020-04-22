import pygame as pg
from random import randint
from pygame import mixer

try:
    pg.init()
except:
    print("PyGame wasn't initialized!")
    
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 800
HEIGHT = 600


class Player(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pg.image.load("spaceship.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 370
        self.rect.y = 480

    def update(self):
        self.rect.x += player_speed
        if self.rect.x > 735:
            self.rect.x = 735
        elif self.rect.x < 5:
            self.rect.x = 5


class Enemy(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pg.image.load("space-invaders.png").convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randint(5, 735)
        self.rect.y = randint(20, 100)


class Bullet(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pg.image.load('bullet.png').convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = -30
        self.rect.y = 480

    def update(self):
        global bullet_state
        if bullet_state:
            self.rect.y -= bulletY_change
        if self.rect.y <= 0:
            self.rect.x = -30
            self.rect.y = 480
            bullet_state = False


screen = pg.display.set_mode((WIDTH, HEIGHT))
background = pg.image.load('background.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)
pg.display.set_caption("Space Invader")
icon = pg.image.load('ufo.png')
pg.display.set_icon(icon)

# Spaceship
player = Player()
player_group = pg.sprite.Group()
player_group.add(player)
player_speed = 0

# Enemy
num_enemies = 5
enemy_change_x = []
enemy_group = pg.sprite.Group()
for i in range(0, num_enemies):
    enemy = Enemy()
    enemy_group.add(enemy)
    enemy_change_x.append(3)
enemies = pg.sprite.Group.sprites(enemy_group)
enemy_change_y = 40
new_enemy = True

# Bullet
bullet = Bullet()
bullet_group = pg.sprite.Group()
bullet_group.add(bullet)
bulletY_change = 5
bullet_state = False
bullet_sound = mixer.Sound('laser.wav')
collision_sound = mixer.Sound('explosion.wav')

# Score
points = int(0)
font = pg.font.Font("freesansbold.ttf", 32)

# Game Over
over = pg.font.Font("freesansbold.ttf", 64)
still_play = pg.font.Font("freesansbold.ttf", 32)
yes = pg.font.Font("freesansbold.ttf", 25)
no = pg.font.Font("freesansbold.ttf", 25)


def game_over():
    over_text = over.render("GAME OVER", True, WHITE)
    still_play_text = still_play.render("Do you want to play again?", True, WHITE)
    yes_text = yes.render("Yes", True, WHITE)
    no_text = no.render("No", True, WHITE)
    screen.blit(over_text, (200, 250))
    screen.blit(still_play_text, (190, 320))
    pg.draw.rect(screen, BLACK, (290, 380, 60, 40))
    pg.draw.rect(screen, BLACK, (440, 380, 50, 40))
    screen.blit(yes_text, (300, 390))
    screen.blit(no_text, (450, 390))


def show_score():
    score = font.render("Points: " + str(points), True, WHITE)
    screen.blit(score, (10, 10))


clock = pg.time.Clock()
running = True
end_game = False
while running:

    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                player_speed = -3
            if event.key == pg.K_RIGHT:
                player_speed = 3
            if event.key == pg.K_SPACE:
                if not bullet_state:
                    bullet_sound.play()
                    bullet.rect.x = player.rect.x + 15
                    bullet_state = True
        if event.type == pg.KEYUP:
            if (event.key == pg.K_LEFT) or (event.key == pg.K_RIGHT):
                player_speed = 0
        if event.type == pg.MOUSEBUTTONDOWN and end_game:
            x = pg.mouse.get_pos()[0]
            y = pg.mouse.get_pos()[1]
            if 290 < x < 350 and 380 < y < 420:
                end_game = False
                points = 0
                num_enemies = 5
                enemy_change_x.clear()
                pg.sprite.Group.empty(enemy_group)
                for i in range(0, num_enemies):
                    enemy = Enemy()
                    enemy_group.add(enemy)
                    enemy_change_x.append(3)
                enemies = pg.sprite.Group.sprites(enemy_group)
            elif 440 < x < 490 and 380 < y < 420:
                running = False

    screen.blit(background, (0, 0))

    for i in range(0, num_enemies):
        enemies[i].rect.x += enemy_change_x[i]
        if enemies[i].rect.x > 735:
            enemy_change_x[i] *= -1
            enemies[i].rect.y += enemy_change_y
        elif enemies[i].rect.x < 5:
            enemy_change_x[i] *= -1
            enemies[i].rect.y += enemy_change_y

    if new_enemy and ((points % 10) == 0) and points != 0:
        new_enemy = False
        enemy = Enemy()
        enemy_group.add(enemy)
        enemy_change_x.append(((points / 10) * 0.5) + 1)
        num_enemies += 1
        enemies = pg.sprite.Group.sprites(enemy_group)
    elif not new_enemy and ((points % 10) != 0):
        new_enemy = True

    if pg.sprite.groupcollide(player_group, enemy_group, False, False, pg.sprite.collide_mask):
        for i in range(0, num_enemies):
            enemies[i].rect.y = 2000
        end_game = True

    if pg.sprite.groupcollide(bullet_group, enemy_group, False, True, pg.sprite.collide_mask):
        collision_sound.play()
        points += 1
        bullet.rect.x = -30
        bullet.rect.y = 480
        bullet_state = False
        enemy = Enemy()
        enemy_group.add(enemy)
        enemies = pg.sprite.Group.sprites(enemy_group)

    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)

    player_group.update()
    bullet_group.update()

    if end_game:
        game_over()

    show_score()
    pg.display.update()

pg.quit()

