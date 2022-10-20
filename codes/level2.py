import pygame,sys,time
from zombie import*



class CLS_level2(object):
    def __init__(self,scr,clock):
        self.clock = clock
        self.draw_circle = 0
        self.hb = CLS_huiben2(scr)
        self.hb_play = 0
        self.finish = 0
        self.btn = CLS_btn(scr)
        self.maze = CLS_maze()
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
        img_text = font.render('正在初始化1/6',True,(255,255,255))
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
            self.tick%1000 == 0
            self.current_bg+=1
            scr.blit(self.bgList[self.current_bg],(0,0))
            if self.current_bg == 9:
                self.zb_draw = 1
            return
        scr.blit(self.bgList[self.current_bg],(0,0))
        if self.zb_draw == 1:
            self.zb.draw(scr)
        if self.zb.x<0:
            self.zb.current[0] = 2
            self.zb.x+=self.zb.spd
            if self.zb.x>=0:
                self.zb.current[0] = 0
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
                    print('yes')
                    break
            self.mouse = 1
        except:
            print('no')
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
            ll = []
            for x in range(8):
                l.append(int(ff[x+8*y]))
                ll.append(0)
            self.btn.append(l)
            self.fin.append(l)
            self.duibi.append(ll)
    def draw(self,scr):
        scr.blit(self.bg,(0,0))
        scr.blit(self.again,(50,40))
        x,y,w,h = 185,85,70,74
        for yy in range(6):
            for xx in range(8):
                if self.btn[yy][xx] == 1:
                    color = (255,0,0)
                elif self.btn[yy][xx] == 0:
                    color = (0,255,0)
                pygame.draw.circle(scr,color,(x+xx*w,y+yy*h),10,0)
    def mousedown(self,mx,my):
        if self.done == 1:
            self.finish = 1
            return
        if 52<mx<93 and 44<my<87:
            self.btn = self.fin
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
            print(1)
        print(xx,yy)
        return
class CLS_maze(object):
    def __init__(self):
        fin = open('2迷宫.txt','r')
        ff = fin.read().split()
        self.maze = []
        fin.close()
        self.finish = 0
        for y in range(15):
            l = []
            for x in range(20):
                l.append(int(ff[x+20*y]))
            self.maze.append(l)
        #print(self.maze)
        self.bg = load_img('2maze.jpg',(860,540),None)
        self.ball_x,self.ball_y = 1,1
    def draw(self,scr):
        scr.blit(self.bg,(0,0))
        x,y,w = 150,50,27
        color = (30,60,100)
        ball_color = (100,100,255)
        pygame.draw.circle(scr,color,(x+20*w,y+15*w),10,0)
        pygame.draw.circle(scr,color,(x+1 *w,y+1 *w),10,0)
        pygame.draw.line(scr,color,(x+1 *w,y+1 *w),(x+1* w,y+15*w),5)
        pygame.draw.line(scr,color,(x+1 *w,y+15*w),(x+18*w,y+15*w),5)
        pygame.draw.line(scr,color,(x+1 *w,y+2 *w),(x+5 *w,y+2 *w),5)
        pygame.draw.line(scr,color,(x+3 *w,y+2 *w),(x+3 *w,y+7 *w),5)
        pygame.draw.line(scr,color,(x+9 *w,y+7 *w),(x+3 *w,y+7 *w),5)
        pygame.draw.line(scr,color,(x+5 *w,y+2 *w),(x+5 *w,y+5 *w),5)
        pygame.draw.line(scr,color,(x+7 *w,y+1 *w),(x+7 *w,y+5 *w),5)
        pygame.draw.line(scr,color,(x+7 *w,y+5 *w),(x+5 *w,y+5 *w),5)
        pygame.draw.line(scr,color,(x+9 *w,y+1 *w),(x+9 *w,y+7 *w),5)
        pygame.draw.line(scr,color,(x+9 *w,y+1 *w),(x+20*w,y+1 *w),5)
        pygame.draw.line(scr,color,(x+20*w,y+1 *w),(x+20*w,y+7 *w),5)
        pygame.draw.line(scr,color,(x+11*w,y+1 *w),(x+11*w,y+4 *w),5) 
        pygame.draw.line(scr,color,(x+11*w,y+4 *w),(x+12*w,y+4 *w),5) 
        pygame.draw.line(scr,color,(x+12*w,y+4 *w),(x+12*w,y+9 *w),5) 
        pygame.draw.line(scr,color,(x+14*w,y+1 *w),(x+14*w,y+7 *w),5)
        pygame.draw.line(scr,color,(x+14*w,y+7 *w),(x+18*w,y+7 *w),5) 
        pygame.draw.line(scr,color,(x+18*w,y+3 *w),(x+18*w,y+7 *w),5)
        pygame.draw.line(scr,color,(x+18*w,y+3 *w),(x+16*w,y+3 *w),5) 
        pygame.draw.line(scr,color,(x+16*w,y+5 *w),(x+16*w,y+3 *w),5) 
        pygame.draw.line(scr,color,(x+12*w,y+9 *w),(x+20*w,y+9 *w),5)
        pygame.draw.line(scr,color,(x+1 *w,y+9 *w),(x+10*w,y+9 *w),5)
        pygame.draw.line(scr,color,(x+10*w,y+9 *w),(x+10*w,y+11*w),5)
        pygame.draw.line(scr,color,(x+10*w,y+11*w),(x+3 *w,y+11*w),5)
        pygame.draw.line(scr,color,(x+1 *w,y+13*w),(x+12*w,y+13*w),5)
        pygame.draw.line(scr,color,(x+12*w,y+13*w),(x+12*w,y+11*w),5)
        pygame.draw.line(scr,color,(x+14*w,y+13*w),(x+14*w,y+9 *w),5)
        pygame.draw.line(scr,color,(x+14*w,y+13*w),(x+18*w,y+13*w),5)
        pygame.draw.line(scr,color,(x+18*w,y+13*w),(x+18*w,y+11*w),5)
        pygame.draw.line(scr,color,(x+16*w,y+11*w),(x+18*w,y+11*w),5)
        pygame.draw.line(scr,color,(x+20*w,y+9 *w),(x+20*w,y+15*w),5)
        pygame.draw.circle(scr,(0,0,0),(x+self.ball_x *w,y+self.ball_y*w),9,0)
        pygame.draw.circle(scr,ball_color,(x+self.ball_x *w,y+self.ball_y*w),8,0)
        pygame.draw.circle(scr,(255,255,255),(x+self.ball_x *w+2,y+self.ball_y*w+2),3,0)
        if self.ball_x == 20 and self.ball_y == 15:
            self.finish = 1
            print('a')
        font = pygame.font.Font('G0v1.otf', 20)
        img_text = font.render('键盘方向键控制移动',True,(255,255,255))
        scr.blit( img_text ,(156,30))
    def keydown(self,key):
        x,y = self.ball_x,self.ball_y
        if key == 273:#up
            y-=1
        elif key == 276:#left
            x-=1
        elif key == 275:#right
            x+=1
        elif key == 274:#down
            y+=1
        if y>15 or y<1 or x>20 or x<1:
            return
        if self.maze[y-1][x-1] == 1:
            self.ball_x,self.ball_y = x,y
            return
        print(key)
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
            print('finish')
        elif 18<mx<79 and 232<my<301 and self.current != 0:
            self.current -=1
            if self.current == 8:
                self.current-=1
            self.play = 0
        return
'''
pygame.init()
screen = pygame.display.set_mode((860, 540))
pygame.display.set_caption("level2")
level2 = CLS_level2(screen)
screen.fill((255,255,255))
clock = pygame.time.Clock()
while True:
    clock.tick( 30 )
    level2.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            level2.mousedown(event.pos[0],event.pos[1])
            print(event.pos[0],event.pos[1])
            
        elif event.type == pygame.MOUSEBUTTONUP:
            level2.mouseup(event.pos[0],event.pos[1])
        elif event.type == pygame.KEYDOWN:
            level2.keydown(event.key)
        elif event.type == pygame.MOUSEMOTION:
            level2.mousemotion(event.pos[0],event.pos[1])
            
    pygame.display.update()'''
    


        
