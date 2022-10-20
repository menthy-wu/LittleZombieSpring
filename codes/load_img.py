
import pygame,sys,time,os
def load_img(pic,size,color):
    img = pygame.image.load(pic)
    if color != None:
        img.set_colorkey( color )
    img = pygame.transform.scale(img, size )
    return img
def draw_picture(scr,pic,start):
    w = start
    while True:
        w+=1
        scr.blit(pic,(0,0),(0,0,w,540))
        pygame.display.update()
        if w >= 860:
            break
    return
