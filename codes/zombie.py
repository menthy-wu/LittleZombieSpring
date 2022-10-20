
from load_img import *
import pygame,sys,time,os



class CLS_zombie(object):
    def __init__(self,scr,x,y,w,h,num):
        self.sound_step = pygame.mixer.Sound('step.ogg')
        self.sound_step.set_volume(0.1)
        self.w,self.h = w,h
        walkList_r = ['zbr walk1.jpg','zbr walk2.jpg','zbr walk3.jpg',\
              'zbr walk4.jpg','zbr walk5.jpg','zbr walk6.jpg',\
              'zbr walk7.jpg','zbr walk8.jpg','zbr walk9.jpg',]  
        stop_r = 'zbr stop.jpg'
        walkList_l = ['zbl walk1.jpg','zbl walk2.jpg','zbl walk3.jpg',\
                      'zbl walk4.jpg','zbl walk5.jpg','zbl walk6.jpg',\
                      'zbl walk7.jpg','zbl walk8.jpg','zbl walk9.jpg',]
        stop_l = 'zbl stop.jpg'
        pickList_r = ['zbr pick1.jpg','zbr pick2.jpg','zbr pick3.jpg','zbr pick2.jpg','zbr pick1.jpg']
        self.walkList_r = [] 
        self.walkList_l = []
        self.pickList_r = []
        scr.blit(load_img('1 世界末日.jpg',(860,540),None),(0,0))
        font = pygame.font.Font('G0v1.otf', 20)
        img_text = font.render('正在初始化'+str(num)+'/6',True,(255,255,255))
        scr.blit( img_text ,(130,220))
        pygame.draw.rect(scr,(255,255,255),(130,250,600,20),2)
        n = 0
        self.sound = 0
        for walk in range(9):
            self.walkList_r.append(load_img(walkList_r[walk],(self.w,self.h),(50,80,90)))
            self.walkList_l.append(load_img(walkList_l[walk],(self.w,self.h),(50,80,90)))
            pygame.draw.rect(scr,(255,255,255),(130,250,600/14*n,20),0)
            pygame.display.update()
            n+=1
        for pick in range(5):
            n+=1
            self.pickList_r.append(load_img(pickList_r[pick],(self.w,self.h),(50,80,90)))
            pygame.draw.rect(scr,(255,255,255),(130,250,600/14*n,20),0)
            pygame.display.update()
        self.stop_r = load_img(stop_r,(self.w,self.h),(50,80,90))
        self.stop_l = load_img(stop_l,(self.w,self.h),(50,80,90))
        self.current = [0,0]  #0:stop_r   1:stop_l   2:walk_r   3:walk_l  4:pick_r
        self.systick = 0
        self.spd = 2
        self.x,self.y = x,y
        self.handle = None
        self.hand = None
    def draw(self,scr):
        self.systick += 1
        if self.current[0] == 0:
            scr.blit(self.stop_r,(self.x,self.y))
            self.hand = (self.x+30,self.y+150)
        elif self.current[0] == 1:
            self.hand = (self.x+30,self.y+150)
            scr.blit(self.stop_l,(self.x,self.y))
        elif self.current[0] == 2:
            self.hand = (self.x+30,self.y+150)
            if self.sound == 0:
                if self.current[1]%len(self.walkList_r) == 2 or self.current[1]%len(self.walkList_r) == 6:
                    self.sound_step.play()
                    self.sound = 1
            if self.current[1]%len(self.walkList_r) == 3 or self.current[1]%len(self.walkList_r) == 7:
                self.sound = 0
            scr.blit(self.walkList_r[self.current[1]%len(self.walkList_r)],(self.x,self.y))
            if self.systick%8 ==4:
                self.current[1]+=1
        elif self.current[0] == 3:
            self.hand = (self.x+30,self.y+150)
            if self.sound == 0:
                if self.current[1]%len(self.walkList_r) == 2 or self.current[1]%len(self.walkList_r) == 6:
                    self.sound_step.play()
                    self.sound = 1
            if self.current[1]%len(self.walkList_r) == 3 or self.current[1]%len(self.walkList_r) == 7:
                self.sound = 0
            scr.blit(self.walkList_l[self.current[1]%len(self.walkList_l)],(self.x,self.y))
            if self.systick%8 ==4:
                self.current[1]+=1
        elif self.current[0] == 4:
            if self.current[1]%len(self.pickList_r) == 0:
                self.hand = None
            elif self.current[1]%len(self.pickList_r) == 1:
                self.hand = None
            elif self.current[1]%len(self.pickList_r) == 2:
                self.hand = (self.x+30,self.y+250)
            elif self.current[1]%len(self.pickList_r) == 3:
                self.hand = (self.x+30,self.y+210)
            elif self.current[1]%len(self.pickList_r) == 4:
                self.current[0] = 0
                self.hand = (self.x+30,self.y+160)
            scr.blit(self.pickList_r[self.current[1]%len(self.pickList_r)],(self.x,self.y))
            if self.systick%20 ==10:
                self.current[1]+=1
                
        return
'''
pygame.init()
screen = pygame.display.set_mode((860, 540))
pygame.display.set_caption("zombie")
zombie = CLS_zombie(screen,5,245,134,283)
screen.fill((255,255,255))
clock = pygame.time.Clock()
while True:
    screen.fill((255,255,255))
    zombie.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos[0],event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
    pygame.display.update()
    clock.tick( 50 ) '''

        
        
