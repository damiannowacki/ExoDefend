import pygame

class Bullet:
    def start(self, x, y, owner):
        self.active = False
        self.owner = owner
       
        if self.owner == "player":
           self.size = 40
           self.speed = -6
           self.sprites = self.split_up_spritesheet(pygame.image.load("images/bullet/player-bullet.png"), False)
        else:
            self.size = 15
            self.speed = 5
            self.sprites = self.split_up_spritesheet(pygame.image.load("images/bullet/enemy-bullet.png"), False)

        self.image = self.sprites[0]
        self.position = self.image.get_rect()
        self.position.center = (x,y)

        self.timer = 0
        self.sprite_time = 5
    
    def move(self):
        self.position.y += self.speed

    def update(self):
        if self.active:
            self.move()

    def draw(self, screen):
        if self.active:
            self.animate()
            screen.blit(self.image, self.position)
            

    def animate(self):
        index = self.timer // self.sprite_time % len(self.sprites)

        self.image = self.sprites[index]

        self.timer += 1
    
    def split_up_spritesheet(self, spritesheet, flipped = False):
        sprite_list = []

        number_of_sprites = int(spritesheet.get_width() // self.size)

        for i in range(number_of_sprites):
            sprite = spritesheet.subsurface(i * self.size, 0, self.size, self.size)

            sprite = pygame.transform.flip(sprite, flipped, False)

            sprite_list.append(sprite)
        
        return sprite_list
    
    def get_mask(self):
        return pygame.mask.from_surface(self.image)

    def collide(self, mask, x=0, y=0):
        if self.active:
            bullet_mask = self.get_mask()
            offset = (self.position.x - x, self.position.y - y)
            return mask.overlap(bullet_mask, offset)
        else:
            return None