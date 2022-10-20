import pygame,sys,time
from zombie import*

class CLS_level3(object):
    def __init__(self,scr,clock):
        self.clock = clock
        self.hb_play = 0
        self.hb = CLS_huiben3(scr)
        self.finish = 0
        ball = '3球.jpg'
        picList = ['3游乐园1.jpg',\
                   '3游乐园2.jpg',\
                   '3游乐园3.jpg',\
                   '3游乐园4.jpg',\
                   '3游乐园5.jpg',\
                   '3游乐园6.jpg',\
                   '3游乐园7.jpg',\
                   '3游乐园8.jpg',\
                   '3游乐园 电路板.jpg']
        dlList = [['3电路0,0.jpg','3电路0,1.jpg','3电路0,2.jpg'],\
                  ['3电路1,0.jpg','3电路1,1.jpg','3电路1,2.jpg'],\
                  ['3电路2,0.jpg','3电路2,1.jpg','3电路2,2.jpg'],\
                  ['3电路3,0.jpg','3电路3,1.jpg','3电路3,2.jpg']]
        self.rList = [[1,0,2],[3,1,1],[2,3,0],[2,3,1]]
        self.rList1 = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.rList2 = [[0,2,0],[0,0,0],[0,0,0],[0,0,0]]
        #x,y 335,104 w,h57,57   2 394
        solar_panel = '3太阳能板120.jpg'
        font = pygame.font.Font('G0v1.otf', 20)
        scr.blit(load_img('1 世界末日.jpg',(860,540),None),(0,0))
        img_text = font.render('正在初始化3/6',True,(255,255,255))
        scr.blit( img_text ,(130,220))
        pygame.draw.rect(scr,(255,255,255),(130,250,600,20),2)
        self.picList = []
        self.dlList = [[],[],[],[]]
        self.current_bg = 0
        n = 0
        for pic in picList:
            n+=1 
            self.picList.append(load_img(pic,(860,540),None))
            pygame.draw.rect(scr,(255,255,255),(130,250,600/22*n,20),0)
            pygame.display.update()
        for p in range(4):
            for pic in dlList[p]:
                n+=1
                self.dlList[p].append(load_img(pic,(57,57),None))
                pygame.draw.rect(scr,(255,255,255),(130,250,600/22*n,20),0)
                pygame.display.update()
        self.ball = load_img(ball,(36,36),(255,255,255))
        self.solar_panel = load_img(solar_panel,(75,36),(120,120,120))
        self.solar_panel_fanzhuan = pygame.transform.flip(self.solar_panel ,True,False)
        n+=1
        pygame.draw.rect(scr,(255,255,255),(130,250,600/22*n,20),0)
        pygame.display.update()

        self.scr = scr
        self.zb = CLS_zombie(scr,-150,245,134,283,4)
        self.solar_panel_down = 0#太阳能板掉下来了没
        self.solar_panel_pick = 0#太阳能板捡起来了没
        self.derection = 0 #手上工具的方向
        self.wtd_tishi = 0  #还未通电提示
        self.tick = 0
        self.use_solar_panel = 0#放上太阳能板
        self.dl_pass = 0 #电路pass
        self.ball_pick=0
        return
    def draw(self,scr):
        if self.finish == 1:
            return
        if self.hb_play == 1 and self.hb.finish == 0:
            if self.hb.start == 0:
                r = 0
                while True:
                    r+=1
                    pygame.draw.circle(scr,(255,255,255),(430,260),r,0)
                    pygame.display.update()
                    if r>860:
                        self.draw_circle =1
                        self.hb.start = 1
                        break
            self.hb.hb_draw(scr)
            return
        if self.hb.finish == 1:
            self.zb.current[0] = 2
            while True:
                self.clock.tick( 100 )
                self.zb.x+=self.zb.spd
                scr.blit(self.picList[self.current_bg],(0,0))
                self.zb.draw(scr)
                pygame.display.update()
                if self.zb.x>860:
                    r= 0
                    while True:
                        r+=1
                        pygame.draw.circle(scr,(0,0,0),(430,260),r,0)
                        pygame.display.update()
                        if r>860:
                            self.draw_circle =1
                            self.hb.start = 1
                            break
                    self.finish = 1
                    return
        if self.current_bg == 3 and self.tick == 100:
            self.current_bg = 4
            self.tick = 0
        if self.current_bg == 4 and self.tick == 100:
            self.current_bg = 5
            self.tick = 0
        if self.current_bg == 5 and self.tick == 100:
            self.current_bg = 6
            self.tick = 0
        self.tick+=1
        self.clock.tick( 100 ) 
        scr.blit(self.picList[self.current_bg],(0,0))
        if self.current_bg !=8:
            self.zb.draw(scr)
        if self.zb.x<0:
            self.zb.current[0] = 2
            self.zb.x+=self.zb.spd
            if self.zb.x >= 0:
                self.zb.current[0] = 0
        if self.solar_panel_down == 1 and self.solar_panel_pick == 0:  
            scr.blit(self.solar_panel,(75,490))   #太阳能板掉下来
        if self.solar_panel_pick == 1 and self.use_solar_panel == 0 and self.solar_panel_down==1:  #捡起太阳能板
            if self.zb.hand!=None:
                if self.derection==0:
                    scr.blit(self.solar_panel,self.zb.hand)
                if self.derection==1:
                    scr.blit(self.solar_panel_fanzhuan,self.zb.hand)
        if self.wtd_tishi == 1:        #还未通电
            if self.tick == 50:
                self.wtd_tishi = 0
            font = pygame.font.Font('G0v1.otf', 15)
            img_text = font.render('还未通电',True,(255,255,255))
            scr.blit( img_text ,(130,315))
        if self.current_bg == 8:      #电路板
            #x,y 335,104 w,h57,57   2 394
            x1,y1,w = 335,104,57
            for y in range(4):
                for x in range(3):
                    img = self.dlList[y][x]
                    if self.rList == self.rList1 or self.rList == self.rList2:
                        self.dl_pass= 1
                    for r in range(self.rList[y][x]):
                        img = pygame.transform.rotate(img,90 )
                    scr.blit( img ,(x1+x*(w+2),y1+y*(w+2)))
        if self.ball_pick == 1:
            scr.blit(self.ball,self.zb.hand)
        return
    def mousedown(self,mx,my):
        if self.finish == 1:
            return
        if self.hb_play == 1 and self.hb.finish == 0:
            self.hb.mousedown(mx,my)
            return
        if self.current_bg == 6 and 450<mx<486 and 323<my<359:   #拿球
            self.handle = self.ball
            self.ball_pick = 1
            self.current_bg = 7
        if self.current_bg == 8 and 335<mx<572 and 104<my<340:    #电路板
            x = (mx-335)//59
            y = (my-335)//59
            self.rList[y][x] +=1
            if self.rList[y][x] == 4:
                self.rList[y][x] =0
        print(self.dl_pass)
        if self.dl_pass == 1 and 390<mx<461 and 403<my<474:   #红色按钮
            self.current_bg = 3
            self.tick = 0
        if 145<mx<167 and 338<my<395 and self.solar_panel_pick == 0 :
            self.wtd_tishi = 1#未通电提示
            self.tick = 0
            return
        if 145<mx<167 and 338<my<395 and self.solar_panel_pick == 1 and self.use_solar_panel ==0:
            self.use_solar_panel = 1#放上太阳能板
            self.current_bg = 2
            return
        if 71<mx<204 and 147<my<240:  #让太阳能板掉下来
            self.current_bg = 1
            self.solar_panel_down = 1
            return
        if self.use_solar_panel == 1  and 145<mx<167 and 338<my<395:#激活电路板：
            self.current_bg = 8
            return
        if self.zb.x<mx-self.zb.w:   #向右走
            self.derection = 0
            self.zb.current[0] = 2
            while True:
                if self.zb.x>=mx-self.zb.w:
                    self.zb.current[0] = 0
                    break
                self.zb.x+=self.zb.spd
                self.draw(self.scr)
                pygame.display.update()
        if self.zb.x>mx:             #向左走
            self.zb.current[0] = 3
            self.derection = 1
            while True:
                if self.zb.x<=mx:
                    self.zb.current[0] = 1
                    break
                self.zb.x-=self.zb.spd
                self.draw(self.scr)
                pygame.display.update()
        if 75<mx<150 and 490<my<490+36 and self.solar_panel_pick == 0 and self.solar_panel_down==1: #捡起太阳能板
            self.solar_panel_pick = 1
            self.zb.current[0] = 4
            self.zb.handle = self.solar_panel
        return
    def mouseup(self,mx,my):
        return
    def keyup(self,key):
        return
    def keydown(self,key):
        if key == 32:#空格
            print(self.zb.handle )
            if self.ball_pick == 1:
                print(key)
                self.hb_play = 1
        return
class CLS_huiben3(object):
    def __init__(self,scr):
        hbList = ['绘本1.jpg','绘本2.jpg','绘本3.jpg','绘本4.jpg',\
                  '绘本5.jpg','绘本6.jpg','绘本7.jpg','绘本8.jpg',\
                  '绘本12.jpg','绘本13.jpg','绘本14.jpg','绘本15.jpg']
        self.hbList = []
        self.start = 0
        for hb in hbList:
            self.hbList.append(load_img(hb,(860,540),None))
        self.tick = 0
        self.r = 0
        self.current = 9
        self.play = 0
        self.finish = 0
    def hb_draw(self,scr):
        if self.play == 0:
            draw_picture(scr,self.hbList[self.current],0)
            if self.current == 9:
                self.current = 10
                draw_picture(scr,self.hbList[self.current],0)
            self.play = 1
        else:
            scr.blit(self.hbList[self.current],(0,0))
    def mousedown(self,mx,my):
        if 782<mx<845 and 226<my<306 and self.current <11:
            self.current +=1
            if self.current == 9:
                self.current +=1
            self.play = 0
        elif 782<mx<845 and 226<my<306 and self.current ==11:
            self.finish = 1
        elif 18<mx<79 and 232<my<301 and self.current != 0:
            self.current -=1
            if self.current == 9:
                self.current-=1
            self.play = 0
        return
'''
pygame.init()
screen = pygame.display.set_mode((860, 540))
pygame.display.set_caption("level3")
level3 = CLS_level3(screen)
screen.fill((255,255,255))
clock = pygame.time.Clock()
while True:
    level3.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            level3.mousedown(event.pos[0],event.pos[1])
            print(event.pos[0],event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.KEYDOWN:
            level3.keydown(event.key)
    pygame.display.update()'''
    

