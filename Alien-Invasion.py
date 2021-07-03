import sys
import pygame
import random
import time
from pygame.sprite import Sprite
from pygame.sprite import Group

class Settings():
    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.screen_width = 1200
        self.screen_hight = 800
        self.caption = "Alien Invasion"
        self.bullet_speed_factor = 6
        self.bullet_width = 3
        self.bullet_hight = 15
        self.bullet_color = [255, 255, 102]
        self.bullet_number = 100
        self.bullet_vanish = True
        self.ship_life=3
        self.ship_low_life_num=5
        self.ship_speed=6
        self.beatable_time=3
        self.alien_bullet_color=[255,255,102]
        self.alien_transform = 200
        self.alien_life = 3
        self.alien_point = 5
        self.alien_speed = 3
        self.alien_bullet_speed = self.alien_speed+1

class GameStats():
    def __init__(self):
        self.score=0
        self.game_active = False
        self.last_score=0

    def reset_stats(self):
        self.score=0

class Scoreboard():
    def __init__(self,screen,ai_setting,stats):
        self.screen=screen
        self.screen_rect=screen.get_rect()
        self.ai_settings=ai_setting
        self.stats=stats
        self.stats_score=True

        self.text_color=(250,250,250)
        self.font=pygame.font.Font('resources/font.ttf', 48)
        self.prep_score()

    def prep_score(self):
        if self.stats.game_active:
            score_str=str(self.stats.score)
            self.score_image = self.font.render(score_str, True, self.text_color)
            self.score_rect = self.score_image.get_rect()
            self.score_rect.right = self.ai_settings.screen_width - 20
            self.score_rect.top = 20
        else:
            score_str = str(self.stats.last_score)
            self.score_image = self.font.render(score_str, True, self.text_color)
            self.score_rect = self.score_image.get_rect()
            self.score_rect.centerx = self.screen_rect.centerx
            self.score_rect.top = self.screen_rect.centery + 100

    def show_score(self):
        self.prep_score()
        self.screen.blit(self.score_image,self.score_rect)

class Bullet(Sprite):
    def __init__(self, ai_setting, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        self.image = pygame.image.load('resources/bullet2.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.speed = ai_setting.bullet_speed_factor
        self.color = ai_setting.bullet_color
        self.bullet_number = ai_setting.bullet_number
        self.ship_location = ship.rect.bottom

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        self.update()
        self.screen.blit(self.image, self.rect)

class AlienBullet(Sprite):
    def __init__(self, ai_setting, screen,alien):
        super(AlienBullet, self).__init__()
        self.screen = screen
        self.position = [alien.rect.centerx,alien.rect.bottom]
        self.raduis = 3
        self.color = ai_setting.alien_bullet_color
        self.width=0
        self.speed=ai_setting.alien_bullet_speed
        self.rect=pygame.Rect(0,0,self.raduis*2,self.raduis*2)
        self.rect.centerx=self.position[0]
        self.rect.centery=self.position[1]

    def update(self):
        self.position[1] += self.speed
        self.position[1]=int(self.position[1])
        self.rect.centery = self.position[1]

    def draw_bullet(self):
        self.update()
        pygame.draw.circle(self.screen, self.color, self.position, self.raduis, self.width)

class Ship():
    def __init__(self, screen, ai_setting):
        self.screen = screen
        self.image = pygame.image.load('resources/ship3.png')
        self.fire_image = pygame.image.load('resources/ship_fire.png')
        self.fire_rect = self.fire_image.get_rect()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.life = ai_setting.ship_life
        self.life_rect = self.image.get_rect()
        self.low_life_rect=pygame.Rect(0,0,20,3)
        self.low_life_color=(255,255,0)
        self.low_life_reset=ai_setting.ship_low_life_num
        self.low_life_num=self.low_life_reset
        self.beatable=True
        self.beatable_time=ai_setting.beatable_time
        self.beatable_last_time=time.time()
        self.vanish_time=0.1
        self.vanish_last_time=time.time()
        self.come_in_time=0.1
        self.come_in_last_time = time.time()
        self.come_in=True
        self.vanish=False

        self.hight = ai_setting.screen_hight
        self.width = ai_setting.screen_width

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.fire_rect.centerx = self.rect.centerx
        self.fire_rect.top = self.rect.bottom

        self.speed = ai_setting.ship_speed
        self.moving_right = False
        self.moving_light = False
        self.moving_up = False
        self.moving_dowm = False
        self.keep_fire = False

    def ship_move(self,boom_cartoon):
        if boom_cartoon.activate==False:
            if self.moving_light:
                if self.rect.centerx > 0:
                    self.rect.centerx -= self.speed
            if self.moving_right:
                if self.rect.centerx < self.width:
                    self.rect.centerx += self.speed
            if self.moving_up:
                if self.rect.top > 0:
                    self.rect.centery -= self.speed
            if self.moving_dowm:
                if self.rect.bottom < self.hight:
                    self.rect.centery += self.speed
            self.fire_rect.centerx = self.rect.centerx
            self.fire_rect.top = self.rect.bottom

    def blitme(self,fire=True):
        self.screen.blit(self.image, self.rect)
        if fire:
            self.fire_image = pygame.transform.flip(self.fire_image, True, False)
            self.screen.blit(self.fire_image, self.fire_rect)

    def live_biltme(self):
        for i in range(0, self.life):
            self.life_rect.top = 15;
            self.life_rect.centerx = 15 + self.life_rect.width / 2 + i * self.life_rect.width
            self.screen.blit(self.image, self.life_rect)

    def could_fire(self, y, bullet_number):
        if (self.rect.top - y) > bullet_number:
            return True
        else:
            return False

    def draw_low_life(self):
        self.low_life_rect.bottom=self.hight-15
        self.low_life_rect.right=self.width-15
        for i in range(0,self.low_life_num):
            pygame.draw.rect(self.screen,self.low_life_color,self.low_life_rect)
            self.low_life_rect.bottom-=5+self.low_life_rect.height

    def ship_come_in(self):
        if self.come_in:
            self.rect.top=self.screen_rect.bottom
            self.rect.centerx=self.screen_rect.centerx
            self.come_in=False
        if time.time()-self.come_in_last_time>=self.come_in_time and self.rect.bottom>self.screen_rect.bottom:
            self.rect.top-=4
            self.come_in_last_time=time.time()

class Alien(Sprite):
    def __init__(self, screen, ai_setting):
        super(Alien, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('resources/alien2.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.hight = ai_setting.screen_hight
        self.width = ai_setting.screen_width
        self.last_location = self.rect.centery
        self.transform = ai_setting.alien_transform
        self.life = ai_setting.alien_life
        self.point= ai_setting.alien_point

        self.rect.centerx = random.randint(0, self.width)
        self.rect.bottom = self.screen_rect.top
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.speed = ai_setting.alien_speed
        self.moving_down = False
        self.moving_right = False
        self.moving_light = False
        self.moving_flag = True

    def alien_move(self):
        if self.moving_down:
            self.centery += self.speed
        if self.moving_light:
            if self.rect.centerx < 0:
                self.moving_light = False
                self.moving_right = True
            else:
                self.centerx -= self.speed
        if self.moving_right:
            if self.rect.centerx > self.width:
                self.moving_light = True
                self.moving_right = False
            else:
                self.centerx += self.speed
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def ai_alien(self):
        if bool(random.randint(0, 1)) and self.moving_flag:
            self.moving_down = True
            self.moving_light = True
            self.moving_flag = False
        elif self.moving_flag:
            self.moving_down = True
            self.moving_right = True
            self.moving_flag = False
        if self.rect.centery - self.last_location > self.transform:
            self.last_location = self.rect.centery
            if self.moving_light:
                self.moving_light = False
            else:
                self.moving_light = True
            if self.moving_right:
                self.moving_right = False
            else:
                self.moving_right = True

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.alien_move()
        self.ai_alien()

class Background_Stars(Sprite):
    def __init__(self, screen, ai_setting):
        super(Background_Stars, self).__init__()
        self.star_rect = pygame.Rect(0, 0, 2, 2)
        self.star_rect.centerx = random.randint(0, ai_setting.screen_width)
        self.star_rect.bottom = 0
        self.star_speed = 1.5
        self.screen = screen
        self.star_color = [255, 255, 255]
        self.centery = float(self.star_rect.centery)

    def update(self):
        self.centery += self.star_speed
        self.star_rect.centery = self.centery

    def draw_background(self):
        self.update()
        pygame.draw.rect(self.screen, self.star_color, self.star_rect)

def loade_image(file,number):
    image_list=[]
    image_rect_list=[]
    for i in range(1,number):
        load_file=file+str(i)+'.png'
        image=pygame.image.load(load_file)
        image_list.append(image)
        image_rect_list.append(image.get_rect())
    return [image_list,image_rect_list]

class BoomCartoon():
    def __init__(self,screen):
        self.file='boom\\boom'
        self.image_num=16
        self.image_list,self.image_rect_list=loade_image(self.file,self.image_num)
        self.order=-1
        self.last_time=time.time()
        self.time=0.1
        self.screen=screen
        self.activate=False

    def update(self):
        if (self.order<self.image_num) and (time.time()-self.last_time>self.time) and self.activate:
            self.order+=1
            self.last_time=time.time()
        if self.order>=self.image_num-1:
            self.activate=False
            self.order=-1

    def blitme(self,ship):
        self.update()
        if self.activate:
            boom_sound()
            self.image_rect_list[self.order].centerx = ship.rect.centerx
            self.image_rect_list[self.order].centery = ship.rect.centery
            self.screen.blit(self.image_list[self.order],self.image_rect_list[self.order])

class AlienBoomCartoon(Sprite):
    def __init__(self,screen,alien):
        super(AlienBoomCartoon, self).__init__()
        self.file='boom\\boom'
        self.image_num=16
        self.image_list,self.image_rect_list=loade_image(self.file,self.image_num)
        self.order=-1
        self.last_time=time.time()
        self.time=0.1
        self.screen=screen
        self.kill=False
        self.alien=alien

    def update(self):
        if (self.order<self.image_num) and (time.time()-self.last_time>self.time) and (self.kill is False):
            self.order+=1
            self.last_time=time.time()
        if self.order>=self.image_num-1:
            self.kill=True

    def blitme(self):
        self.update()
        if self.kill==False:
            boom_sound()
            self.image_rect_list[self.order].center = self.alien.rect.center
            self.screen.blit(self.image_list[self.order],self.image_rect_list[self.order])

class Boom():
    def __init__(self, screen):
        self.image_hit = pygame.image.load('resources/boom2.png')
        self.rect_hit = self.image_hit.get_rect()
        self.rect_hit.centerx=-100
        self.rect_hit.centery=-100
        self.screen = screen
        self.last_time = time.time()

    def set(self, bullet_class):
        self.rect_hit.centerx = bullet_class.rect.centerx
        self.rect_hit.centery = bullet_class.rect.top

    def select(self,alien_life=0):
        if alien_life<=0:
            self.rect_hit.centerx = -100
            self.rect_hit.centery = -100

    def blitme(self):
            self.screen.blit(self.image_hit,self.rect_hit)

    def clear_boom(self):
        if time.time() - self.last_time > 0.5:
            self.rect_hit.centerx = -100
            self.rect_hit.centery = -100
            self.last_time = time.time()

class Button():
    def __init__(self,ai_setting,screen):
        self.screen=screen
        self.image=pygame.image.load('resources/start.png')
        self.image_push=pygame.image.load('resources/start2.png')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        self.rect.center=self.screen_rect.center
        self.pushed=False
        self.push = False

    def blitme(self):
        if self.push:
            self.screen.blit(self.image_push,self.rect)
        else:
            self.screen.blit(self.image,self.rect)

def gun_sound():
    sound = pygame.mixer.Sound('resources/gun3.wav')
    sound.set_volume(0.2)
    sound.play()

def boom_sound():
    sound = pygame.mixer.Sound('resources/boom.wav')
    sound.set_volume(1.5)
    sound.play()

def aliens_make(aliens, screen, ai_setting):
    if random.randint(0, 1000) % 500 == 0:
        new_alien = Alien(screen, ai_setting)
        aliens.add(new_alien)

def fire(list_bullets, bullets, ai_setting, screen, ship,boom_cartoon):
    if ship.keep_fire and boom_cartoon.activate==False:
        if len(list_bullets) == 0:
            new_bullet = Bullet(ai_setting, screen, ship)
            bullets.add(new_bullet)
            gun_sound()
        elif ship.could_fire(list_bullets[-1].y, ai_setting.bullet_number):
            new_bullet = Bullet(ai_setting, screen, ship)
            bullets.add(new_bullet)
            gun_sound()

def alien_fire(aliens,screen,ai_setting,aliens_bullets):
    if random.randint(0,100)%50==0:
        if len(aliens.sprites()):
            alien = random.choice(aliens.sprites())
            new_alien_buttle = AlienBullet(ai_setting, screen,alien)
            aliens_bullets.add(new_alien_buttle)

def my_spritecollide(sprite, group, game_stats,aliens_boom_cartoon,screen):
        crashed = []
        append = crashed.append
        spritecollide = sprite.rect.colliderect
        for s in group.sprites():
            if spritecollide(s.rect):
                s.life -= 1
                if s.life == 0:
                    game_stats.score+=s.point
                    new_alien_boom_cartoon=AlienBoomCartoon(screen,s)
                    aliens_boom_cartoon.add(new_alien_boom_cartoon)
                    s.kill()
                append(s)
        return crashed

def my_groupcollide(groupa, groupb, game_stats,aliens_boom_cartoon,screen):
    crashed = {}
    SC = my_spritecollide
    for s in groupa.sprites():
        c = SC(s, groupb, game_stats,aliens_boom_cartoon,screen)
        if c:
            crashed[s] = c
            s.kill()
    return crashed

def check_collid(aliens,ship,aliens_bullets,aliens_boom_cartoon,boom_cartoon,screen):
    aliens_list=[]
    if ship.beatable:
        aliens_list=pygame.sprite.spritecollide(ship, aliens, True)
        for sprite in aliens_list:
            new_alien_boom_cartoon = AlienBoomCartoon(screen, sprite)
            aliens_boom_cartoon.add(new_alien_boom_cartoon)
    aliens_bullets_list = pygame.sprite.spritecollide(ship, aliens_bullets, True)
    if (pygame.sprite.spritecollideany(ship,aliens) or len(aliens_bullets_list) or len(aliens_list)) and ship.beatable:
        ship.low_life_num-=1
        if ship.low_life_num==0:
            ship.life-=1
            ship.low_life_num=ship.low_life_reset
            boom_cartoon.activate=True
        ship.beatable_last_time=time.time()
        ship.beatable=False
    if ship.beatable==False:
        if time.time()-ship.beatable_last_time>ship.beatable_time:
            ship.beatable=True

def bullet_update(bullets, aliens, game_stats,aliens_boom_cartoon,screen):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collision = my_groupcollide(bullets, aliens, game_stats,aliens_boom_cartoon,screen)
    bullet_list = list(collision.keys())
    aliens_list=list(collision.values())
    if len(bullet_list):
        boom_sound()
        return [bullet_list,aliens_list]

def alien_update(aliens, screen_hight):
    for alien in aliens.copy():
        if alien.rect.top > screen_hight:
            aliens.remove(alien)

def alien_bullet_update(aliens_bullets, screen_hight):
    for alien_bullet in aliens_bullets.copy():
        if alien_bullet.position[1] > screen_hight:
            aliens_bullets.remove(alien_bullet)

def stars_updata(background_stars, screen_hight):
    for star in background_stars.copy():
        if star.star_rect.top > screen_hight:
            background_stars.remove(star)

def aliens_boom_cartoon_updata(aliens_boom_cartoon):
    for alien_boom_cartoon in aliens_boom_cartoon:
        if alien_boom_cartoon.kill:
            aliens_boom_cartoon.remove(alien_boom_cartoon)

def stars_make(background_stars, screen, ai_setting):
    if random.randint(0, 100) % 50 == 0:
        new_star = Background_Stars(screen, ai_setting)
        background_stars.add(new_star)

def check_events(ship):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            if event.key == pygame.K_LEFT:
                ship.moving_light = True
            if event.key == pygame.K_UP:
                ship.moving_up = True
            if event.key == pygame.K_DOWN:
                ship.moving_dowm = True
            if event.key == pygame.K_SPACE:
                ship.keep_fire = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            if event.key == pygame.K_LEFT:
                ship.moving_light = False
            if event.key == pygame.K_UP:
                ship.moving_up = False
            if event.key == pygame.K_DOWN:
                ship.moving_dowm = False
            if event.key == pygame.K_SPACE:
                ship.keep_fire = False

def check_play_events(stats,play_button):
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            if  play_button.rect.collidepoint(mouse_x,mouse_y):
                play_button.pushed=True
                play_button.push=True
        if event.type==pygame.MOUSEBUTTONUP and play_button.pushed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            play_button.push = False
            if play_button.rect.collidepoint(mouse_x, mouse_y) and play_button.pushed:
                stats.game_active=True
                play_button.pushed=False


def update_screen(ai_setting, ship, aliens, screen, bullets, boom, background_stars,scoreboard,game_stats,
                  aliens_bullets,boom_cartoon,aliens_boom_cartoon,alien_class=None):
    screen.fill(ai_setting.bg_color)
    for alien_boom_cartoon in aliens_boom_cartoon.sprites():
        alien_boom_cartoon.blitme()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien in aliens.sprites():
        alien.blitme()
    for star in background_stars.sprites():
        star.draw_background()
    for alien_bullet in aliens_bullets.sprites():
        alien_bullet.draw_bullet()
    if ship.beatable==False:
        if time.time()-ship.vanish_last_time>ship.vanish_time:
            if ship.vanish==False:
                ship.vanish=True
            else:
                ship.vanish=False
            ship.vanish_last_time = time.time()
    else:
        ship.vanish=False
    if ship.vanish==False and boom_cartoon.activate==False:
        ship.blitme()
    ship.live_biltme()
    ship.draw_low_life()
    if  alien_class:
        boom.select(alien_class[0][0].life)
    boom_cartoon.blitme(ship)
    boom.clear_boom()
    boom.blitme()
    scoreboard.show_score()

    pygame.display.flip()

def start_acreen(screen,ai_setting,background_stars,stats,ship,scoreboard):
    screen.fill(ai_setting.bg_color)
    for star in background_stars.sprites():
        star.draw_background()
    stats.blitme()
    ship.blitme(False)
    scoreboard.show_score()

    pygame.display.flip()

def reset_game_data(ship,aliens,bullets,aliens_bullets,ai_setting):
    ship.life=ai_setting.ship_life
    ship.low_life=ai_setting.ship_low_life_num
    ship.moving_right = False
    ship.moving_light = False
    ship.moving_up = False
    ship.moving_dowm = False
    ship.keep_fire = False
    aliens.empty()
    bullets.empty()
    aliens_bullets.empty()

def run_game():
    pygame.init()
    pygame.mixer.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_hight))
    pygame.display.set_caption(ai_setting.caption)
    pygame.mixer.music.load('resources/background.mid')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)

    ship = Ship(screen, ai_setting)
    boom = Boom(screen)
    game_stats=GameStats()
    scoreboard=Scoreboard(screen,ai_setting,game_stats)
    bullets = Group()
    aliens = Group()
    aliens_bullets=Group()
    background_stars = Group()
    boom_cartoon=BoomCartoon(screen)
    play_button=Button(ai_setting,screen)
    aliens_boom_cartoon=Group()
    fcclock = pygame.time.Clock()

    while True:

        if game_stats.game_active:
            check_events(ship)
            list_bullets = bullets.sprites()

            bullet_class_list = []
            alien_class_list = []
            ship.ship_move(boom_cartoon)
            bullets.update()
            bullet_alien_class = bullet_update(bullets, aliens,game_stats,aliens_boom_cartoon,screen)
            if bullet_alien_class:
                bullet_class_list=bullet_alien_class[0]
                alien_class_list=bullet_alien_class[1]
            if bullet_class_list:
                boom.set(bullet_class_list[0])
            fire(list_bullets, bullets, ai_setting, screen, ship,boom_cartoon)
            alien_fire(aliens,screen,ai_setting,aliens_bullets)
            aliens_make(aliens, screen, ai_setting)
            aliens.update()
            aliens_bullets.update()
            stars_make(background_stars, screen, ai_setting)
            stars_updata(background_stars, ai_setting.screen_hight)
            alien_bullet_update(aliens_bullets, ai_setting.screen_hight)
            check_collid(aliens,ship,aliens_bullets,aliens_boom_cartoon,boom_cartoon,screen)
            boom_cartoon.update()
            if ship.life<=0 and len(aliens_boom_cartoon.sprites()) and boom_cartoon.activate==False:
                game_stats.game_active=False
                ship.come_in=True
                game_stats.last_score=game_stats.score

            update_screen(ai_setting, ship, aliens, screen, bullets, boom, background_stars,scoreboard,
                          game_stats,aliens_bullets,boom_cartoon,aliens_boom_cartoon,alien_class_list)
        else:
            game_stats.reset_stats()
            reset_game_data(ship,aliens,bullets,aliens_bullets,ai_setting)
            ship.ship_come_in()
            check_play_events(game_stats,play_button)
            stars_make(background_stars, screen, ai_setting)
            stars_updata(background_stars, ai_setting.screen_hight)
            start_acreen(screen,ai_setting,background_stars,play_button,ship,scoreboard)
        fcclock.tick(60)
run_game()
