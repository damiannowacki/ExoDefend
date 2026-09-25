import pygame
import random
from player import Player 
from enemy import Enemy
from bullet import Bullet
from enemy_waves import waves
from account_manager import Account_Manager


class Game:
    def __init__(self):
        self.width = 450

    def start(self):
        self.setup()
        if self.current_user is not None:
            self.run()
    
    def setup(self):
        pygame.init()
        
        pygame.display.set_caption("ExoDefend")

        self.fps = 60

        self.height = 800

        self.offset = 0

        self.screen = pygame.display.set_mode((self.width, self.height), vsync = 1)
        self.clock = pygame.time.Clock()

        self.accounts = Account_Manager()
        self.current_user = self.startscreen()

        if self.current_user is None:
            return

        print("Logged in as:", self.current_user)

        self.heart = pygame.image.load("images/player/Heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (45, 45))
        
        self.player = Player()
        self.enemy = Enemy()
        self.highscore = self.accounts.get_highscore(self.current_user)
        self.waves = waves

        self.enemies = []

        self.player_bullet_pool = []
        self.enemy_bullet_pool = []
        self.score_pool = []

        self.score_pool_cooldown = 30
        self.score = 0

        self.spawn_timer = 0
        self.spawn_timer_offset = 0
        self.current_wave = 0

        self.bullets_shot_amount = 0
        self.bullets_landed = 0
        self.enemies_killed_count = 0

        for i in range(1000):
            bullet = Bullet()
            bullet.start(200,200,"player")
            self.player_bullet_pool.append(bullet)

        self.player.start(self.width // 2, self.height - 50)
        initial_bullets = self.waves[self.current_wave].number_of_bullets
        self.bullet_creation(initial_bullets)


    def run(self):
        running = True
        playing = True

        while running:
            # clock
            self.clock.tick(self.fps)

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            # gameplay
            if playing:
                self.update_enemies()
                self.update_player()
                if len(self.score_pool) > 0:
                    if self.score_pool_cooldown > 0:
                        self.score_pool_cooldown -= 1
                    else:
                        self.score_pool_cooldown = 30
                        self.score_pool.pop(0)
                if not self.player.alive:
                    self.accounts.save_highscore(self.current_user, self.score)
                    self.highscore = self.accounts.get_highscore(self.current_user)
                    playing = False


            # draw
            self.draw_background()

            if playing:
                self.draw_enemies()
                self.player.draw(self.screen)
                self.draw_text(f"WAVE_{self.current_wave + 1}", 48, x = 20, y = 20)

                self.draw_text(f"Player: {self.current_user}", 10, x=10, y=100)
                self.draw_text(f"High: {self.highscore}", 10, x=10, y=150)

                for bullet in self.player_bullet_pool:
                    bullet.draw(self.screen)
                
                for bullet in self.enemy_bullet_pool:
                    bullet.draw(self.screen)

                for score in self.score_pool:
                    self.draw_text(score[0], 10, x = score[1], y = score[2])

            else:
                self.draw_text("GAME OVER!", 45, 8, 20)
                self.draw_text(f"HIGH SCORE: {self.highscore}", 20, 80, 80)
                self.stats()

            
            self.draw_hearts()
                    

            # render
            pygame.display.update()
        
        pygame.quit()
    
    def update_player(self):
        keys = pygame.key.get_pressed()
        if self.player.position.left < 0:
            self.player.speed = 0

        elif self.player.position.right > self.width:
            self.player.speed = 0

        if keys[pygame.K_a] and self.player.position.left > 0:
            self.player.move_left()
        
        if keys[pygame.K_d] and self.player.position.right < self.width:
            self.player.move_right()

        self.player.move()
        self.player.cooldown()
        self.update_player_bullets()

    def update_player_bullets(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.player.shot_cooldown <= 0 and self.player.burst_cooldown <= 0:
            for bullet in self.player_bullet_pool:
                if not bullet.active:
                    self.player.fire(bullet, x = 8)
                    self.bullets_shot_amount += 1
                    break

        for bullet in self.player_bullet_pool:
            bullet.move()

            if bullet.position.bottom < 0:
                bullet.active = False

            for enemy in self.enemies:
                if enemy.alive and bullet.active:
                    if bullet.collide(enemy.get_mask(), enemy.position.x, enemy.position.y) != None:
                        enemy.damage(1)
                        self.bullets_landed += 1
                        bullet.active = False
                        if not enemy.alive and not enemy.scored:
                            self.score += enemy.value
                            self.score_pool.append((f"{enemy.value}", enemy.position.centerx, enemy.position.centery))
                            enemy.scored = True
                            self.enemies_killed_count += 1


    def draw_background(self):
        space = pygame.image.load("images/space/Big Space Background 2.png")
        space = pygame.transform.scale(space, (self.width, self.height))

        self.screen.blit(space, (0, self.offset - space.get_height()))
        self.screen.blit(space, (0, self.offset))
        self.screen.blit(space, (0, self.offset + space.get_height()))

        if self.offset > space.get_height():
            self.offset = 0

        self.offset += 1
    
    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)

    def update_enemies(self):
        self.update_wave()

        for enemy in self.enemies:
            enemy.update_movement(self.width, self.player)
            enemy.cooldown()
            
            if enemy.position.top > self.height and enemy.alive == True:
                enemy.alive = False
                self.player.damage(1)

            if enemy.alive and self.player.alive:
                if enemy.collide(self.player.get_mask(), self.player.position.x, self.player.position.y):
                    enemy.damage(1)
                    self.player.damage(1)

        self.update_enemy_bullets()

    def update_enemy_bullets(self):
        for bullet in self.enemy_bullet_pool:
            if len(self.enemies) > 0:
                random_num = random.randint(0, len(self.enemies) - 1)
                enemy = self.enemies[random_num]

                if not bullet.active and enemy.shoot_cooldown <= 0 and random.random() > 0.75:
                    enemy.fire(bullet, x= 28, y=40)

                bullet.move()

                if bullet.position.top > self.height:
                    bullet.active = False
                
                for enemy in self.enemies:
                    if enemy.alive and bullet.active:
                        if bullet.collide(self.player.get_mask(), self.player.position.x, self.player.position.y) != None:
                            self.player.damage(1)
                            bullet.active = False


    def update_wave(self):
        wave = self.waves[self.current_wave]
        next_wave = True

        if len(self.enemies) < wave.number_of_enemies and self.spawn_timer // 1000 >= wave.time_between_enemies * len(self.enemies):
            for i in range(wave.burst_enemy_number):
                enemy = Enemy()
                offset_x = (i - (wave.burst_enemy_number - 1) / 2) * 40
                offset_y = (i - (wave.burst_enemy_number - 1) / 2) * 20

                if wave.movement_type == "Divebomb":
                    offset_x =  random.randint(-100, 100)

                enemy.start(wave.start_x + offset_x, wave.start_y + offset_y, wave.speed_x, wave.speed_y, wave.enemy_type, wave.health, wave.movement_type)
                enemy.current_wave = self.current_wave
                self.enemies.append(enemy)

            self.spawn_timer = 0
        else:
            self.spawn_timer = pygame.time.get_ticks() - self.spawn_timer_offset

        all_spawned = len(self.enemies) >= wave.number_of_enemies
        if not all_spawned:
            next_wave = False
        else:
            for enemy in self.enemies:
                if enemy.alive:
                    next_wave = False
        
        if next_wave:
            self.current_wave = self.current_wave + 1 if self.current_wave + 1 < len(self.waves) else 0
            self.spawn_timer_offset += self.spawn_timer
            self.spawn_timer = 0
            self.enemies = []
            new_wave = self.waves[self.current_wave]
            number_of_bullets = new_wave.number_of_bullets
            self.bullet_creation(number_of_bullets)
            print(number_of_bullets)


        """if next_wave and wave_10 in waves:
            self.level = 10
            self.playing = False"""

    def bullet_creation(self, x):
        self.enemy_bullet_pool = []
        for i in range(x):
            bullet = Bullet()
            bullet.start(300,200,"enemy")
            self.enemy_bullet_pool.append(bullet)

    def draw_text(self, message, size, x = 0, y = 0, centered = False):
        font = pygame.font.Font("fonts/pixeled.ttf", size)
        text = font.render(message, 1, "white")
        origin_x = 0
        origin_y = 0
        if centered:
            origin_x = (self.width - text.get_width()) / 2
            origin_y = (self.height - text.get_height()) / 2
        self.screen.blit(text, (origin_x + x, origin_y + y))

    def draw_stats_text(self, message, size, x = 0, y = 0, centered = False):
            font = pygame.font.Font("fonts/pixeloidsans-bold.ttf", size)
            text = font.render(message, 1, "white")
            origin_x = 0
            origin_y = 0
            if centered:
                origin_x = (self.width - text.get_width()) / 2
                origin_y = (self.height - text.get_height()) / 2
            self.screen.blit(text, (origin_x + x, origin_y + y))

    def draw_hearts(self):
        for i in range(self.player.lives):
            x = self.width - 140 + i * 40
            y = 25
            self.screen.blit(self.heart, (x,y))


    def accuracy(self):
        if self.bullets_shot_amount == 0:
            self.accuracy_finder = 0
            return self.accuracy_finder
        elif self.bullets_shot_amount > 0 and self.bullets_landed == 0:
            self.accuracy_finder = 0
            return self.accuracy_finder
        self.accuracy_finder = (self.bullets_landed / self.bullets_shot_amount) * 100 
        if self.accuracy_finder == int(self.accuracy_finder):
            return int(self.accuracy_finder)
        elif self.accuracy_finder == round(self.accuracy_finder, 1):
            return self.accuracy_finder
        else:
            return round(self.accuracy_finder, 2)


    def stats(self):
        stats_box = pygame.image.load("images/buttons/Buttons/stats_box.png").convert_alpha()
        stats_box = pygame.transform.scale(stats_box, (375, 480))
        self.screen.blit(stats_box, (36, 120))

        self.draw_text("STATS", 36, 132, 174)
        self.draw_stats_text(f"Current Score: {self.score}", 22, 80, 270)
        self.draw_stats_text(f"Levels Survived: {self.current_wave}", 22, 80, 310)
        self.draw_stats_text(f"Enemies Killed: {self.enemies_killed_count}", 22, 80, 350)
        self.draw_stats_text(f"Bullets Shot: {self.bullets_shot_amount}", 22, 80, 390)
        self.draw_stats_text(f"Bullets Landed: {self.bullets_landed}", 22, 80, 430)
        self.draw_stats_text(f"Accuracy: {self.accuracy()}%", 22, 80, 470)
        
        retry_button = pygame.image.load("images/buttons/Buttons/Retry_button.png")
        retry_button = pygame.transform.scale(retry_button, (400, 100))
        self.screen.blit(retry_button, (25 ,620))

        settings_button = pygame.image.load("images/buttons/Icons/Settings_icon.png")
        settings_button = pygame.transform.scale(settings_button, (65, 65))
        self.screen.blit(settings_button, (180, 725))
        

    def startscreen(self):
        self.draw_background()
        self.draw_text("EXO", 50, 150, 32)
        self.draw_text("DEFEND", 50, 80, 100)

        log_in_button = pygame.image.load("images/buttons/Buttons/Log_in_button.png")
        log_in_button = pygame.transform.scale(log_in_button, (310,100))
        self.screen.blit(log_in_button, (80,400))

        sign_up_button = pygame.image.load("images/buttons/Buttons/Sign_up_button.png")
        sign_up_button = pygame.transform.scale(sign_up_button, (310,100))
        self.screen.blit(sign_up_button, (80,520))
          
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.is_clicked(80,400,300,100): #login
                        username = self.account_screen("login")
                        if username is not None:
                            return username
                    elif self.is_clicked(80,520,310,100): #signup
                        username = self.account_screen("signup")
                        if username is not None:
                            return username
                    

            pygame.display.update()

    def account_screen(self, mode):
        username = ""
        password = "" 
        selected = "username"
        message = ""
        while True:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_TAB:
                        if selected == "username":
                            selected = "password"
                        else:
                            selected = "username"
                    elif event.key == pygame.K_RETURN:
                        if selected == "username":
                            selected = "password"
                        else:
                            if mode == "login":
                                if self.accounts.login(username, password):
                                    return username
                                else:
                                    message = "Invalid Login"
                            elif mode == "signup":
                                success, message = self.accounts.sign_up(username, password)
                                if success:
                                    return username
                    elif event.key == pygame.K_BACKSPACE:
                        if selected == "username":
                            username = username[:-1]
                        else:
                            password = password[:-1]
                    else:
                        if event.unicode.isprintable():
                            if selected == "username":
                                username += event.unicode
                            else:
                                password += event.unicode
            self.screen.fill("black")
            if mode == "login":
                title = "LOGIN"
            else:
                title = "SIGN UP"
            self.draw_text(title, 26, y=-170, centered=True)
            self.draw_text("Username:", 14, y=-90, centered=True)
            self.draw_text(username, 14, y=-55, centered = True)
            self.draw_text("Password:", 14, y=0, centered=True)
            hiddem_password = "*" * len(password)
            self.draw_text(hiddem_password, 14, y=35, centered=True)
            if selected == username:
                selected_text = "Typing Username"
            else:
                selected_text = "Typing Password"
            self.draw_text(selected_text, 10, y=100, centered = True)
            self.draw_text("TAB - Switch", 8, y=140, centered = True)
            self.draw_text("ENTER - Continue", 8, y = 165, centered = True)
            if message != "":
                self.draw_text(message, 10, y = 210, centered=True)
            pygame.display.update()

    def is_clicked(self, button_x, button_y, button_width, button_height):
        button_layout = pygame.Rect(button_x, button_y, button_width, button_height)
        if button_layout.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

game = Game()
game.start()

#fix enemy shooting bullets
#DO ALL MOVEMENT TYPES
#healthbar for enemies
#add sound effects, for shooting, losing a life, quiet background music
#maybe a bullet count in bottom corner, and says how much you used out of total amount of bullets, with a reload animation when reloading