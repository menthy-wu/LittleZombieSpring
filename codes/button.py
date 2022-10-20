import pygame,sys,time,os
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

