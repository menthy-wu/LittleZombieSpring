import pygame,sys,time
from zombie import*

class CLS_level4(object):
    def __init__(self,scr,clock):
        self.clock = clock
        self.glas_break=pygame.mixer.Sound('Bottle Break.wav')
        self.finish = 0
        self.hb_play = 0
        self.hb = CLS_huiben4(scr,clock)
        bgList = ['4风筝1.jpg','4风筝2.jpg','4风筝3.jpg','4风筝4.jpg','4风筝5.jpg',\
                  '4风筝6.jpg','4风筝7.jpg','4风筝8.jpg','4风筝9.jpg','4风筝10.jpg']
        banshou = '4扳手100.jpg'
        fengzhen = '4风筝100.jpg'
        gunzi = '4棍儿100.jpg'
        luntai = '4轮胎100.jpg'
        luntaipiao = '4轮胎飘100.jpg'
        qianjingding = '4千斤顶100.jpg'
        self.bgList = []
        n = 0
        scr.blit(load_img('1 世界末日.jpg',(860,540),None),(0,0))
        font = pygame.font.Font('G0v1.otf', 20)
        img_text = font.render('正在初始化5/6',True,(255,255,255))
        scr.blit( img_text ,(130,220))
        pygame.draw.rect(scr,(255,255,255),(130,250,600,20),2)
        for bg in bgList:
            n+=1 
            self.bgList.append(load_img(bg,(860,540),None))
            pygame.draw.rect(scr,(255,255,255),(130,250,600/16*n,20),0)
            pygame.display.update()
        n+=1 
        self.banshou = load_img(banshou,(70,70),(100,100,100))  #扳手
        self.banshou_fanzhuan = pygame.transform.flip(self.banshou ,True,False)
        pygame.draw.rect(scr,(255,255,255),(130,250,600/16*n,20),0)
        pygame.display.update()
        n+=1 
        self.fengzhen = load_img(fengzhen,(82,70),(100,100,100))  #风筝
        self.fengzhen_fanzhuan = pygame.transform.flip(self.fengzhen ,True,False)
        pygame.draw.rect(scr,(255,255,255),(130,250,600/16*n,20),0)
        pygame.display.update()
        n+=1 
        self.gunzi = load_img(gunzi,(70,70),(100,100,100))  #棍子
        self.gunzi_fanzhuan = pygame.transform.flip(self.gunzi ,True,False)
        pygame.draw.rect(scr,(255,255,255),(130,250,600/16*n,20),0)
        pygame.display.update()
        n+=1 
        self.luntai = load_img(luntai,(70,70),(100,100,100))#轮胎
        self.luntai_fanzhuan = pygame.transform.flip(self.luntai ,True,False)
        pygame.draw.rect(scr,(255,255,255),(130,250,600/16*n,20),0)
        pygame.display.update()
        n+=1 
        self.luntaipiao = load_img(luntaipiao,(150,84),(100,100,100))#漂浮的轮胎
        pygame.draw.rect(scr,(255,255,255),(130,250,600/16*n,20),0)
        pygame.display.update()
        n+=1 
        self.qianjingding = load_img(qianjingding,(70,70),(100,100,100))#千斤顶
        self.qianjingding_fanzhuan = pygame.transform.flip(self.qianjingding ,True,False)
        pygame.draw.rect(scr,(255,255,255),(130,250,600/16*n,20),0)
        pygame.display.update()
        
        self.scr = scr
        self.zb = CLS_zombie(scr,-150,245,134,283,6)
        self.current_bg = 0  #现在的背景
        self.hbx_open = 0    #打开后备箱
        self.qjd_pick = 0    #拿起千斤顶
        self.qjd_place = 0   #放下千斤顶
        self.direction = 0   #物品方向
        self.use_qjd = 0     #使用千斤顶
        self.pick_stick = 0  #拿棍子
        self.window_break = 0 #砸窗子
        self.pick_banshou = 0 #拿扳手
        self.pick_luntai = 0 #拿轮胎
        self.luntai_place = 0#放轮胎
        self.luntai_x = 470  #轮胎坐标
        self.on_luntai = 0  #上轮胎
        self.fengzheng_pick = 0#捡风筝
        return
    def mousedown(self,mx,my):
        if self.hb_play == 1 :
            self.hb.mousedown(mx,my)
            return
        if self.zb.x<mx-self.zb.w and self.on_luntai == 0:   #向右走
            self.direction = 0
            self.zb.current[0] = 2
            while True:
                self.clock.tick( 100 )
                if self.zb.x>=400:
                    self.zb.current[0] = 0
                    return
                if self.zb.x>=mx-self.zb.w:
                    self.zb.current[0] = 0
                    break
                self.zb.x+=self.zb.spd
                self.draw(self.scr)
                pygame.display.update()
        if self.zb.x>mx and self.on_luntai == 0:             #向左走
            self.direction = 1
            self.zb.current[0] = 3
            while True:
                self.clock.tick( 100 )
                if self.zb.x<=mx:
                    self.zb.current[0] = 1
                    break
                self.zb.x-=self.zb.spd
                self.draw(self.scr)
                pygame.display.update()
        if self.zb.x<mx-self.zb.w and self.on_luntai == 1:   #向右飘
            self.direction = 0
            self.zb.current[0] = 0
            while True:
                if self.zb.x>=mx-self.zb.w:
                    break
                self.zb.x+=self.zb.spd
                self.luntai_x +=self.zb.spd
                self.draw(self.scr)
                pygame.display.update()
        if self.zb.x>mx and self.on_luntai == 1:             #向左飘
            self.direction = 1
            self.zb.current[0] = 1
            while True:
                if self.zb.x<=mx or self.zb.x<=480:
                    break
                self.zb.x-=self.zb.spd
                self.luntai_x -=self.zb.spd
                self.draw(self.scr)
                pygame.display.update()
        if self.luntai_place == 1 and 492<mx<635 and 476<my<540:#上轮胎
            self.on_luntai = 1
        if self.pick_luntai == 1 and self.luntai_place == 0 and 496<mx<613 and 446<my<534:#放轮胎
            self.luntai_place = 1
            self.zb.current[0] = 4
        if self.pick_banshou == 1 and 90<mx<152 and 368<my<461:#拿轮胎
            self.pick_luntai = 1
            self.current_bg = 8
            self.zb.current[0] = 4
        if self.window_break == 1 and self.pick_banshou == 0 and 370<mx<441 and 255<my<296: #拿扳手
            self.pick_banshou = 1
            self.current_bg = 7
        if self.pick_stick == 1 and self.window_break == 0 and 370<mx<441 and 255<my<296:#砸窗子
            self.glas_break.play(loops=0, maxtime=0, fade_ms=0)
            self.window_break = 1
            self.current_bg = 6
            self.pick_stick = 0
        if self.use_qjd == 1 and 145<mx<208 and 423<my<477 and self.window_break == 0: #拿棍子
            self.pick_stick = 1
            self.current_bg = 5
            self.zb.current[0] = 4
        if self.qjd_place == 1 and 145<mx<208 and 423<my<477 and self.use_qjd == 0:#使用千斤顶
            self.use_qjd = 1
            self.current_bg = 4
        if self.qjd_pick == 1 and self.qjd_place == 0 and 145<mx<208 and 423<my<477: #放下千斤顶
            self.zb.current[0] = 4
            self.zb.handle = 0
            self.current_bg = 3
            self.qjd_place = 1
        if self.hbx_open == 1 and 243<mx<306 and 302<my<367:#拿千斤顶
            self.zb.handle = self.qianjingding
            self.qjd_pick = 1
            self.current_bg = 2
            return
        if self.hbx_open == 0 and 159<mx<366 and 224<my<371:#打开后备箱
            self.current_bg = 1
            self.hbx_open = 1
            return
        if self.on_luntai == 1 and 747<mx<864 and 443<my<498:#拿起风筝
            self.current_bg = 9
            self.fengzheng_pick = 1
            self.zb.current[0] = 4 
        
        return
    def mouseup(self,mx,my):
        return
    def draw(self,scr):
        if self.zb.x<0:
            self.zb.current[0] = 2
            self.clock.tick( 100 )
            while True:
                self.zb.x+=self.zb.spd
                scr.blit(self.bgList[self.current_bg],(0,0))
                self.zb.draw(scr)
                pygame.display.update()
                if self.zb.x>=0:
                    self.zb.current[0] = 0
                    break
        if self.hb_play == 1:
            if self.hb.start == 0:
                r = 0
                self.hb.start = 1
                while True:
                    r+=1
                    pygame.draw.circle(scr,(255,255,255),(430,260),r,0)
                    pygame.display.update()
                    if r>860:
                        break
            self.hb.hb_draw(scr)
            return
        scr.blit(self.bgList[self.current_bg],(0,0))
        if self.qjd_pick == 1 and self.qjd_place == 0 and self.zb.hand != None:   #拿起千斤顶
            if self.direction == 0:
                scr.blit(self.qianjingding,self.zb.hand)
            if self.direction == 1:
                scr.blit(self.qianjingding_fanzhuan,self.zb.hand)
        if self.pick_stick == 1 and self.window_break == 0 and self.zb.hand != None:       #拿起棍子
            if self.direction == 0:
                scr.blit(self.gunzi,self.zb.hand)
            if self.direction == 1:
                scr.blit(self.gunzi_fanzhuan,self.zb.hand)
        if self.pick_banshou == 1 and self.pick_luntai == 0 and self.zb.hand != None:       #拿起扳手
            if self.direction == 0:
                scr.blit(self.banshou,self.zb.hand)
            if self.direction == 1:
                scr.blit(self.banshou_fanzhuan,self.zb.hand)
        if self.pick_luntai == 1 and self.luntai_place == 0 and self.zb.hand != None:       #拿起轮胎
            if self.direction == 0:
                scr.blit(self.luntai,self.zb.hand)
            if self.direction == 1:
                scr.blit(self.luntai_fanzhuan,self.zb.hand)
        if self.luntai_place == 1:#放轮胎
            scr.blit(self.luntaipiao,(self.luntai_x,460))
        if self.on_luntai == 1:  #上轮胎
            self.zb.x = self.luntai_x
        if self.fengzheng_pick == 1 and self.zb.hand != None:#拿起风筝
            if self.direction == 0:
                scr.blit(self.fengzhen,self.zb.hand)
            if self.direction == 1:
                scr.blit(self.fengzhen_fanzhuan,self.zb.hand)
        self.zb.draw(scr)
            
            
        return
    def keydown(self,key):
        if self.fengzheng_pick == 1 and key == 32:#空格
            self.hb_play = 1
        return
    def keyup(self,key):
        return
class CLS_huiben4(object):
    def __init__(self,scr,clock):
        self.clock = clock
        hbList = ['绘本1.jpg','绘本2.jpg','绘本3.jpg','绘本4.jpg',\
                  '绘本5.jpg','绘本6.jpg','绘本7.jpg','绘本8.jpg',\
                  '绘本12.jpg','绘本14.jpg','绘本15.jpg','绘本16.jpg',\
                  '绘本17.jpg','绘本18.jpg','绘本19.jpg','绘本20.jpg',\
                  '绘本21.jpg','绘本22.jpg','绘本23.jpg']
        self.hbList = []
        self.start = 0
        for hb in hbList:
            
            self.hbList.append(load_img(hb,(860,540),None))
        self.tick = 0
        self.r = 0
        self.current = 10
        self.play = 0
        self.finish = 0
        self.endList = 'The End'
        self.end = ''
        self.endnum = 0
    def hb_draw(self,scr):
        if self.current == 18:
            self.clock.tick( 5 )
            if self.endnum<=len(self.endList):
                self.endnum+=1
            self.end=self.endList[0:self.endnum]
            font = pygame.font.Font('ArgonPERSONAL-Regular.otf', 60)
            img_text = font.render(self.end,True,(0,85,75))
            scr.blit( img_text ,(85,180))
            return
        if self.finish ==1 and self.current == 12:
            for i in range(13,19):
                self.clock.tick( 1 )
                scr.blit(self.hbList[i],(0,0))
                pygame.display.update()
            self.current = 18
            return
        if self.play == 0:
            draw_picture(scr,self.hbList[self.current],0)
            if self.current == 10:
                self.current = 11
                draw_picture(scr,self.hbList[self.current],0)
            self.play = 1
        else:
            scr.blit(self.hbList[self.current],(0,0))
    def mousedown(self,mx,my):
        print(self.current)
        if 782<mx<845 and 226<my<306 and self.current <12:
            self.current +=1
            if self.current == 10:
                self.current +=1
            self.play = 0
        elif self.current ==12:
            self.finish = 1
        elif 18<mx<79 and 232<my<301 and self.current != 0:
            self.current -=1
            if self.current == 10:
                self.current-=1
            self.play = 0
        return
'''
pygame.init()
screen = pygame.display.set_mode((860, 540))
pygame.display.set_caption("level4")
level4 = CLS_level4(screen)
screen.fill((255,255,255))
clock = pygame.time.Clock()
while True:
    clock.tick( 100 )
    level4.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            level4.mousedown(event.pos[0],event.pos[1])
            print(event.pos[0],event.pos[1])
        elif event.type == pygame.KEYDOWN:
            level4.keydown(event.key)
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
    pygame.display.update()  '''  
        
