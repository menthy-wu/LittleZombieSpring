import pygame, sys, time
from intro import *
from start import *
from level1 import *
from level2 import *
from level3 import *
from level4 import *
SCREEN_W,SCREEN_H = 860, 540

class CLS_framework(object):
    def __init__(self,scr,clock):
        self.click = pygame.mixer.Sound('click1.wav')
        self.current = 0
        self.modList = []
        intro = CLS_intro()
        start = CLS_Start('1 世界末日.jpg')
        level1 = CLS_level_1(scr,clock)
        level2 = CLS_level2(scr,clock)
        level3 = CLS_level3(scr,clock)
        level4 = CLS_level4(scr,clock)
        self.modList = [start,intro,level1,level2,level3,level4]
    def mousedown(self,mx,my): 
        self.click.play()
        self.modList[self.current].mousedown(mx,my)
    def mouseup(self,mx,my):
        self.modList[self.current].mouseup(mx,my)
    def mousemotion(self,mx,my):
        try: 
            self.modList[self.current].mousemotion(mx,my)
        except:
            return
    def draw(self,scr):
        self.modList[self.current].draw(scr)
    def play(self):
        if self.modList[self.current].finish == 1 and self.current+1<len(self.modList):
            self.current+=1
    def keydown(self,key):
        self.modList[self.current].keydown(key)
    def keyup(self,key):
        self.modList[self.current].keyup(key)
        

pygame.init()
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
pygame.display.set_caption("小僵尸的春天")
clock = pygame.time.Clock()
pygame.mixer.music.load('Winds Of Stories.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops = -1)
framework = CLS_framework(screen,clock)

#——————————————————————————————main————————————————————
while True:
    framework.draw(screen)
    framework.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            framework.mousedown(event.pos[0],event.pos[1])
        elif event.type == pygame.MOUSEMOTION:
            framework.mousemotion(event.pos[0],event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            framework.mouseup(event.pos[0],event.pos[1])
        elif event.type == pygame.KEYDOWN:
            framework.keydown(event.key)
        elif event.type == pygame.KEYUP:
            framework.keyup(event.key)
    pygame.display.update()
    clock.tick( 1000 )
            
