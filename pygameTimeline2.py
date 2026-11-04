#!/Users/james/Programming/piDisplay/.venv/bin python3
import datetime
import time
import random
import math
from multiprocessing import Process, Value, Manager, Lock
from ctypes import c_char_p
import json
from stockDataFunctions import RedisConnection
import sys
import copy
import argparse
import os

white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

class Button:
    _button_id_counter = 0
    _max_buttons = 5

    def __init__(self):
        Button._button_id_counter += 1
        self.button_id = Button._button_id_counter
        self.loading = False
        self.rect = pygame.Rect(0, 0, 0, 0)

    def load_font(self,pygame_font):
        self.font = pygame_font

    def load_text(self,pygame_text, color = red):
        # if self.loading:
        #     self.text =  self.font.render("loading", True, red, None)
        # else:
        self.text =  self.font.render(pygame_text, True, color, None)
        self.rect = self.text.get_rect()
        self.rect.centery = surface_y * self.button_id / Button._max_buttons + 2 # this places buttons neatly and automatically in 1 of 4 positions
        self.rect.centerx = surface_x / 2

    def draw(self,surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and not self.loading:
            pygame.draw.rect(surface, white, self.rect)
        else:
            pass
            pygame.draw.rect(surface, black, self.rect)
        surface.blit(self.text, self.rect)

    def is_clicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
            if self.rect.collidepoint(event.pos):
                return True
        return False

class DisplayBoard:
    def __init__(self):
        size = pygame.display.get_desktop_sizes()
        print (f'size = {size}')
        my_screen_size = 0
        if size[0] == (800,480) or size[0] == (480,800):
            my_screen_size = 21
            my_screen = "Pi Touchscreen 1 Monitor"
        elif size[0] == (1280,720) or size[0] == (720,1280):
            my_screen_size = 22
            my_screen = "Pi Touchscreen 2 Monitor"
        else:
            my_screen = "an 'I'm not sure' Monitor"

        self.screen_width=0
        self.screen_height=0

        if my_screen_size == 21 or my_screen_size == 22:
            flags = pygame.FULLSCREEN
            pygame.mouse.set_visible(False)
        else:
            flags = pygame.SHOWN | pygame.RESIZABLE
            self.screen_width=800
            self.screen_height=480
            pygame.mouse.set_visible(True)

        self.display_surface = pygame.display.set_mode([self.screen_width, self.screen_height],flags)
        self.surface_x, self.surface_y = self.display_surface.get_size()
        self.background = black
        pygame.display.set_caption("Draw a Rectangle")
        self.font = pygame.font.Font('freesansbold.ttf', 15)

    def show_title(self,title):
        textProgram = self.font.render(title, True, white, self.background)
        textProgramRect = textProgram.get_rect()
        textProgramRect.centery = 10 / 480 * self.surface_y
        textProgramRect.centerx = 400 / 800 * self.surface_x
        self.display_surface.blit(textProgram,textProgramRect)

    def show_time(self,time_to_show):
        current_time_str = time_to_show.strftime("%Y-%m-%d %H:%M:%S")
        textTime = self.font.render(f"{current_time_str}", True, white, self.background)
        textTimeRect = textTime.get_rect()
        textTimeRect.centery = 10 / 480 * self.surface_y
        textTimeRect.right = self.surface_x - 5
        self.display_surface.blit(textTime, textTimeRect)

    def show_display_stock(self):
        pass

    def draw_border(self):
        leftside = int (50 * self.surface_x / 800)
        rightside = int (730 * self.surface_x / 800)
        topside = 20
        bottomside = self.surface_y - 40

        pygame.draw.rect(self.display_surface, self.background, (0,0,self.surface_x,self.surface_y),width=0)
        pygame.draw.rect(self.display_surface, (100,100,0), (leftside,20,rightside,self.surface_y-20-40),width=2)

    def resize(self,event):
                self.surface_x, self.surface_y = event.size
                display_surface = pygame.display.set_mode((self.surface_x, self.surface_y), pygame.RESIZABLE)
                print('Resized to', self.surface_x, self.surface_y)


 
if __name__ == '__main__':
    import pygame
    pygame.init()
    # pygame.display.Info()

    print("")
    myRedis = RedisConnection()
    myRedis.connect()
    print("")
    my_display = DisplayBoard()
    time.sleep(10)
    done = False
    clock = pygame.time.Clock()

    while not done:
        now = datetime.datetime.now()
        my_display.draw_border()
        my_display.show_title("Option Timeline")
        my_display.show_time(now)
        my_display.show_display_stock()
        clock.tick(30) 
        pygame.display.update()
        # pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                my_display.resize(event)
            if event.type == pygame.QUIT:
                done = True
pygame.quit()
