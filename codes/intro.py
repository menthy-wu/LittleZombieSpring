import pygame,sys,time,os
class CLS_intro(object):
    def __init__(self):
        txt1 = '有一个叫人类的种族因为丧尸病毒灭绝了'
        txt2 ='地球被冰雪覆盖，这个世界除了白色就只有白色'
        txt3 ='这个地球上仅存的物种开始消失'
        txt4 ='世界上只剩下一只小僵尸了'
        txt5 = '这天，小僵尸捡到了一本绘本'
        txt6 = '这是一本有关春天的绘本'
        txt7 = '自此，小僵尸踏上了寻找春天的旅程'
        txt8 = '在这个旅程中，他也找回了自己为人时候的记忆'
        self.txtList = [txt1,txt2,txt3,txt4,txt5,txt6,txt7,txt8]
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
'''
pygame.init()
screen = pygame.display.set_mode((860, 540))
pygame.display.set_caption("start")
intro = CLS_intro()
while True:
    intro.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            intro.mousedown()
            print(event.pos[0],event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
    pygame.display.update()
'''
