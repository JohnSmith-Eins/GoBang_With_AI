# -*- coding:utf-8 -*-
import pygame
import os
import time
from pygame.locals import *
from 五子棋 import resource_folder
import chess
import aiGobang
class Game():
    def __init__(self, screen, clock, resource_folder):
        self.background2=pygame.image.load(os.path.join(resource_folder,'background1.jpg')).convert()
        self.screen = screen
        self.clock = clock
        self.stage = 0#0:开始菜单；1：人机；2：人人
        self.resource_folder = resource_folder

        #背景图片
        self.background=pygame.image.load(os.path.join(resource_folder,'background1.jpg')).convert()
        #棋子组
        self.black_chess_group = pygame.sprite.Group()
        self.white_chess_group = pygame.sprite.Group()
        #谁的回合
        self.round = 'black'
        self.winner = ''
        self.ai_color = 'white'
        #标签
        self.lable0 = pygame.font.SysFont('SimHei', int(60)).render(('五   子   棋'),True,(0,0,0))
        self.lable1 = pygame.font.SysFont('SimHei', int(30)).render(('人机对战'),True,(0,0,0))
        self.lable2 = pygame.font.SysFont('SimHei', int(30)).render(('双人对战'),True,(0,0,0))
        self.lable3 = pygame.font.SysFont('SimHei', int(30)).render(('退出游戏'),True,(0,0,0))
        self.lable4 = pygame.font.SysFont('SimHei', int(30)).render(('五子棋'),True,(0,0,0))
        self.lable5 = pygame.font.SysFont('SimHei', int(30)).render(('返回主菜单'),True,(0,0,0))
        self.lable0_rect = self.lable0.get_rect()
        self.lable1_rect = self.lable1.get_rect()
        self.lable2_rect = self.lable2.get_rect()
        self.lable3_rect = self.lable3.get_rect()
        self.lable5_rect = self.lable5.get_rect()
        self.lable0_rect.center=(400,100)
        self.lable1_rect.center=(400,250)
        self.lable2_rect.center=(400,400)
        self.lable3_rect.center=(400,550)
        self.lable5_rect.topleft=(650,600)
        #时间
        self.last_time = time.time()
        self.current_time = time.time()
        #AI
        self.ai_player = aiGobang.aiGobang('white', 'black')
        #历史记录
        self.history_record = []
        
        
        
    def run(self):
        while True:
            if self.stage==0:
                self.clock.tick(30)#屏幕刷新
                self.screen.fill((255,255,255))
                self.screen.blit(self.background2,(0,0))
                self.screen.blit(self.lable0, self.lable0_rect)
                self.screen.blit(self.lable1, self.lable1_rect)
                self.screen.blit(self.lable2, self.lable2_rect)
                self.screen.blit(self.lable3, self.lable3_rect)                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        exit()
                    if event.type == MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        pygame.mixer.Sound(os.path.join(resource_folder,'piece.wav')).play()
                        print(self.lable1.get_rect())
                        if self.lable1_rect.collidepoint(mouse_pos):
                            self.stage = 1
                        if self.lable2_rect.collidepoint(mouse_pos):
                            self.stage = 2
                        if self.lable3_rect.collidepoint(mouse_pos):
                            exit()
                pygame.display.update()
            if self.stage==1:
                self.screen.blit(self.background,(0,0))
    
                self.clock.tick(30)#屏幕刷新
        
                for event in pygame.event.get():#设置事件
                    if event.type == QUIT:
                        exit()
                    if event.type == KEYDOWN:
                        pressed_key = pygame.key.get_pressed()
                        if pressed_key[K_r]:
                            self.restart()
                    if event.type == MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.lable5_rect.collidepoint(mouse_pos):
                            self.stage = 0
                            self.restart()
                        print(mouse_pos)
                        if event.button == 1:
                            pygame.mixer.Sound(os.path.join(resource_folder,'piece.wav')).play()
                        if not self.winner:
                            if mouse_pos[0] > 16 and mouse_pos[0]<624 and mouse_pos[1] > 16 and mouse_pos[1] < 624:
                                mouse_pos = self.to_my_xy(mouse_pos)
                                print(mouse_pos)
                                clicked_chess = None                                
                                if self.round is 'black':
                                    for i in self.black_chess_group.sprites()+self.white_chess_group.sprites():
                                        if i.pos == mouse_pos:
                                            clicked_chess = i
                                            break
                                    if not clicked_chess:
                                        self.black_chess_group.add(self.black_chess((mouse_pos)))
                                        self.history_record.append(([*(mouse_pos[0]-1,mouse_pos[1]-1), self.round]))
                                        if self.check_success(self.black_chess_group.sprites(), mouse_pos):
                                            print('Black Wins!')
                                            self.winner = 'black'
                                        else:
                                            self.round = 'white'
                                            self.last_time = time.time()
                if event.type ==MOUSEBUTTONUP:
                    if not self.winner:
                    
                        #这里进行ai
                        if self.round == 'white':
                            ai_pos = self.ai_player.act(self.history_record)
                            self.history_record.append([*ai_pos, self.round])
                            ai_pos = (ai_pos[0]+1,ai_pos[1]+1)
                            self.white_chess_group.add(self.white_chess((ai_pos)))
                            if self.check_success(self.white_chess_group.sprites(), ai_pos):
                                print('White Wins!')
                                self.winner = 'white'
                            else:
                                self.round = 'black'
                                self.last_time = time.time()
                    
                self.screen.blit(self.lable4, (650,20))
                self.screen.blit(self.lable5, self.lable5_rect)
                self.screen.blit(pygame.font.SysFont('SimHei', int(20)).render(('当前执子：'+('黑方' if self.round == 'black' else '白方')),True,(0,0,0)),(650,100))
                if self.winner:
                    self.screen.blit(pygame.font.SysFont('SimHei', int(25)).render((('黑方' if self.round == 'black' else '白方')+'胜利！'),True,(240,0,0)),(650,500))
                else:
                    self.current_time = time.time()
                self.screen.blit(pygame.font.SysFont('SimHei', int(20)).render(time.strftime("%M:%S",time.localtime(self.current_time - self.last_time)),True,(0,0,0)),(650,130))
                self.black_chess_group.update()
                self.black_chess_group.draw(self.screen)
                self.white_chess_group.update()
                self.white_chess_group.draw(self.screen)
                pygame.display.update() 


            if self.stage == 2:
                self.screen.blit(self.background,(0,0))
    
                self.clock.tick(30)#屏幕刷新
        
                for event in pygame.event.get():#设置事件
                    if event.type == QUIT:
                        exit()
                    if event.type == KEYDOWN:
                        pressed_key = pygame.key.get_pressed()
                        if pressed_key[K_r]:
                            self.restart()
                    if event.type == MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.lable5_rect.collidepoint(mouse_pos):
                            self.stage = 0
                            self.restart()
                        print(mouse_pos)
                        if event.button == 1:
                            pygame.mixer.Sound(os.path.join(resource_folder,'piece.wav')).play()
                        if not self.winner:
                            if mouse_pos[0] > 16 and mouse_pos[0]<624 and mouse_pos[1] > 16 and mouse_pos[1] < 624:
                                mouse_pos = self.to_my_xy(mouse_pos)
                                print(mouse_pos)
                                clicked_chess = None
                                if self.round == 'black':
                                    for i in self.black_chess_group.sprites()+self.white_chess_group.sprites():
                                        if i.pos == mouse_pos:
                                            clicked_chess = i
                                            break
                                    if not clicked_chess:
                                        self.black_chess_group.add(self.black_chess((mouse_pos)))
                                        if self.check_success(self.black_chess_group.sprites(), mouse_pos):
                                            print('Black Wins!')
                                            self.winner = 'black'
                                        else:
                                            self.round = 'white'
                                            self.last_time = time.time()
                                else:
                                    for i in self.black_chess_group.sprites()+self.white_chess_group.sprites():
                                        if i.pos == mouse_pos:
                                            clicked_chess = i
                                            break
                                    if not clicked_chess:
                                        self.white_chess_group.add(self.white_chess((mouse_pos)))
                                        if self.check_success(self.white_chess_group.sprites(), mouse_pos):
                                            print('White Wins!')
                                            self.winner = 'white'
                                        else:
                                            self.round = 'black'
                                            self.last_time = time.time()
            
                self.screen.blit(self.lable1, (650,20))
                self.screen.blit(self.lable5, self.lable5_rect)
                self.screen.blit(pygame.font.SysFont('SimHei', int(20)).render(('当前执子：'+('黑方' if self.round == 'black' else '白方')),True,(0,0,0)),(650,100))
                if self.winner:
                    self.screen.blit(pygame.font.SysFont('SimHei', int(25)).render((('黑方' if self.round == 'black' else '白方')+'胜利！'),True,(240,0,0)),(650,500))
                else:
                    self.current_time = time.time()
                self.screen.blit(pygame.font.SysFont('SimHei', int(20)).render(time.strftime("%M:%S",time.localtime(self.current_time - self.last_time)),True,(0,0,0)),(650,130))
                self.black_chess_group.update()
                self.black_chess_group.draw(self.screen)
                self.white_chess_group.update()
                self.white_chess_group.draw(self.screen)
                pygame.display.update()            
                
    def black_chess(self, pos):
        return chess.Chess(pos, 32, 32, os.path.join(self.resource_folder,'black.png'))
    def white_chess(self, pos):
        return chess.Chess(pos, 32, 32, os.path.join(self.resource_folder,'white.png'))
    def to_my_xy(self, pos):
        return pos[0]//32 + (0 if pos[0]%32<=15 else 1), pos[1]//32 + (0 if pos[1]%32<=15 else 1)
    def restart(self):
        self.white_chess_group.empty()
        self.black_chess_group.empty()
        self.round = 'black'
        self.winner = ''
        self.last_time = time.time()
        self.current_time = time.time()
        self.history_record = []
    def check_success(self, chess_list, new_chess):
        chessxy = {}
        for i in range(-1,21):
            for j in range(-1,21):
                chessxy[(i,j)] = 0
        pos = new_chess
        for i in chess_list:
            chessxy[i.pos] = 1
        #水平
        count = 1
        i = 1
        while True:
            if chessxy[pos[0]-i, pos[1]]:
                count += 1
                i +=1
            else:
                break
        i = 1
        while True:
            if chessxy[pos[0]+i, pos[1]]:
                count += 1
                i +=1
            else:
                break
        if count >= 5:
            return True
        #垂直方向
        count = 1
        i = 1
        while True:
            if chessxy[pos[0], pos[1]-i]:
                count += 1
                i +=1
            else:
                break
        i = 1
        while True:
            if chessxy[pos[0], pos[1]+i]:
                count += 1
                i +=1
            else:
                break
        if count >= 5:
            return True
        #左上到右下方向
        count = 1
        i = 1
        while True:
            if chessxy[pos[0]-i, pos[1]-i]:
                count += 1
                i +=1
            else:
                break
        i = 1
        while True:
            if chessxy[pos[0]+i, pos[1]+i]:
                count += 1
                i +=1
            else:
                break
        if count >= 5:
            return True
        #左下到右上方向
        count = 1
        i = 1
        while True:
            if chessxy[pos[0]-i, pos[1]+i]:
                count += 1
                i +=1
            else:
                break
        i = 1
        while True:
            if chessxy[pos[0]+i, pos[1]-i]:
                count += 1
                i +=1
            else:
                break
        if count >= 5:
            return True
        return False