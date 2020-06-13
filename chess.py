# -*- coding:utf-8 -*-
import pygame
class Chess(pygame.sprite.Sprite):
    def __init__(self, pos, w, h, image_file):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.width = int(w)
        self.heigh = int(h)
        self.image = pygame.transform.scale(pygame.image.load(image_file).convert_alpha(), (self.width, self.heigh)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0]*32, pos[1]*32)