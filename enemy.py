import pygame
import random
import math

class Enemy:
    def start(self, x, y, speed_x, speed_y, enemy_type, health, movement):
        self.alive = True
        self.movement = movement
       
        self.enemy_sprites = [self.setup_sprite("images/enemy/fighter.png"), #normal
                              self.setup_sprite("images/enemy/bomber.png"), #fast
                              self.setup_sprite("images/enemy/frigate.png"), #slow, high health
                              self.setup_sprite("images/enemy/support.png"), #fast + high health
                              self.setup_sprite("images/enemy/battlecruiser.png"), #miniboss
                              self.setup_sprite("images/enemy/bomber.png"), #fast, spawn in groups of 3
                              self.setup_sprite("images/enemy/scout.png"), #slightly faster, high health and high bullets
                              self.setup_sprite("images/enemy/torpedo-ship.png"), #side to side quickly
                              self.setup_sprite("images/enemy/support.png"), #lots of small ones, lots of bullets
                              self.setup_sprite("images/enemy/dreadnought.png") #final boss
                              ]
        
        self.image = self.enemy_sprites[enemy_type]

        self.position = self.image.get_rect()
        self.position.center = (x,y)

        self.timer = 0
        self.sprite_time = 30

        self.enemy_type = enemy_type
        self.health = health

        self.max_speed_x = speed_x
        self.max_speed_y = speed_y
        self.speed_x = 0
        self.speed_y = self.max_speed_y

        self.direction = 0
        
        self.current_wave = 0

        self.shoot_cooldown = 0

        self.value = 10
        self.scored = False

        self.divebombing = False
        self.divebomb_timer = 0

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.position)

    def setup_sprite(self, sprite_path):
        sprite = pygame.image.load(sprite_path)
        return pygame.transform.flip(sprite, False, True)
    
    def move(self, screenwidth = 0):
        #if enemy.position <= 0:

        if self.alive:
            #if self.current_wave == 0:
            self.position.x += self.speed_x
            self.position.y += self.speed_y

    def move_left(self):
        self.direction = -1
        self.speed_x = self.max_speed_x * self.direction

    def move_right(self):
        self.direction = 1
        self.speed_x = self.max_speed_x * self.direction
    
    def fire(self, bullet, x = 0, y = 0):
        if self.alive:
            p_x = self.position.x + x
            p_y = self.position.y + y

            bullet.position.x = p_x
            bullet.position.y = p_y

            bullet.active = True
            self.shoot_cooldown = 60

    def cooldown(self):
        self.shoot_cooldown -= 1
 
    def damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.alive = False

    def collide(self, mask, x = 0, y = 0):
        if self.alive:
            enemy_mask = self.get_mask()
            offset = (self.position.x - x, self.position.y - y)
            return mask.overlap(enemy_mask, offset)
        else:
            return None
        
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def update_movement(self, screen_width, player):
        if self.movement == "Bounce":
            self.bounce_movement(screen_width)

        elif self.movement == "Random":
            self.random_movement(screen_width)

        elif self.movement == "Divebomb":
            self.divebomb_movement(player)

        self.move()

    def bounce_movement(self, screen_Width):
        if self.direction == 0:
            self.move_right()
        elif self.position.right > screen_Width:
            self.move_left()
        elif self.position.left < 0:
            self.move_right()

    def random_movement(self, width):
        if random.random() < 0.1:
            self.speed_x = random.randint(-self.max_speed_x, self.max_speed_x)
        if self.position.left < 0:
            self.speed_x = abs(self.speed_x)
        if self.position.x >= width:
            self.speed_x = -abs(self.speed_x)
        self.speed_y = self.max_speed_y

    def divebomb_movement(self, player):
        self.divebomb_timer += 1
        if self.divebomb_timer < 90: #90 is 1.5 seconds (90/60fps)
            self.speed_x = 0
            self.speed_y = self.max_speed_y
        else:
            self.divebombing = True
        if self.divebombing:
            b = player.position.centerx - self.position.centerx 
            c = player.position.centery - self.position.centery
            a = math.sqrt(b ** 2 + c ** 2)
            if a != 0:
                self.speed_x = (b / a) * self.max_speed_x * 4
                self.speed_y = (c / a) * self.max_speed_y * 4