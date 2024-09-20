import pygame as py
from sys import exit
import random as r

#sprite CLASSES
class main_rocket(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos=(80,200)
        rocket_pic=py.image.load("graphics/main rocket.png")
        rocket_pic=py.transform.rotozoom(py.transform.scale(rocket_pic,(50,60)),270,1)
        self.image=rocket_pic
        self.rect=self.image.get_rect(midbottom=self.pos)

    def input(self):
        keys=py.key.get_pressed()
        if keys[py.K_RIGHT] or keys[py.K_d]: self.rect.x+=5
        if keys[py.K_LEFT] or keys[py.K_a]: self.rect.x-=5
        if keys[py.K_DOWN] or keys[py.K_s]: self.rect.y+=5
        if keys[py.K_UP] or keys[py.K_w]: self.rect.y-=5
       

    def border(self):
        if self.rect.x<=0:self.rect.x=0
        if self.rect.y <= 0: self.rect.y= 0
        if self.rect.x >= 750: self.rect.x = 750
        if self.rect.y>=340:self.rect.y=340

    def update(self):
        self.input()
        self.border()

class laser(py.sprite.Sprite):
    global score
    def __init__(self,pos):
        super().__init__()
        blast_pic = py.image.load("graphics/blast.jpg")
        blast_pic = py.transform.scale(blast_pic, (20, 10))
        self.image=blast_pic
        self.rect=self.image.get_rect(center=pos)

    def collide(self):
        global score
        if py.sprite.spritecollide(self,enemy_grp,True):
            score+=1
            

    def update(self):
        self.collide()
        self.rect.x+=10
        if self.rect.x>780:
            self.kill()

class enemies(py.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type==1:
            enemy=py.image.load("graphics/enemy rocket.png")
            enemy=py.transform.scale(enemy,(30,30))
        else:
            enemy = py.image.load("graphics/enemy rocket 2.png")
            enemy = py.transform.scale(enemy, (40, 35))

        self.image=py.transform.rotozoom(enemy,90,1)
        self.rect=self.image.get_rect(center=(r.randint(900,1100),r.randint(30,380)))

    def update(self):
        self.rect.x-=5
        self.destroy()

    def destroy(self):
        if self.rect.x<=-50:
            self.kill()

#FUNCTIONS
def player_collision():
    global score
    if py.sprite.spritecollide(rocket.sprite,enemy_grp,True):
        enemy_grp.empty()
        lasers.empty()
        score=0
        return "game over"

    else:
        return "active"


py.init()
screen = py.display.set_mode((800, 400))
game_state="menu"
clock = py.time.Clock()
py.display.set_caption("SPACE FIGHTER")
font=py.font.Font("font/Arinoe.ttf",100)
font1=py.font.Font("font/NEONLEDLight.otf",100)
button_font=py.font.Font("font/Evil Empire.otf",50)
score=0
laser_sound=py.mixer.Sound("audio/3TRG6M5-laser.mp3")
bg_music=py.mixer.Sound("audio/Naruto - Main Theme.mp3")
bg_music.play(loops=-1)

#COLOURS
restart_button_color="#6a5acd"
menu_button_color="#6a5acd"

#SURFACE AND RECTANGLES
backgrd = py.image.load("graphics/R.png").convert_alpha()
backgrd_rect = backgrd.get_rect(topleft=(0, 0))

crash=py.transform.scale(py.image.load("graphics/rocket crash.png").convert_alpha(),(150,100))


game_over=font.render("GAME OVER",True,"#191970")
game_over_rect=game_over.get_rect(topleft=(200,50))


gametitle=font1.render("SPACE FIGHTER",True,"aquamarine3")

# GROUPS
rocket = py.sprite.GroupSingle()
rocket.add(main_rocket())
enemy_grp = py.sprite.Group()
lasers = py.sprite.Group()

# USEREVENTS
enemy_timer = py.USEREVENT + 1
py.time.set_timer(enemy_timer, 300)

while True:
    #BUTTONS
    restart_button = button_font.render("restart", True, restart_button_color)
    restart_button_rect = restart_button.get_rect(midtop=(game_over_rect.x + 200, game_over_rect.y + 100))
    menu_button = button_font.render("menu", True, menu_button_color)
    menu_button_rect = menu_button.get_rect(midtop=(game_over_rect.x + 200, game_over_rect.y + 200))
    start_button = button_font.render("start", True, restart_button_color)
    start_button_rect=restart_button_rect

    #surfaces
    score_surf = py.transform.scale(font.render(("score:"+str(score)), True, (200, 200, 200)), (60, 30))

    #EVENTLOOP
    for ev in py.event.get():
        if ev.type == py.QUIT:
            py.quit()
            exit()
        if game_state=="active":
            if ev.type == enemy_timer:
                enemy_grp.add(enemies(r.choice([1, 1, 1, 1, 2])))
            if ev.type == py.KEYDOWN:
                if ev.key == py.K_SPACE:
                    if len(lasers) < 3:
                        lasers.add(laser(rocket.sprite.rect.center))
                        laser_sound.play()

            game_state= player_collision()

        elif game_state=="game over":
            mouse_pos=py.mouse.get_pos()
            if restart_button_rect.collidepoint(mouse_pos):
                restart_button_color="#8a2be2"
                if ev.type==py.MOUSEBUTTONDOWN:
                    rocket.add(main_rocket())
                    game_state="active"
            else:
                restart_button_color="#6a5acd"
            if menu_button_rect.collidepoint(mouse_pos):
                menu_button_color="#8a2be2"
                if ev.type == py.MOUSEBUTTONDOWN:
                    game_state = "menu"
            else:
                menu_button_color="#6a5acd"

        else:
            mouse_pos = py.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_pos):
                restart_button_color = "#8a2be2"
                if ev.type == py.MOUSEBUTTONDOWN:
                    rocket.add(main_rocket())
                    game_state = "active"
            else:
                restart_button_color = "#6a5acd"



    screen.blit(backgrd, backgrd_rect)

    if game_state=="active":
        lasers.draw(screen)
        rocket.draw(screen)
        enemy_grp.draw(screen)
        lasers.update()
        rocket.update()
        enemy_grp.update()
        screen.blit(score_surf,(700,350))

    elif game_state=="game over":
        rocket.empty()
        screen.blit(game_over,game_over_rect)
        screen.blit(restart_button,restart_button_rect)
        screen.blit(menu_button, menu_button_rect)
        screen.blit(crash,(100,150))
        screen.blit(crash, (550, 150))

    else:
        screen.blit(gametitle,(30,10))
        screen.blit(start_button,start_button_rect)
        rocket.draw(screen)



    py.display.update()
    clock.tick(60)