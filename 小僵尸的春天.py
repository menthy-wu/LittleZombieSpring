import pygame,sys,time,os,random
def load_img(pic,size,color):
    img = pygame.image.load(pic)
    if color != None:
        img.set_colorkey( color )
    img = pygame.transform.scale(img, size )
    return img
def draw_picture(scr,pic,start):
    w = 860
    while True:
        w-=5
        scr.blit(pic,(w,0),(w,0,860,540))
        pygame.display.update()
        if w <= start:
            break
    return
class CLS_button(object):
    def __init__(self,x,y,w,h,bgCls = None, txt = '', align = 0,\
                 fnt = None, fSize = 14, fCls = (0,0,0), auto = True):
        self.left, self.top = x,y
        self.width,self.height = w,h
        self.bgColor = bgCls
        self.txt = txt
        self.alignment = align #0:左   1：右  2：居中
        self.fontName = fnt
        self.fontSize = fSize
        self.fontColor = fCls
        self.autoSize = auto
        self.font = pygame.font.Font(self.fontName,self.fontSize)
        self.flag = 0
        self.callback_click = None
        return
    def draw(self,scr):
        pygame.draw.circle(scr,self.bgColor,\
                (self.left+self.height//2,self.top+self.height//2),self.height//2,0)
        pygame.draw.circle(scr,self.bgColor,\
                (self.left+self.width-self.height//2,self.top+self.height//2),self.height//2,0)
        pygame.draw.rect(scr,self.bgColor,\
                (self.left+self.height//2,self.top,self.width-self.height,self.height),0)
        if self.flag == 1:
            pygame.draw.circle(scr,(self.bgColor[0]/1.5,self.bgColor[1]/1.5,self.bgColor[2]/1.5),\
                    (self.left+self.height//2,self.top+self.height//2),self.height//2,0)
            pygame.draw.circle(scr,(self.bgColor[0]/1.5,self.bgColor[1]/1.5,self.bgColor[2]/1.5),\
                    (self.left+self.width-self.height//2,self.top+self.height//2),self.height//2,0)
            pygame.draw.rect(scr,(self.bgColor[0]/1.5,self.bgColor[1]/1.5,self.bgColor[2]/1.5),\
                    (self.left+self.height//2,self.top,self.width-self.height,self.height),0)
        img_text = self.font.render(self.txt,True,self.fontColor)
        w,h = img_text.get_size()
        y = self.top+self.height/2-h/2
        if self.alignment == 0:
            scr.blit( img_text ,(self.left,y))
        elif self.alignment == 1:
            scr.blit( img_text ,(self.left+self.width-w,y))
        elif self.alignment == 2:
            scr.blit( img_text ,(self.left+(self.width-w)/2,y))
    def mousedown(self,mx,my):
        if self.left<=mx<=self.left+self.width and self.top <=my <= self.top+self.height:
            self.flag = 1
            return True
    def mouseup(self,mx,my):
        if self.left<=mx<=self.left+self.width and self.top <=my <= self.top+self.height:
            self.flag = 0
            return True
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
        img_text = font.render('Initializing '+str(num)+'/6',True,(255,255,255))
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
class CLS_Start(object):
    def __init__(self,pic):
        img = pygame.image.load(pic)
        self.img = pygame.transform.scale(img, (860, 540) )
        button1 = CLS_button(280,280,300,60,bgCls = (142,174,173),txt = "START",fnt = 'ArgonPERSONAL-Regular.otf',\
                            fCls = (255,255,255),fSize = 40,align = 2)
        button1.callback_click = self.is_start
        self.buttonList = [button1]
        self.finish = 0
        return
    def draw(self,scr):
        scr.blit(self.img, (0, 0))
        for button in self.buttonList:
            button.draw(scr)
        font = pygame.font.Font('ArgonPERSONAL-Regular.otf', 60)
        img_text = font.render("LITTLE ZOMBIE'S SPRING",True,(100,120,120))
        #72,63,119
        #scr.blit( img_text ,(32,132))
        img_text = font.render("LITTLE ZOMBIE'S SPRING",True,(255,255,255))
        scr.blit( img_text ,(85,180))
        return
    def mousedown(self,mx,my):
        for button in self.buttonList:
            button.mousedown(mx,my)
        return
    def mouseup(self,mx,my):
        for button in self.buttonList:
            if button.mousedown(mx,my):
                if button.callback_click!=None:
                    button.callback_click(button)
    def is_start(self,button):
        self.finish = 1
        return
    def keydown(self,key):
        return
    def keyup(self,key):
        return
class CLS_intro(object):
    def __init__(self):
        txt1 = 'All the humans were wiped out by the zombie virus'
        txt2 ='The Earth was covered with ice and snow'
        txt3 = 'The world was nothing but white'
        txt4 ='The last remaining species on the Earth began to disappear'
        txt5 ='There was only one little zombie left in the world'
        txt6 = 'One day, the little zombie picked up a picture book'
        txt7 = 'This was a picture book about spring'
        txt8 = 'The little zombie set out on a journey to find spring'
        txt9 = 'During this journey, he also found his own memories of being human'
        self.txtList = [txt1,txt2,txt3,txt4,txt5,txt6,txt7,txt8,txt9]
        self.corrent_txt = [0,0]
        self.systick = 0
        self._tick = 0
        self.txt = ''
        self.font = pygame.font.Font('G0v1.otf', 24)
        self.x,self.y = 160,210
        self.finish = 0
        self.flag = 0
    def add_txt(self):
        self.systick+=1
        if self.corrent_txt[0]>=len(self.txtList):
            self.finish = 1
            return False
        if self.systick%70 == 60 and self.corrent_txt[1]<len(self.txtList[self.corrent_txt[0]]):
            self.txt = self.txt+self.txtList[self.corrent_txt[0]][self.corrent_txt[1]]
            self.corrent_txt[1]+=1
    def draw(self,scr):
        scr.fill((0,0,0))
        self.add_txt()
        img_text = self.font.render(self.txt,True,(255,255,255))
        scr.blit( img_text ,(self.x,self.y))
        txt = self.font.render('>>>',True,(255,255,255))
        scr.blit(txt,(780,500))
        self.draw_(scr)
    def mousedown(self,mx,my):
        self.txt = ''
        self.corrent_txt = [self.corrent_txt[0]+1,0]
        return
        #self.add_txt()
    def mouseup(self,mx,my):
        return
    def draw_(self,scr):
        self._tick +=1
        if self._tick%240 <= 100:
            img_text = self.font.render(self.txt,True,(255,255,255))
            img = self.font.render('_',True,(255,255,255))
            scr.blit(img,(img_text.get_size()[0]+self.x,self.y))
        return
    def keydown(self,key):
        return
    def keyup(self,key):
        self.mousedown(0,0)
        return
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
            img_text = font24.render('Click to move',True,(255,255,255))
            scr.blit( img_text ,(150,250))
        if self.pick_hb == 0:
            font24 = pygame.font.Font('G0v1.otf', 20)
            img_text = font24.render('Click to pick up',True,(255,255,255))
            scr.blit( img_text ,(self.hb_x,self.hb_y-50))
        if self.pick_tishi == 1:
            font24 = pygame.font.Font('G0v1.otf', 20)
            img_text = font24.render('press space to look at the book',True,(255,255,255))
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
            img_text = font24.render('is this.....me?',True,(85,65,55))
            heartbeat = pygame.mixer.Sound('heartbeat.ogg')
            if self.sound == 0:
                heartbeat.play()
                self.sound = 1
            scr.blit( img_text ,(471,418))
    def mousedown(self,mx,my):
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
class CLS_level2(object):
    def __init__(self,scr,clock):
        self.clock = clock
        self.draw_circle = 0
        self.hb = CLS_huiben2(scr)
        self.hb_play = 0
        self.finish = 0
        self.btn = CLS_btn(scr)
        self.maze = CLS_maze(scr)
        self.pintu = CLS_pintu(scr)
        self.current_bg = 0
        bgList = ['2bg1.jpg','2bg2.jpg','2bg3.jpg','2bg4.jpg',\
                  '2bg5.jpg','2bg6.jpg','2bg7.jpg','2bg8.jpg',\
                  '2bg9.jpg','2bg10.jpg','2bg11.jpg','2bg12.jpg',\
                  '2bg13.jpg','2bg14.jpg']
        self.bgList = []
        self.zb_draw = 0
        scr.blit(load_img('1 世界末日.jpg',(860,540),None),(0,0))
        font = pygame.font.Font('G0v1.otf', 20)
        img_text = font.render('Initializing 1/6',True,(255,255,255))
        scr.blit( img_text ,(130,220))
        n = 0
        pygame.draw.rect(scr,(255,255,255),(130,250,600,20),2)
        self.tick = 0
        for bg in bgList:
            n+=1
            self.bgList.append(load_img(bg,(860,540),None))
            pygame.draw.rect(scr,(255,255,255),(130,250,600/14*n,20),0)
            pygame.display.update()
        self.zb = CLS_zombie(scr,-150,245,134,283,2)
        self.xq = load_img('2项圈.jpg',(70,70),(255,255,255))#项圈
        self.xq_fanzhuan = pygame.transform.flip(self.xq ,True,False)
        self.door_open = 0  #门开了没
        self.maze_start = 0  #迷宫开始
        self.direction = 0 #物品的方向
        self.pt_start = 0 #拼图开始
        self.scr = scr
        self.three_start = 0#第三个开启
        return
    def draw(self,scr):
        if self.finish == 1:
            return
        if self.hb_play == 1 and self.hb.finish == 0:
            if self.draw_circle == 0:
                r = 0
                self.clock.tick( 150 )
                while True:
                    r+=1
                    pygame.draw.circle(scr,(255,255,255),(430,260),r,0)
                    pygame.display.update()
                    if r>860:
                        self.draw_circle =1
                        break
            self.hb.hb_draw(scr)
            return
        if self.hb.finish == 1:
            self.zb.current[0] = 2
            while True:
                self.clock.tick( 100 )
                self.zb.x+=self.zb.spd
                scr.blit(self.bgList[self.current_bg],(0,0))
                self.zb.draw(scr)
                pygame.display.update()
                if self.zb.x>860:
                    self.finish = 1
                    return
        self.tick += 1
        if self.door_open == 1 and self.current_bg < 9:
            while True:
                self.clock.tick( 10 )
                self.current_bg+=1
                scr.blit(self.bgList[self.current_bg],(0,0))
                pygame.display.update()
                if self.current_bg == 9:
                    break
                self.zb_draw = 1
            return
        scr.blit(self.bgList[self.current_bg],(0,0))

        if self.zb_draw == 1:
            self.zb.draw(scr)
            if self.zb.x<0:
                self.zb.current[0] = 2
                while True:
                    clock.tick( 100 )
                    self.zb.x+=self.zb.spd
                    if self.zb.x>=0:
                        self.zb.current[0] = 0
                        break
                    scr.blit(self.bgList[self.current_bg],(0,0))
                    self.zb.draw(scr)
                    pygame.display.update()
        if self.maze_start == 1 and self.maze.finish == 0: #迷宫开启
            self.maze.draw(scr)
        if self.maze.finish == 1 and self.pt_start == 0:  #第一个通过
            self.current_bg = 10 
            self.zb_draw = 1
        if self.pt_start == 1 and self.pintu.finish == 0: #拼图开启
            self.pintu.draw(scr)
        if self.pintu.finish == 1 and self.current_bg == 10:  #第二个通过
            self.current_bg = 11 
            self.zb_draw = 1
        if self.three_start == 1 and self.btn.finish == 0: #拼图开启
            self.btn.draw(scr)
        if self.btn.finish == 1 and self.current_bg == 11:#第三个通过
            self.current_bg = 12
            self.zb_draw = 1
        if self.current_bg == 13:
            if self.direction == 0 and self.zb.hand != None:
                scr.blit(self.xq,(self.zb.hand))
            if self.direction == 1 and self.zb.hand != None:
                scr.blit(self.xq_fanzhuan,(self.zb.hand))
        if self.zb.handle == self.xq:
            font = pygame.font.Font('G0v1.otf', 30)
            img_text = font.render('new page collected, press space to open the book',True,(255,255,255))
            scr.blit( img_text ,(50,150))
        
        return
    def mousedown(self,mx,my):
        if self.hb_play ==1 and self.hb.finish == 0:
            self.hb.mousedown(mx,my)
            return
        if self.current_bg == 12:
            if 625<mx<818 and 331<my<522:
                self.current_bg = 13
                self.zb.handle = self.xq
                return
        if self.door_open == 0 and 393<mx<467 and 278<my<357: #开门
            self.door_open = 1
            self.tick = 0
            return
        if self.zb.x<mx-self.zb.w:   #向右走
            self.direction = 0
            self.zb.current[0] = 2
            while True:
                if self.zb.x>=184-self.zb.w and self.maze.finish == 0:
                    self.zb.current[0] = 0
                    break
                if self.zb.x>=308-self.zb.w and self.pintu.finish == 0:
                    self.zb.current[0] = 0
                    break
                if self.current_bg == 11 and self.zb.x>=461-self.zb.w:
                    self.zb.current[0] = 0
                    break
                if self.current_bg == 12 and self.zb.x>=602-self.zb.w:
                    self.zb.current[0] = 0
                    break
                if self.zb.x>=mx-self.zb.w:
                    self.zb.current[0] = 0
                    break
                self.clock.tick( 100 )
                self.zb.x+=self.zb.spd
                self.draw(self.scr)
                pygame.display.update()
        if self.zb.x>mx:             #向左走
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
        if self.door_open == 1 and self.current_bg == 9:  #第一个
            if 186<mx<268 and 328<my<519:
                self.zb_draw = 0
                self.maze_start = 1
                return
        if self.current_bg == 10:  #第二个
            if 317<mx<409 and 339<my<529:
                self.zb_draw = 0
                self.pt_start = 1
                return
        if self.current_bg == 11:      #第三个
            if 470<mx<559 and 346<my<527:
                self.zb_draw = 0
                self.three_start = 1
        if self.three_start == 1: #第三个开启
            self.btn.mousedown(mx,my)
        if self.pt_start == 1:       #拼图开启
            self.pintu.mousedown(mx,my)
        return
    def mouseup(self,mx,my):
        self.pintu.mouseup(mx,my)
        return
    def keydown(self,key):
        if self.maze_start == 1 and self.maze.finish == 0:
            self.maze.keydown(key)
            return
        if key == 32 and self.current_bg == 13:#空格
            if self.zb.handle == self.xq:
                self.hb_play = 1
        return
    def keyup(self,key):
        return
    def mousemotion(self,mx,my):
        self.pintu.mousemotion(mx,my)
        return
class CLS_pintu(object):
    def __init__(self,scr):
        self.bg = load_img('2maze.jpg',(860,540),None)
        self.pintu = load_img("2拼图.jpg",(450,300),None)
        pintuList = ['2 拼图1.jpg','2 拼图2.jpg','2 拼图3.jpg',\
                     '2 拼图4.jpg','2 拼图5.jpg','2 拼图6.jpg']
        self.ptList = []
        self.xyList =  [(167,336),(537,50 ),(376,241),(238,98 ),(555,213),(502,344)]
        self.xy2List = [(205,100),(355,100),(505,100),(205,250),(355,250),(505,250)]
        for pt in pintuList:
            self.ptList.append(load_img(pt,(150,150),None))
        self.mouse = 0
        self.current_pt = None
        self.gx,self.gy = 0,0
        self.finish = 0
        self.done = 0
        return
    def draw(self,scr):
        scr.blit(self.bg,(0,0))
        #scr.blit(self.pintu,(205,100))
        pygame.draw.rect(scr,(32,67,96),(205,100,450,300),2)
        for i in range(6):
            scr.blit(self.ptList[i],self.xyList[i])
        return
    def mousedown(self,mx,my):
        try:
            if self.done == 1:
                self.finish = 1
            for i in range(6):
                if self.xyList[i][0]<mx<self.xyList[i][0]+150 and self.xyList[i][1]<my<self.xyList[i][1]+150:
                    self.current_pt = i
                    self.gx,self.gy = mx-self.xyList[i][0],my-self.xyList[i][1]
                    break
            self.mouse = 1
        except:
            return
        return
    def mouseup(self,mx,my):
        self.mouse = 0
        return
    def mousemotion(self,mx,my):
        if self.mouse == 1:
            self.xyList[self.current_pt] = (mx-self.gx,my-self.gy)
            if self.xy2List[self.current_pt][0]+20<mx<self.xy2List[self.current_pt][0]+130 \
               and self.xy2List[self.current_pt][1]+20<my<self.xy2List[self.current_pt][1]+130:
                self.xyList[self.current_pt] = self.xy2List[self.current_pt]
                if self.xyList == self.xy2List:
                    self.done = 1
        return
class CLS_btn(object):
    def __init__(self,scr):
        self.scr = scr
        fin = open('2第三个.txt','r')
        ff = fin.read().split()
        self.btn = []
        self.fin = []
        self.done = 0
        self.finish = 0
        self.duibi = []
        fin.close()
        self.again = load_img('2again.jpg',(50,50),(255,255,255))
        self.bg = load_img('2maze.jpg',(860,540),None)
        self.finish = 0
        for y in range(6):
            l = []
            for x in range(8):
                l.append(int(ff[x+8*y]))
            self.fin.append(l)
        for y in range(6):
            l = []
            ll = []
            for x in range(8):
                l.append(int(ff[x+8*y]))
                ll.append(0)
            self.btn.append(l)
            #self.fin.append(lll)
            self.duibi.append(ll)
    def draw(self,scr):
        scr.blit(self.bg,(0,0))
        scr.blit(self.again,(10,25))
        x,y,w,h = 185,85,70,74
        for yy in range(6):
            for xx in range(8):
                if self.btn[yy][xx] == 1:
                    color = (255,0,0)
                elif self.btn[yy][xx] == 0:
                    color = (0,255,0)
                pygame.draw.circle(scr,color,(x+xx*w,y+yy*h),10,0)
        font = pygame.font.Font('G0v1.otf', 20)
        img_text = font.render('make all the lights green',True,(255,255,255))
        scr.blit( img_text ,(160,35))
    def mousedown(self,mx,my):
        if 10<mx<60 and 25<my<75:
            self.btn = [[],[],[],[],[],[]]
            for y in range(6):
                for x in range(8):
                    self.btn[y].append(self.fin[y][x])
                    
            return
        if self.done == 1:
            self.finish = 1
            return
        color=self.scr.get_at((mx,my))
        if color != (255, 0, 0, 255) and color != (0, 255, 0, 255):
            return
        x,y,w,h = 185,85,70,74
        xx = int((mx+15-x)/w)
        yy = int((my+15-y)/h)
        dlist = [[0,0],[-1,0],[1,0],\
                 [0,1],[0,-1],[1,-1],\
                 [-1,1],[1,1],[-1,-1]]
        for d in dlist:
            x1,y1 = xx+d[0],yy+d[1]
            try:
                self.btn[y1][x1] =1-self.btn[y1][x1]
            except:
                continue
        if self.btn == self.duibi:
            self.done = 1
        return
class CLS_maze(object):
    def maze_create(self):
        def find_next(x,y,List):
            dList = [[0,2],[0,-2],[2,0],[-2,0]]
            d = random.randint(0,3)
            for i in range(4):
                dx,dy = x+dList[d%4][0],y+dList[d%4][1]
                if 0<dx<45 and 0<dy<36 and List[dy][dx] == 1:
                    return d%4
                d += 1
            return 'aaaaaaaaaaaa'
        a = [0]*45
        b = [0,1]*22
        b.append(0)
        List = []
        List.append(a)
        for i in range(18):
            List.append(b[::])
            List.append(a[::])
        dList1 = [[0,1],[0,-1],[1,0],[-1,0]]
        dList2 = [[0,2],[0,-2],[2,0],[-2,0]]
        List[1][1] = 2
        mem = [[1,1]]
        x,y = 1,1
        while True:
            if mem == []:
                break
            d = find_next(x,y,List)
            if d != 'aaaaaaaaaaaa':
                x,y,x1,y1 = x+dList2[d][0],y+dList2[d][1],x+dList1[d][0],y+dList1[d][1]
                List[y][x] = 2
                List[y1][x1] = 2
                mem.append([x,y])
            else:
                x,y = mem.pop(-1)
        return List
    def draw_lines(self,scr,List):
        scr.fill((151,156,171))
        def find_next(x,y,List,lx,ly):
            dList = [[0,1],[0,-1],[-1,0],[1,0]]
            for d in range(4):
                dx,dy = x+dList[d][0],y+dList[d][1]
                if 0<dx<45 and 0<dy<36 and List[dy][dx] == 2 :
                    #print(x,y,dx,dy,lx,ly,'hi')
                    if dx!=lx or dy!=ly:
                        color = (30,60,100)
                        pygame.draw.line(scr,color,(165+12*x,70+11*y),(165+12*dx,70+11*dy),5)
                        find_next(dx,dy,List,x,y)
        find_next(1,1,List,1,1)
        img = scr.copy()
        pygame.image.save(img,'maze.jpg')
                    
    def __init__(self,scr):
        self.maze = self.maze_create()
        self.draw_lines(scr,self.maze)
        self.maze_pic=load_img('maze.jpg',(860,540),(151,156,171))
        self.finish = 0
        self.bg = load_img('2maze.jpg',(860,540),None)
        self.ball_x,self.ball_y = 1,1
    def draw(self,scr):
        scr.blit(self.bg,(0,0))
        scr.blit(self.maze_pic,(165,70),(165,70,535,410))
        x,y,w = 150,50,27
        color = (30,60,100)
        ball_color = (100,100,255)
        pygame.draw.circle(scr,color,(x+20*w,y+15*w+2),10,0)
        pygame.draw.circle(scr,color,(x+1 *w,y+1 *w+2),10,0)
        pygame.draw.circle(scr,(0,0,0),(165+self.ball_x *12,70+self.ball_y*11),9,0)
        pygame.draw.circle(scr,ball_color,(165+self.ball_x *12,70+self.ball_y*11),8,0)
        pygame.draw.circle(scr,(255,255,255),(165+self.ball_x *12+3,70+self.ball_y*11+3),3,0)
        
        if self.ball_x == 43 and self.ball_y == 35:
            self.finish = 1
        font = pygame.font.Font('G0v1.otf', 20)
        img_text = font.render('Use direction keys to move',True,(255,255,255))
        scr.blit( img_text ,(165,40))
    def keydown(self,key):
        x,y = self.ball_x,self.ball_y
        x1,y1 = self.ball_x,self.ball_y
        if key == 273:#up
            y-=1
            y1 = y-1
        elif key == 276:#left
            x-=1
            x1 = x-1
        elif key == 275:#right
            x+=1
            x1 = x+1
        elif key == 274:#down
            y+=1
            y1 = y+1
        if y>38 or y<1 or x>45 or x<1:
            return
        if self.maze[y][x] == 2:
            self.ball_x,self.ball_y = x1,y1
            return
        return
class CLS_huiben2(object):
    def __init__(self,scr):
        hbList = ['绘本1.jpg','绘本2.jpg','绘本3.jpg','绘本4.jpg',\
                  '绘本5.jpg','绘本6.jpg','绘本7.jpg','绘本8.jpg',\
                  '绘本11.jpg','绘本12.jpg','绘本13.jpg']
        self.hbList = []
        self.start = 0
        for hb in hbList:
            self.hbList.append(load_img(hb,(860,540),None))
        self.tick = 0
        self.r = 0
        self.current = 8
        self.play = 0
        self.finish = 0
    def hb_draw(self,scr):
        if self.play == 0:
            draw_picture(scr,self.hbList[self.current],0)
            if self.current == 8:
                self.current = 9
                draw_picture(scr,self.hbList[self.current],0)
            self.play = 1
        else:
            scr.blit(self.hbList[self.current],(0,0))
    def mousedown(self,mx,my):
        if 782<mx<845 and 226<my<306 and self.current <10:
            self.current +=1
            if self.current == 8:
                self.current +=1
            self.play = 0
        elif 782<mx<845 and 226<my<306 and self.current ==10:
            self.finish = 1
        elif 18<mx<79 and 232<my<301 and self.current != 0:
            self.current -=1
            if self.current == 8:
                self.current-=1
            self.play = 0
        return
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
        img_text = font.render('Initializing 3/6',True,(255,255,255))
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
            img_text = font.render('no power',True,(255,255,255))
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
            font = pygame.font.Font('G0v1.otf', 30)
            img_text = font.render('new page collected, press space to open the book',True,(255,255,255))
            scr.blit( img_text ,(50,150))
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
            if self.ball_pick == 1:
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
        img_text = font.render('Initializing 5/6',True,(255,255,255))
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
                    break
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
        if self.pick_luntai == 1 and self.luntai_place == 0 and 73<mx<771 and 463<my<531:#放轮胎
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
        if self.use_qjd == 1 and 145<mx<208 and 423<my<477 and self.window_break == 0 and self.pick_stick==0: #拿棍子
            self.pick_stick = 1
            self.current_bg = 5
            self.zb.current[0] = 4
        if self.qjd_place == 1 and 145<mx<208 and 403<my<477 and self.use_qjd == 0:#使用千斤顶
            self.use_qjd = 1
            self.current_bg = 4
        if self.qjd_pick == 1 and self.qjd_place == 0 and 80<mx<367 and 403<my<477: #放下千斤顶
            self.zb.current[0] = 4
            self.zb.handle = 0
            self.current_bg = 3
            self.qjd_place = 1
        if self.hbx_open == 1 and 243<mx<306 and 302<my<367 and self.qjd_pick == 0:#拿千斤顶
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
        if self.hb.complete_finish == 1:
            self.finish = 1
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
            font = pygame.font.Font('G0v1.otf', 30)
            img_text = font.render('new page collected, press space to open the book',True,(255,255,255))
            scr.blit( img_text ,(50,150))
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
        self.complete_finish = 0
    def hb_draw(self,scr):
        if self.current == 18:
            time.sleep(2)
            self.complete_finish = 1
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
class CLS_end(object):
    def __init__(self):
        txt1 = 'The little zombie found his memory'
        txt2 ='He also found his own spring as well as that girl...'
        txt3 ='Although the humans are extinct'
        txt4 ="the zombie's story will continue..."
        txt5 = 'The End'
        self.txtList = [txt1,txt2,txt3,txt4,txt5]
        self.corrent_txt = [0,0]
        self.systick = 0
        self._tick = 0
        self.txt = ''
        self.font = pygame.font.Font('G0v1.otf', 24)
        self.x,self.y = 160,210
        self.finish = 0
        self.flag = 0
    def add_txt(self):
        self.systick+=1
        if self.corrent_txt[0]>=len(self.txtList):
            self.finish = 1
            return False
        if self.systick%120 == 60 and self.corrent_txt[1]<len(self.txtList[self.corrent_txt[0]]):
            self.txt = self.txt+self.txtList[self.corrent_txt[0]][self.corrent_txt[1]]
            self.corrent_txt[1]+=1
    def draw(self,scr):
        scr.fill((0,0,0))
        self.add_txt()
        img_text = self.font.render(self.txt,True,(255,255,255))
        scr.blit( img_text ,(self.x,self.y))
        txt = self.font.render('>>>',True,(255,255,255))
        scr.blit(txt,(780,500))
        self.draw_(scr)
    def mousedown(self,mx,my):
        if self.corrent_txt[0] == 4:
            return
        self.txt = ''
        self.corrent_txt = [self.corrent_txt[0]+1,0]
        return
        #self.add_txt()
    def mouseup(self,mx,my):
        return
    def draw_(self,scr):
        self._tick +=1
        if self._tick%240 <= 120:
            img_text = self.font.render(self.txt,True,(255,255,255))
            img = self.font.render('_',True,(255,255,255))
            scr.blit(img,(img_text.get_size()[0]+self.x,self.y))
        return
    def keydown(self,key):
        return
    def keyup(self,key):
        self.mousedown(0,0)
        return
SCREEN_W,SCREEN_H = 860, 540

class CLS_framework(object):
    def __init__(self,scr,clock):
        self.click = pygame.mixer.Sound('click1.wav')
        self.current = 0
        self.modList = []
        intro = CLS_intro()
        #start = CLS_Start('1 世界末日.jpg')
        #level1 = CLS_level_1(scr,clock)
        #level2 = CLS_level2(scr,clock)
        #level3 = CLS_level3(scr,clock)
        #level4 = CLS_level4(scr,clock)
        #end = CLS_end()
        self.modList = [intro]
        #self.modList = [start,intro,level1,level2,level3,level4,end]
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
pygame.mixer.music.set_volume(0.05)
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
