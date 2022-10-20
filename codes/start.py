#开始

from button import *
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


'''
pygame.init()
screen = pygame.display.set_mode((860, 540))
pygame.display.set_caption("start")
screen.fill((0,0,30))
start = CLS_Start('1 世界末日.jpg')
while True:
    start.draw(screen)
    if start.start== 1:
        print('start')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start.mousedown(event.pos[0],event.pos[1])
            #print(event.pos[0],event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
    pygame.display.update()
'''
