import pygame as py
import random as r

class Player(py.sprite.Sprite):
    def __init__(self):
        super().__init__()
        rocket_pic=py.image.load("graphics/main rocket.png")
        rocket_pic=py.transform.rotozoom(py.transform.scale(rocket_pic,(50,60)),270,1)
        self.image=rocket_pic
        self.rect=self.image.get_rect(midbottom=(80,200))

        self.lasers=py.sprite.Group()


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

    def shoot_laser(self):
        self.lasers.add(laser(self.rect.center))

    def update(self):
        self.input()
        self.border()

class laser(py.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        blast_pic = py.image.load("graphics/blast.jpg")
        blast_pic = py.transform.scale(blast_pic, (20, 10))
        self.image=blast_pic
        self.rect=self.image.get_rect(center=pos)

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
        if self.rect.x<=-100:
            self.kill()