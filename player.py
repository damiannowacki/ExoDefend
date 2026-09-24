import pygame
import random

class Player:
    def start(self, x, y):
       self.alive = True
       self.lives = 3
       
       self.main_sprites = [pygame.image.load("images/player/player-health-0.png"), 
                            pygame.image.load("images/player/player-health-1.png"),
                            pygame.image.load("images/player/player-health-2.png"),
                            pygame.image.load("images/player/player-health-3.png")]
       self.engine_sprite = pygame.image.load("images/player/engine.png")
       self.booster_sprites = self.split_up_spritesheet(pygame.image.load("images/player/engine.png"), 48, False)
       self.image = self.main_sprites[self.lives]
       self.flame_sprite = self.booster_sprites[0]

       self.position = self.image.get_rect()
       self.position.center = (x,y)

       self.timer = 0
       self.sprite_time = 5

       self.max_speed = 5
       self.speed = 0
       self.direction = 0

       self.shot_cooldown = 0 #between each shot cooldown
       self.burst_cooldown = 0 #between each burst cooldown, burst randomizes bullet jam
       self.burst_count = 0 #current count of bullets in burst
       self.burst_amount = random.randint(3,6) #total amount of bullets in burst


       
    def draw(self, screen):
        if self.alive:
            self.animate()
            screen.blit(self.engine_sprite, self.position)
            screen.blit(self.image, self.position)
            screen.blit(self.flame_sprite, self.position)

    def animate(self):
        self.image = self.main_sprites[self.lives]

        index = int(self.timer // self.sprite_time) % len(self.booster_sprites)
        self.flame_sprite = self.booster_sprites[index]

        self.timer += 1
    
    def split_up_spritesheet(self, spritesheet, size, flipped = False):
        sprite_list = []

        number_of_sprites = spritesheet.get_width() // size

        for i in range(number_of_sprites):
            sprite = spritesheet.subsurface(i * size, 0, size, size)

            sprite = pygame.transform.flip(sprite, flipped, False)

            sprite_list.append(sprite)
        
        return sprite_list
    
    def move(self):
        if self.alive:
            if self.speed > 0:
                self.speed -= 0.2
            elif self.speed < 0:
                self.speed += 0.2
            else:
                self.speed = 0
                self.direction = 0

            self.position.x += self.speed

    def move_left(self):
        self.direction = -1
        self.speed = self.max_speed * self.direction

    def move_right(self):
        self.direction = 1
        self.speed = self.max_speed * self.direction
    
    def cooldown(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        
        if self.burst_cooldown > 0:
            self.burst_cooldown -= 1

    def fire(self, bullet, x=0, y=0):
        if self.alive and self.shot_cooldown <= 0 and self.burst_cooldown <= 0:
            p_x = self.position.x + x
            p_y = self.position.y + y

            bullet.position.x = p_x
            bullet.position.y = p_y

            bullet.active = True

            self.burst_count += 1

            if self.burst_count >= self.burst_amount:
                self.burst_cooldown = 120
                self.burst_count = 0
                self.burst_amount = random.randint(3,6)
            else:
                self.shot_cooldown = 10

    def damage(self, damage):
        self.lives -= damage 
        if self.lives <= 0:
            self.alive = False

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

