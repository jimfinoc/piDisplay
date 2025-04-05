import pygame
import datetime
import time
import random
import math
from threading import Thread, Event
from stockDataFunctions import return_details

import argparse

time_between_redis_pulls = .5

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sort", choices=['Name','Percent'], default=['Name'], help = "Sort stocks by Name")
args = parser.parse_args()

# print("args")
print('args.sort')
print(args.sort)

DataStyle = 0
if 'Name' in args.sort:
    print("Sorting by Name")
    DataStyle = 1
elif 'Percent' in args.sort:
    DataStyle = 2
    print("Sorting by Percent")

# if args.Output:
#     print("Displaying Output as: % s" % args.Output)

redisDataPull  = {}
# print(redisDataPull)
stop_threads = False

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prBlue(skk): print("\033[94m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def redisPullDataFunction(var):
    pullcount = 0
    global stop_threads
    start = time.time()
    while not stop_threads:
        if time.time() - start > time_between_redis_pulls:
            start = time.time()
            # var.clear()
            global redisDataPull
            redisDataPull = return_details("My_quotes")
            var = redisDataPull
            # prRed('done loading stock data')
            # print('len(var)')
            # print(len(var))
            # time.sleep(1)
    prRed('Stop printing')


t1 = Thread(target=redisPullDataFunction, args=(redisDataPull, ))
t1.start()


pygame.init()
print()
size = pygame.display.get_desktop_sizes()
if size[0] == (3440,1440):
    my_screen_size = 10
    my_screen = "Widescreen Big Monitor"
elif size[0] == (1920,1080):
    my_screen_size = 11
    my_screen = "Standard  Monitor"
elif size[0] == (800,480) or size[0] == (480,800):
    my_screen_size = 21
    my_screen = "Pi Touchscreen 1 Monitor"
elif size[0] == (1280,720) or size[0] == (720,1280):
    my_screen_size = 22
    my_screen = "Pi Touchscreen 2 Monitor"
else:
    my_screen_size = 0
    my_screen = "an 'I'm not sure' Monitor"

print("Looks like you are using a", my_screen)
print("Your screen size is ",size[0])
time.sleep(1)

if my_screen_size == 21 or my_screen_size == 22:
    flags = pygame.FULLSCREEN
    screen_width=0
    screen_height=0
else:
    # flags = pygame.FULLSCREEN
    flags = pygame.SHOWN
    screen_width=800
    screen_height=480
    
display_surface = pygame.display.set_mode([screen_width, screen_height],flags)

pygame.mouse.set_visible(False)
# display_surface = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
print(pygame.display.Info())
# print()
x, y = display_surface.get_size()
# x = x - 1
# y = y - 1
print(x)
print(y)
white = (255, 255, 255)
red = (128, 0, 0)
green = (0, 128, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
color = {}
color[0]=black
color[1]=white
color[2]=red
color[3]=green
color[4]=blue
stock_color = {}
stock_color[0] = (255*10/10,0,0)
stock_color[1] = (255*9/10,0,0)
stock_color[2] = (255*8/10,0,0)
stock_color[3] = (255*7/10,0,0)
stock_color[4] = (255*6/10,0,0)
stock_color[5] = (255*5/10,0,0)
stock_color[6] = (255*4/10,0,0)
stock_color[7] = (255*3/10,0,0)
stock_color[8] = (255*2/10,0,0)
stock_color[9] = (255*1/10,0,0)

stock_color[10] = black

stock_color[11] = (0,255*1/10,0)
stock_color[12] = (0,255*2/10,0)
stock_color[13] = (0,255*3/10,0)
stock_color[14] = (0,255*4/10,0)
stock_color[15] = (0,255*5/10,0)
stock_color[16] = (0,255*6/10,0)
stock_color[17] = (0,255*7/10,0)
stock_color[18] = (0,255*8/10,0)
stock_color[19] = (0,255*9/10,0)
stock_color[20] = (0,255*10/10,0)

# font = pygame.font.Font('freesansbold.ttf', 32)

# quit()

# squares = 50
done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(30)
    today = datetime.date.today()

    # print('len(redisDataPull)')
    # print(len(redisDataPull))   
    squares = len(redisDataPull)

    # squares = squares + 1
    # if size[0][0] > size[0][1] or True==True:
    cols = []
    rows = int(math.sqrt(squares))
    if size[0][0] < size[0][1]:
        rows = int(squares/rows)

    for i in range(rows):
        cols.append(int(squares/rows))
    for i in range(rows-1,0,-1):
        if (sum(cols)<squares):
            cols[i]=cols[1]+1


    print('cols')
    print(cols)
    print('rows')
    print(rows)
    print('squares')
    print(squares)

    my_rect={}
    count = 0
    stockList = []
    for each in redisDataPull:
        stockList.append(redisDataPull[each])
    # print ('stockList')
    # print (stockList)

    # stocksSorted = []

    # if 'Name' in args.sort:
    if DataStyle == 1:
        stocksSorted = sorted(stockList, key=lambda item: item["symbol"])
    if DataStyle == 2:
    # elif 'Percent' in args.sort:
        stocksSorted = sorted(stockList, key=lambda item: item["change_percent"])


    # for each in range(len(stocksSortedByName)):
    #     print (stocksSortedByName[each])
    #     pass

    for each_row in range(rows):
        for each_col in range(cols[each_row]):
            my_rect[count] = {}
            # my_rect[count]["Rect"] = pygame.Rect( (x*each_col/cols[each_row],y*each_row/rows) , (x*(each_col+1)/cols[each_row],y*(each_row+1)/rows))
            X1 = x*each_col/cols[each_row]
            my_rect[count]["X1"] = X1
            Y1 = y*each_row/rows
            my_rect[count]["Y1"] = Y1
            X2 = x*(each_col+1)/cols[each_row]
            my_rect[count]["X2"] = X2 
            Y2 = y*(each_row+1)/rows
            my_rect[count]["Y2"] = Y2
            my_rect[count]["Rect"] = pygame.Rect( (X1,Y1) , (X2,Y2) )
            my_rect[count]["Text1"] = stocksSorted[count]["symbol"]
            my_rect[count]["Text2"] = str(stocksSorted[count]["price"])
            my_rect[count]["Text3"] = f'{stocksSorted[count]["change"]}    {stocksSorted[count]["change_percent"]:.2f}%'

            try:
                backgroundNumber = float(stocksSorted[count]["change_percent"])
            except:
                backgroundNumber = 0.0
            if backgroundNumber < 0.0:
                backgroundColor = (int(math.sqrt(-backgroundNumber/100.0)*256.0),0,0)
            elif backgroundNumber > 0.0:
                backgroundColor = (0,int(math.sqrt(backgroundNumber/100.0)*256.0),0)
            else:
                backgroundColor = (0,0,0)
            my_rect[count]["backgroundColor"] = backgroundColor

            count = count + 1

    
    # print (my_rect)


    # my_rect = pygame.Rect((0,0),(x//2,y//2))
    # rect1 = pygame.draw.rect(display_surface, white, my_rect,width=2)
    # pygame.Surface.fill(black, rect1)
    for square in my_rect:
        # pygame.draw.rect(display_surface, white, my_rect[square],width=10,border_radius=50)
        # pygame.draw.rect(display_surface, white, my_rect[square],width=1)
        # pygame.display.flip()

        font = pygame.font.Font('freesansbold.ttf', 60//rows)
        # backgroundColor = random.choice(stock_color)


        background = my_rect[square]["backgroundColor"]

        pygame.draw.rect(display_surface, background, my_rect[square]["Rect"])
        text1 = font.render(my_rect[square]["Text1"], True, white, background)
        cx = my_rect[square]["X1"] + (my_rect[square]["X2"] - my_rect[square]["X1"])//2
        textRect1 = text1.get_rect()
        cy = my_rect[square]["Y1"] + 1*(my_rect[square]["Y2"] - my_rect[square]["Y1"])//4
        textRect1.center = (cx , cy)
        display_surface.blit(text1, textRect1)

        text2 = font.render(my_rect[square]["Text2"], True, white, background)
        textRect2 = text2.get_rect()
        cy = my_rect[square]["Y1"] + 2*(my_rect[square]["Y2"] - my_rect[square]["Y1"])//4
        textRect2.center = (cx , cy)
        display_surface.blit(text2, textRect2)

        text3 = font.render(my_rect[square]["Text3"], True, white, background)
        textRect3 = text3.get_rect()
        cy = my_rect[square]["Y1"] + 3*(my_rect[square]["Y2"] - my_rect[square]["Y1"])//4
        textRect3.center = (cx, cy)
        display_surface.blit(text3, textRect3)


    # time.sleep(1)

    # pygame.screen.fill((0,0,0))

    pygame.display.update()



    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                # print("Left mouse button clicked")
                if DataStyle == 1:
                    DataStyle = 2
                    prYellow("Now sorting by Percent")
                elif DataStyle == 2:
                    DataStyle = 1
                    prGreen("Now sorting by Name")
            if pygame.mouse.get_pressed()[1]:
                prBlue("Doing nothing")
                pass
            if pygame.mouse.get_pressed()[2]:
                # print("Right mouse button clicked")
                print("Exiting program")
                stop_threads = True
                pygame.display.quit()
                done = True
                pygame.quit()
        if event.type == pygame.QUIT:
                stop_threads = True
                pygame.display.quit()
                done = True
                pygame.quit()


