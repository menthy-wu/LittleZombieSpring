import pygame,sys,time,os
from load_img import *
from zombie import *
class CLS_level_1(object):
    def __init__(self,scr,clock):
        self.clock = clock
        self.finish = 0
        self.hb = load_img('1 绘本.jpg',(286,75),(151,151,151))
        self.hb_fanzhuan =pygame.transform.flip(self.hb ,True,False)
        self.hb_size = [95,45]
        self.bg1 = load_img('1 bg 1.jpg',(1720,540),(255,255,255))
        self.bg2 = load_img('1 bg 2.jpg',(1720,540),(150,150,150))
        self.bg3 = load_img('1 bg 3.jpg',(1720,540),(81,81,81))
        self.bg4 = load_img('1 bg 4.jpg',(1720,540),(33,33,33))
        self.hb_x = 1012
        self.hb_y = 480
        self.bg1_x = 0
        self.spd1 = 0.1
        self.bg2_x = 0
        self.spd2 = 0.5
        self.bg3_x = 0
        self.spd3 = 1
        self.bg4_x = 0
        self.spd4 = 1.5
        self.scr = scr
        self.zb = CLS_zombie(scr,5,245,134,283,0)
        self.pick_hb = 0
        self.tishi = 0
        self.hb_derection = 0
        self.hb_play = 0
        self.pick_tishi = 0
        self.huiben = CLS_huiben1(scr)
        return
    def draw(self,scr):
        if self.finish == 1:
            return
        if self.huiben.finish == 1 :
            self.zb.current[0] = 2
            while True:
                self.zb.x+=self.zb.spd
                scr.blit(self.bg1,(self.bg1_x,-38))
                scr.blit(self.bg2,(self.bg2_x,-25))
                scr.blit(self.bg3,(self.bg3_x,-13))
                scr.blit(self.bg4,(self.bg4_x,0))
                self.zb.draw(scr)
                pygame.display.update()
                if self.zb.x>860:
                    r = 0
                    while True:
                        r+=1
                        pygame.draw.circle(scr,(0,0,0),(430,270),r,0)
                        pygame.display.update()
                        if r == 860:
                            break
                    self.finish = 1
                    return
                    break
        if self.hb_play == 1 and self.huiben.finish == 0:
            self.huiben.hb_draw(scr)
            return 
        scr.blit(self.bg1,(self.bg1_x,-38))
        scr.blit(self.bg2,(self.bg2_x,-25))
        scr.blit(self.bg3,(self.bg3_x,-13))
        scr.blit(self.bg4,(self.bg4_x,0))
        self.zb.draw(scr)
        if self.pick_hb == 1 and self.zb.hand!=None:
            if self.hb_derection == 0:
                scr.blit(self.hb,(self.zb.hand[0],self.zb.hand[1]))
            elif self.hb_derection == 1:
                scr.blit(self.hb_fanzhuan,(self.zb.hand[0]-200,self.zb.hand[1]))
        else:
            scr.blit(self.hb,(self.hb_x,self.hb_y))
        if self.tishi == 0:
            font24 = pygame.font.Font('G0v1.otf', 20)
            img_text = font24.render('鼠标点击控制移动',True,(255,255,255))
            scr.blit( img_text ,(150,250))
        if self.pick_hb == 0:
            font24 = pygame.font.Font('G0v1.otf', 20)
            img_text = font24.render('鼠标点击捡起',True,(255,255,255))
            scr.blit( img_text ,(self.hb_x,self.hb_y-50))
        if self.pick_tishi == 1:
            font24 = pygame.font.Font('G0v1.otf', 20)
            img_text = font24.render('按空格查看',True,(255,255,255))
            scr.blit( img_text ,(480,270))
            
        return
    def mousedown(self,mx,my):
        if self.hb_play == 1 and self.huiben.finish == 0:
            self.huiben.mousedown(mx,my)
            return
        self.tishi = 1
        if self.zb.x<mx:
            self.hb_derection = 0
            self.zb.current[0] = 2
            while True:
                if self.zb.x>=mx-self.zb.w:
                    break
                self.zb.x+=self.zb.spd
                self.bg1_x-=self.spd1
                self.bg2_x-=self.spd2
                self.bg3_x-=self.spd3
                self.bg4_x-=self.spd4
                self.hb_x-=self.spd4
                self.draw(self.scr)
                pygame.display.update()
            self.zb.current[0] = 0
        elif self.zb.x>mx:
            self.hb_derection = 1
            self.zb.current[0] = 3
            while True:
                if self.zb.x<=mx:
                    break
                self.zb.x-=self.zb.spd
                self.bg1_x+=self.spd1
                self.bg2_x+=self.spd2
                self.bg3_x+=self.spd3
                self.bg4_x+=self.spd4
                self.hb_x+=self.spd4
                self.draw(self.scr)
                pygame.display.update()
            self.zb.current[0] = 1
        if self.hb_x<mx<self.hb_size[0]+self.hb_x and 480<my<self.hb_size[1]+480:
            self.pick_tishi = 1
            self.zb.handle = self.hb
            self.zb.current = [4,0]
            self.pick_hb = 1
            return
        return
    def mouseup(self,mx,my):
        return
    def keydown(self,key):
        #print(key)
        if key == 32:#空格
            if self.zb.handle == self.hb:
                self.pick_tishi = 0
                self.hb_play = 1
        return
    def keyup(self,key):
        return
class CLS_huiben1(object):
    def __init__(self,scr):
        hbList = ['绘本1.jpg','绘本2.jpg','绘本3.jpg','绘本4.jpg',\
                  '绘本5.jpg','绘本6.jpg','绘本7.jpg','绘本8.jpg',\
                  '绘本9.jpg','绘本10.jpg','绘本11.jpg']
        self.hbList = []
        self.start = 0
        for hb in hbList:
            self.hbList.append(load_img(hb,(860,540),None))
        self.tick = 0
        self.r = 0
        self.current = 0
        self.play = 0
        self.sound = 0
        self.finish = 0
    def hb_draw(self,scr):
        if self.start == 0:
            if self.r == 860:
                self.start = 1
            self.tick+=1
            if self.tick%2 == 1:
                self.r+=1
            pygame.draw.circle(scr,(255,255,255),(430,270),self.r,0)
            return
        if self.play == 0:
            if self.current == 0:
                draw_picture(scr,self.hbList[self.current],400)
            else:
                draw_picture(scr,self.hbList[self.current],0)
            self.play = 1
        else:
            scr.blit(self.hbList[self.current],(0,0))
        if self.current == 7:
            draw_picture(scr,self.hbList[8],630)
            self.current = 8
        if self.current == 8:
            draw_picture(scr,self.hbList[9],630)
            self.current = 9
        if self.current == 9:
            font24 = pygame.font.Font('G0v1.otf', 20)
            img_text = font24.render('这。。。是我?',True,(85,65,55))
            heartbeat = pygame.mixer.Sound('heartbeat.ogg')
            if self.sound == 0:
                heartbeat.play()
                self.sound = 1
            scr.blit( img_text ,(471,418))
    def mousedown(self,mx,my):
        print('hi',mx,my)
        if self.start == 0:
            return
        if 782<mx<845 and 226<my<306 and self.current <7:
            self.current +=1
            self.play = 0
        if 782<mx<845 and 226<my<306 and self.current ==9:
            self.current +=1
            self.play = 0
            return
        if 782<mx<845 and 226<my<306 and self.current ==10:
            self.finish = 1
        if 18<mx<79 and 232<my<301 and self.current != 0 and self.current != 8 and self.current != 9:
            self.current -=1
            self.play = 0
        if 18<mx<79 and 232<my<301 and self.current ==10:
            self.current =7
            self.play = 0
        return
''' 
SCREEN_W,SCREEN_H = 860, 540
pygame.init()
screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))
pygame.display.set_caption("level1")
level1 = CLS_level_1(screen)
clock = pygame.time.Clock()

while True:
    level1.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            level1.mousedown(event.pos[0],event.pos[1])
            print(event.pos[0],event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            level1.mouseup(event.pos[0],event.pos[1])
        elif event.type == pygame.KEYDOWN:
            level1.keydown(event.key) 
        elif event.type == pygame.KEYUP:
            level1.keyup(event.key)
    pygame.display.update()
    clock.tick( 1000 ) '''
