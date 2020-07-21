import pygame
from pygame import Color
from spritesheet import SpriteSheet, Origin
import random
pygame.init()

screen_height = 700
screen_width = 900
y_axis_offset = 112
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Dino")
background = pygame.image.load("PyGame Pictures\\bg.png").convert()
end_begin_screen = pygame.image.load("PyGame Pictures\\end_screen.png").convert()
background_scaled = pygame.transform.scale(background, (screen_width, screen_height + y_axis_offset))
end_begin_screen_scaled = pygame.transform.scale(end_begin_screen, (screen_width, screen_height))

dino_pixel_height = 71

game_speed_increase = 0
backgroundX = 0
backgroundX2 = screen_width
class Pipe():
    def __init__(self, drop_location_x, pipe_gap, height_top, width):
        self.drop_location_x = drop_location_x
        self.height_top = height_top
        self.height_bottom = screen_height - y_axis_offset - height_top - pipe_gap
        self.drop_location_y_top = 0
        self.drop_location_y_bottom = screen_height - self.height_bottom - y_axis_offset
        self.width = width
        self.pipe_gap = pipe_gap
        self.pipe_image_top = pygame.image.load("PyGame Pictures\\tp.png").convert()
        self.pipe_image_top_scaled = pygame.transform.scale(self.pipe_image_top, (self.width, self.height_top))
        self.pipe_image_bottom = pygame.image.load("PyGame Pictures\\tp2.png").convert()
        self.pipe_image_bottom_scaled = pygame.transform.scale(self.pipe_image_bottom, (self.width, self.height_bottom))
        self.hit_box_top = (self.drop_location_x, self.drop_location_y_top, self.width, self.height_top)
        self.hit_box_bottom = (self.drop_location_x, self.drop_location_y_bottom, self.width, self.height_bottom)
    def draw(self):
        self.hit_box_top = (self.drop_location_x, self.drop_location_y_top, self.width, self.height_top)
        self.hit_box_bottom = (self.drop_location_x, self.drop_location_y_bottom, self.width, self.height_bottom)
        screen.blit(self.pipe_image_top_scaled, (self.drop_location_x, self.drop_location_y_top))
        screen.blit(self.pipe_image_bottom_scaled, (self.drop_location_x, self.drop_location_y_bottom))
        # pygame.draw.rect(screen, Color(255, 0, 0), self.hit_box_top, 2)
        # pygame.draw.rect(screen, Color(255, 0, 0), self.hit_box_bottom, 2)
    def collide(self, hit_box):
        for x in range(hit_box[0] + hit_box[2], hit_box[0], -1):
            if hit_box[1] < self.hit_box_top[3] and self.hit_box_top[0] < x < self.hit_box_top[0] + self.hit_box_top[2]:
                return True
                break
            if hit_box[1] + hit_box[3] > self.hit_box_bottom[1] and self.hit_box_bottom[0] < x < self.hit_box_bottom[0] + self.hit_box_bottom[2]:
                return True
                break
class Bird():
    def __init__(self, drop_location_x, drop_location_y,):
        self.drop_location_x = drop_location_x
        self.drop_location_y = drop_location_y
        self.jump_count = 0
        self.sprite = pygame.image.load("PyGame Pictures\\bird2.png")
    def fall(self):
        self.drop_location_y -= (self.jump_count * 3)
        self.jump_count -= 1
    def jump(self):
        self.fall()
        if self.drop_location_y - self.jump_count * 3 < 0:
            self.jump_count = 0
            self.fall()
        if self.drop_location_y > screen_height - y_axis_offset - random.randrange(0, 200):
            self.jump_count = random.randrange(2, 15)
            self.fall()
    def draw(self):
        screen.blit(self.sprite,(self.drop_location_x, self.drop_location_y))
        self.hit_box_bird = (self.drop_location_x+10, self.drop_location_y+5, 50, 35)
        # pygame.draw.rect(screen, (255, 255, 255), self.hit_box_bird, 2)
    def collide(self, hit_box):
        for x in range(hit_box[0] + hit_box[2], hit_box[0], -1):
            for y in range(hit_box[1] + hit_box[3], hit_box[1], -1):
                if self.hit_box_bird[3] + self.hit_box_bird[1] > y > self.hit_box_bird[1] and self.hit_box_bird[0] < x < self.hit_box_bird[0] + self.hit_box_bird[2]:
                    return True
                    break
class FlappyDino():
    def __init__(self, drop_location_x, drop_location_y):
        self.drop_location_x = drop_location_x
        self.drop_location_y = drop_location_y
        self.IsJump = False
        self.jump_count = 3
        self.jump_count_implemented = self.jump_count
        self.walk_count = 0
        self.activation_time = 0
        self.frames_per_sprite = 3
        self.belongtobao = True
        self.sprites = SpriteSheet("PyGame Pictures\\dino3.png", columns=5, rows=1,colour_key=Color(0, 0, 0))
        self.sprites_duck = SpriteSheet("PyGame Pictures\\dino-duck3.png", columns = 2, rows=1, colour_key=Color(0, 0, 0))
    def fall(self):
        self.drop_location_y -= (self.jump_count_implemented * 10)
        self.jump_count_implemented -= 1
    def jump(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_UP]:
            self.IsJump = True
            self.activation_time += 1
        if self.IsJump == True:
            if self.drop_location_y - self.jump_count_implemented * 10 >= 0:
                self.fall()
            if self.drop_location_y - self.jump_count_implemented * 10 < 0:
                self.jump_count_implemented = 0
                self.fall()
            if self.keys[pygame.K_DOWN]:
                self.jump_count_implemented = -5
                self.fall()
            if self.keys[pygame.K_UP] and self.activation_time % 2 == 0:
                self.jump_count_implemented = self.jump_count
            if self.drop_location_y > screen_height - y_axis_offset - dino_pixel_height: #71 is the dino's pixel height
                self.IsJump = False
                self.jump_count_implemented = self.jump_count
        if self.drop_location_y >= screen_height - y_axis_offset - dino_pixel_height:
            self.drop_location_y = screen_height - y_axis_offset - dino_pixel_height
    def DrawCharacter(self):
        global walk_count
        screen.blit(background_scaled, (backgroundX, 0))
        screen.blit(background_scaled, (backgroundX2, 0))
        self.hit_box_walking = (self.drop_location_x + 15, self.drop_location_y + 10, 30, dino_pixel_height - 10)
        self.hit_box_ducking =  (self.drop_location_x + 10, self.drop_location_y + 30, 80, 35)
        if run == True:
            self.walk_count += 1
            if self.drop_location_y >= screen_height - y_axis_offset - dino_pixel_height and self.keys[pygame.K_DOWN]:
                if self.walk_count + 1 >= 2 * self.frames_per_sprite:
                    self.walk_count = 0
                self.sprites_duck.blit(screen, self.walk_count // self.frames_per_sprite, position=(self.drop_location_x, self.drop_location_y), origin=Origin.TopLeft)
                self.dino_hit_box = self.hit_box_ducking
                # pygame.draw.rect(screen, (255, 0, 0),self.dino_hit_box, 2)
            else:
                if self.walk_count + 1 >= 5 * self.frames_per_sprite:
                    self.walk_count = 0
                self.sprites.blit(screen, self.walk_count // self.frames_per_sprite, position=(self.drop_location_x, self.drop_location_y),
                         origin=Origin.TopLeft)
                self.dino_hit_box = self.hit_box_walking
                # pygame.draw.rect(screen, (255, 0, 0), self.dino_hit_box, 2)
pygame.time.set_timer(pygame.USEREVENT, 1750)
pygame.time.set_timer(pygame.USEREVENT + 2, 200)
pygame.time.set_timer(pygame.USEREVENT + 3, random.randrange(200, 350))
dino_character = FlappyDino(100, screen_height - y_axis_offset - dino_pixel_height) #71 is the dino's pixel height)
run = True
score = 0
bird_jump = 0
distance_between_pipes = 400
distance_between_birds = 600
pipe_list = [Pipe(screen_width, random.randrange(200, 350), random.randrange(0, 200), 50)]
bird_list = [Bird(screen_width, random.randrange(50, 500))]
def end_game():
    pass
    global game_speed_increase, pipe_list, backgroundX, backgroundX2, bird_list, text, score
    end_screen = True
    game_speed_increase = 0
    pipe_list = [Pipe(screen_width, random.randrange(250, 350), random.randrange(0, 200), 50)]
    bird_list = [Bird(screen_width, random.randrange(50, 500))]
    score = 0
    backgroundX = 0
    backgroundX2 = screen_width
    screen.blit(end_begin_screen_scaled, (0, 0))
    screen.blit(text, (screen_width - 100, 10))
    pygame.time.delay(1200)
    pygame.display.update()
    while end_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen = False
                pygame.quit()
        if pygame.key.get_pressed()[pygame.K_g]:
            end_screen = False
def begin_game():
    pass
    begin_screen = True
    while begin_screen:
        pygame.time.delay(100)
        screen.blit(end_begin_screen_scaled, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                begin_screen = False
                pygame.quit()
        if pygame.key.get_pressed()[pygame.K_g]:
            begin_screen = False
begin_game()
while run:
    pygame.time.Clock().tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.USEREVENT:
            game_speed_increase += 0.5
        if game_speed_increase >= 40:
            game_speed_increase = 40
        if event.type == pygame.USEREVENT + 2:
            score += 1
        if event.type == pygame.USEREVENT + 3:
            bird_jump += 1
    backgroundX -= 10 + game_speed_increase
    backgroundX2 -= 10 + game_speed_increase
    if backgroundX < screen_width * -1:
        backgroundX = screen_width
    if backgroundX2 < screen_width * -1:
        backgroundX2 = screen_width

    dino_character.jump()
    dino_character.DrawCharacter()
    text = pygame.font.SysFont('comicsans', 30).render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(text, (screen_width - 100, 10))
    for x in pipe_list:
        if x.drop_location_x + x.width <= 0:
            pipe_list.pop(pipe_list.index(x))
        x.drop_location_x -= 10 + game_speed_increase
        x.draw()
        if screen_width - distance_between_pipes - 10 - game_speed_increase < x.drop_location_x <= screen_width - distance_between_pipes:
            if random.randint(0, 4) == 2:
                pipe_list.append(Pipe(screen_width, 50, screen_height - y_axis_offset - 50, 50))
            else:
                pipe_list.append(Pipe(screen_width, random.randrange(200, 300), random.randrange(0, 150), 50))
        if x.collide(dino_character.dino_hit_box):
            pygame.display.update()
            end_game()
    for x in bird_list:
        if x.drop_location_x <= 0:
            bird_list.pop(bird_list.index(x))
        x.drop_location_x -= (10 + game_speed_increase)*1.2
        if bird_jump == 2:
            x.jump_count = random.randrange(2, 10)
            bird_jump -= 2
        if screen_width - distance_between_birds - (10 + game_speed_increase)*1.2 < x.drop_location_x <= screen_width - distance_between_birds:
            bird_list.append(Bird(screen_width, random.randrange(50, 500)))
        x.jump()
        x.draw()
        if x.collide(dino_character.dino_hit_box):
            pygame.display.update()
            end_game()
    pygame.display.update()

