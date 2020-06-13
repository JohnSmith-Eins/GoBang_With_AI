# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import os,sys
import game

WIDTH = 800#界面宽度
HEIGHT = 640#界面高度
FPS = 30#游戏帧率

#游戏路径
game_folder=os.path.dirname(__file__)
resource_folder=os.path.join(game_folder,'resource')
if __name__ == '__main__':
    

    pygame.display.set_caption('五子棋')
    clock=pygame.time.Clock()
    
    #音乐
    pygame.mixer.pre_init(44100,-16,2,512)
    pygame.mixer.init()
    pygame.init()#初始pygame
    pygame.mixer.music.load(os.path.join(resource_folder,'大鱼.mp3'))
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1,0)
    clicked_sound=pygame.mixer.Sound(os.path.join(resource_folder,'piece.wav'))
    screen=pygame.display.set_mode((WIDTH,HEIGHT),0,0)
    game.Game(screen, clock, resource_folder).run()

    