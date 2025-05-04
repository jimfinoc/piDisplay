import pygame
import datetime
import time
import random
import math
# from threading import Thread, Event
from multiprocessing import Process, Value, Manager, Lock
from ctypes import c_char_p
import json
from stockDataFunctions import return_details
from stockDataFunctions import return_positions
import copy
import argparse

time_between_redis_pulls = 1
time_to_show_text = 2

textPortfolioSetTime = time.time()
textSortSetTime = time.time()
textStockSetTime = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sort", choices=['Name','Percent'], default=['Name'], help = "Sort stocks by Name")
parser.add_argument("-p", "--portfolio", choices=['All','Stocks','Options','Both','Speculation','Others'], default=['Options'], help = "Who's portfolio to show")
parser.add_argument("-e", "--equity", type=str, default="", help = "This should be a stock (equity) symbol")
# parser.add_argument("stock")
args = parser.parse_args()

# print("args")
print('args.sort', args.sort)
print('args.portfolio', args.portfolio)
print('args.equity', args.equity)
# print('args.portfolio', args.portfolio)


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prBlue(skk): print("\033[94m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def redisPullDataFunction(lock, shared_dict,stop_threads):
    pullcount = 0
    local_stop = False
    start = time.time()
    while not local_stop:
        if time.time() - start > time_between_redis_pulls:
            with lock:
                local_stop = stop_threads.value
                start = time.time()
                temp = shared_dict.copy()
                temp = return_details("My_quotes")
                shared_dict.clear()
                shared_dict.update(temp)
    prRed('Stop printing')

if __name__ == '__main__':
    with Manager() as manager:
        temp_dict = manager.dict()
        lock = manager.Lock()        

        stop_threads = Value('b', False)
        p1 = Process(target=redisPullDataFunction, args=(lock, temp_dict, stop_threads))
        p1.start()

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
        time.sleep(2)

        if my_screen_size == 21 or my_screen_size == 22:
            flags = pygame.FULLSCREEN
            screen_width=0
            screen_height=0
        else:
            # flags = pygame.FULLSCREEN
            # screen_width=3440 #1280
            # screen_height=1440 #720
            flags = pygame.SHOWN
            # screen_width=1280
            # screen_height=720
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
        print('x')
        print(x)
        print('y')
        print(y)
        white = (255, 255, 255)
        yellow = (255, 255, 0)
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
        moving_x = 0
        moving_y = 0
        test_x = 750
        test_y = 450

        while not done:
            clock.tick(30)
            today = datetime.date.today()

            # print('len(redisFilterData)')
            # print(len(redisFilterData))
            # try:
                # redisFilterData = json.loads(redisFilterData_string.value.decode('utf-8'))
            # except:
                # prCyan("Error loading redisFilterData")
                # redisFilterData = {}
            # var.value = redisFilterData_string
            # prLightPurple('redisFilterData')
            # prLightPurple(redisFilterData)

            squares = 0
            equities = []
            while squares == 0:
                redisFilterData = {}
                # redisAllDataPull = temp_dict.copy()
                redisAllDataPull = copy.deepcopy(temp_dict)
                # if DataShown == 0: #'All'
                if 'All' in args.portfolio:
                    # redisFilterData = redisAllDataPull.copy()
                    for each in redisAllDataPull:
                        redisFilterData[each] = redisAllDataPull[each]
                        equities.append(each)
                # elif DataShown == 1: #'Stocks'
                elif 'Stocks' in args.portfolio:
                    for each in return_positions("stock"):
                        if each in redisAllDataPull:
                            redisFilterData[each] = redisAllDataPull[each]
                            equities.append(each)
                elif 'Options' in args.portfolio:
                    for each in return_positions("option"):
                        if each in redisAllDataPull:
                            redisFilterData[each] = redisAllDataPull[each]
                            equities.append(each)
                elif 'Both' in args.portfolio:
                    for each in return_positions("stock"):
                        if each in redisAllDataPull:
                            redisFilterData[each] = redisAllDataPull[each]
                            equities.append(each)
                    for each in return_positions("option"):
                        if each in redisAllDataPull:
                            redisFilterData[each] = redisAllDataPull[each]
                            equities.append(each)
                elif 'Speculation' in args.portfolio:
                    for each in return_details("My_speculation_stocks"):
                        if each in redisAllDataPull:
                            redisFilterData[each] = redisAllDataPull[each]
                            equities.append(each)
                elif 'Others' in args.portfolio:
                    for each in return_details("My_other_stocks"):
                        if each in redisAllDataPull:
                            redisFilterData[each] = redisAllDataPull[each]
                            equities.append(each)
                # equities = equities.sort()
                
                temp = sorted(set(equities))
                equities = list(temp)

                squares = len(redisFilterData)
                if squares == 0:
                    # prRed("No data found")
                    squares = 1
                    # redisFilterData = {}
                    # redisFilterData = redisAllDataPull.copy()
                    # time.sleep(1)
                # print('squares')
                # print(squares)  
                # print('len(redisFilterData)')
                # print(len(redisFilterData))
                # print('redisFilterData')
                # print(redisFilterData)

            # prPurple('squares != 0')
            
            SelectingEquity = False
            while SelectingEquity == False:
                try:
                    if args.equity == "":
                        args.equity = [equities[0]]
                        SelectingEquity = True
                    if args.equity[0] not in equities:
                        args.equity = [equities[0]]
                        SelectingEquity = True
                    else:
                        SelectingEquity = True
                except:
                    prRed("Error selecting equity")
                    # prPurple('args.equity')
                    # prPurple(args.equity)
                    # prPurple('equities')
                    # prPurple(equities)
                    # prPurple('equities[0]')
                    # prPurple(equities[0])
            # prBlue(f'equities: {equities}')
            # prBlue(f"Now showing {args.equity[0]}")
            
            # if squares == 0:
                # break
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


            # print('cols')
            # print(cols)
            # print('rows')
            # print(rows)
            # print('squares')
            # print(squares)

            my_rect={}
            count = 0
            stockList = []
            for each in redisFilterData:
                stockList.append(redisFilterData[each])

            if 'Name' in args.sort:
                stocksSorted = sorted(stockList, key=lambda item: item["symbol"])
            elif 'Percent' in args.sort:
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
                    if len(stocksSorted) > 0:
                        my_rect[count]["Text1"] = stocksSorted[count]["symbol"]
                        my_rect[count]["Text2"] = str(stocksSorted[count]["price"])
                        my_rect[count]["Text3"] = f'{stocksSorted[count]["change"]:.2f}   {stocksSorted[count]["change_percent"]:.1f}%'
                    else:
                        my_rect[count]["Text1"] = "No Data"
                        my_rect[count]["Text2"] = "No Data"
                        my_rect[count]["Text3"] = "No Data"
                    try:
                        backgroundNumber = float(stocksSorted[count]["change_percent"])
                    except:
                        backgroundNumber = 0.0
                    if backgroundNumber < 0.0:
                        # backgroundColor = (int(math.sqrt(-backgroundNumber/100.0)*255.0),0,0)
                        backgroundColor = (max(0,min(int(math.sqrt(-backgroundNumber/100)*256.0),255)),0,0)
                    elif backgroundNumber > 0.0:
                        # backgroundColor = (0,int(math.sqrt(backgroundNumber/100.0)*255.0),0)
                        backgroundColor = (0,max(0,min(int(math.sqrt(backgroundNumber/100)*256.0),255)),0)

                    else:
                        backgroundColor = (0,0,0)
                    my_rect[count]["backgroundColor"] = backgroundColor

                    count = count + 1

            
            # print (my_rect)


            # my_rect = pygame.Rect((0,0),(x//2,y//2))
            # rect1 = pygame.draw.rect(display_surface, white, my_rect,width=2)
            # pygame.Surface.fill(black, rect1)
            # for square in my_rect:
                # pygame.draw.rect(display_surface, white, my_rect[square],width=10,border_radius=50)
                # pygame.draw.rect(display_surface, white, my_rect[square],width=1)
                # pygame.display.flip()

            font = pygame.font.Font('freesansbold.ttf', 70//rows)
            if size[0][0] < size[0][1]:
                font = pygame.font.Font('freesansbold.ttf', 110//rows)


            # backgroundColor = random.choice(stock_color)


            background = (0,0,0)
            # print('background')
            # print(background)
            # print('my_rect[square]["Rect"]')
            # print(my_rect[square]["Rect"])
            pygame.draw.rect(display_surface, background, (0,0,x,y),width=0)
            pygame.draw.rect(display_surface, (100,100,0), (50,20,x-50-20,y-20-40),width=2)
            
            test_x += moving_x
            test_y += moving_y


            font = pygame.font.Font('freesansbold.ttf', 15)
            today = datetime.date.today()
            current_month = today.month
            current_day = today.day
            text1 = font.render(f"{current_month}/{current_day}", True, white, background)
            textRect1 = text1.get_rect()
            textRect1.center = (50 , 450)
            display_surface.blit(text1, textRect1)

            font = pygame.font.Font('freesansbold.ttf', 15)
            today = datetime.date.today()
            current_month = today.month
            current_day = today.day
            text1 = font.render(f"{current_month}/{current_day}", True, white, background)
            textRect1 = text1.get_rect()
            textRect1.center = (780, 450)
            display_surface.blit(text1, textRect1)
            # print('test_x',test_x,' test_y',test_y)

            # pygame.draw.rect(display_surface, background, my_rect[square]["Rect"])
            # cx = my_rect[square]["X1"] + (my_rect[square]["X2"] - my_rect[square]["X1"])//2
            # cy = my_rect[square]["Y1"] + 1*(my_rect[square]["Y2"] - my_rect[square]["Y1"])//4
            # textRect1.center = (cx , cy)
            # display_surface.blit(text1, textRect1)

            # text2 = font.render(my_rect[square]["Text2"], True, white, background)
            # textRect2 = text2.get_rect()
            # cy = my_rect[square]["Y1"] + 2*(my_rect[square]["Y2"] - my_rect[square]["Y1"])//4
            # textRect2.center = (cx , cy)
            # display_surface.blit(text2, textRect2)

            # text3 = font.render(my_rect[square]["Text3"], True, white, background)
            # textRect3 = text3.get_rect()
            # cy = my_rect[square]["Y1"] + 3*(my_rect[square]["Y2"] - my_rect[square]["Y1"])//4
            # textRect3.center = (cx, cy)
            # display_surface.blit(text3, textRect3)



            # time.sleep(1)

            # pygame.screen.fill((0,0,0))
            # if DataShown == 0: # 'All'
            # if 'All' in args.portfolio:
            if time.time() - textPortfolioSetTime  < time_to_show_text:
                font2 = pygame.font.Font('freesansbold.ttf', 30)
                textPortfolio = font2.render(f'Portfolio shown is {args.portfolio[0]}', True, yellow, background)
                textPortfolioRect = textPortfolio.get_rect()
                x, y = display_surface.get_size()
                cx = x * 2/3
                PortfolioOption = {'All':1,'Stocks':2,'Options':3,'Both':4,'Speculation':5,'Others':6}
                cy = y * PortfolioOption[args.portfolio[0]]/7
                textPortfolioRect.center = (cx, cy)
                display_surface.blit(textPortfolio, textPortfolioRect)

            if time.time() - textSortSetTime  < time_to_show_text:
                font2 = pygame.font.Font('freesansbold.ttf', 30)
                textSort = font2.render(f'Sort by {args.sort[0]}', True, yellow, background)
                textSortRect = textSort.get_rect()
                x, y = display_surface.get_size()
                cx = x * 1/3
                SortOption = {'Name':3,'Percent':4}
                cy = y * SortOption[args.sort[0]]/7
                textSortRect.center = (cx, cy)
                display_surface.blit(textSort, textSortRect)

            if time.time() - textStockSetTime  < time_to_show_text:
                font2 = pygame.font.Font('freesansbold.ttf', 30)
                textSort = font2.render(f'Now showing {args.equity[0]}', True, yellow, background)
                textSortRect = textSort.get_rect()
                x, y = display_surface.get_size()
                cx = x * 1/2
                # cy = y / 2
                cy = y * (equities.index(args.equity[0])+1)/(len(equities)+1)
                textSortRect.center = (cx, cy)
                display_surface.blit(textSort, textSortRect)


                
            # elif DataShown == 1: #'Stocks'

            pygame.display.update()

            moving_x = 0
            moving_y = 0

            action = 0
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        action = 1
                        prYellow("Left mouse button clicked")
                    if pygame.mouse.get_pressed()[1]:
                        # if event.mod & pygame.KMOD_LSHIFT or event.mod & pygame.KMOD_RSHIFT:
                        action = 21
                        prYellow("Middle mouse button clicked")
                        # else:
                            # action = 20
                        # prYellow("Shift Middle mouse button clicked")
                    if pygame.mouse.get_pressed()[2]:
                        action = -1
                        prYellow("Right mouse button clicked")
                if event.type == pygame.MOUSEWHEEL:
                    # print('event.x')
                    # print(event.x)
                    # print('event.y')
                    if event.y < 0:
                        action = 22
                        prYellow("Wheel rolled up")
                    if event.y > 0:
                        action = 21
                        prYellow("Wheel rolled down")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        moving_y = -1
                        prYellow("Up key pressed")
                    if event.key == pygame.K_DOWN:
                        moving_y = 1
                        prYellow("Down key pressed")
                    if event.key == pygame.K_LEFT:  
                        moving_x = -1
                        prYellow("Left key pressed")
                    if event.key == pygame.K_RIGHT:
                        moving_x = 1
                        prYellow("Right key pressed")

                    if event.key == pygame.K_1:
                        action = 1
                        prYellow("1 key pressed")
                    if event.key == pygame.K_2:
                        if event.mod & pygame.KMOD_LSHIFT or event.mod & pygame.KMOD_RSHIFT:
                            action = 22
                            prYellow("shift 2 key pressed")
                        else:
                            action = 21
                            prYellow("2 key pressed")
                    if event.key == pygame.K_3:
                        if event.mod & pygame.KMOD_LSHIFT or event.mod & pygame.KMOD_RSHIFT:
                            action = 32
                            prYellow("shift 2 key pressed")
                        else:
                            action = 31
                            prYellow("2 key pressed")
                    if event.key == pygame.K_ESCAPE:
                        action = -1
                        prYellow("Escape key pressed")
                if event.type == pygame.QUIT:
                        prGreen("Quit event detected")
                        action = -1

            if action == 1:
                    textSortSetTime = time.time()
                    if 'Name' in args.sort:
                        args.sort = ['Percent']
                        prGreen("Now sorting by Percent")
                    elif 'Percent' in args.sort:
                        args.sort = ['Name']
                        prGreen("Now sorting by Name")

            if action == 31:
                textPortfolioSetTime = time.time()
                if 'All' in args.portfolio:
                    args.portfolio = ['Stocks']
                elif 'Stocks' in args.portfolio:
                    args.portfolio = ['Options']
                elif 'Options' in args.portfolio:
                    args.portfolio = ['Both']
                elif 'Both' in args.portfolio:
                    args.portfolio = ['Speculation']
                elif 'Speculation' in args.portfolio:
                    args.portfolio = ['Others']
                elif 'Others' in args.portfolio:
                    args.portfolio = ['All']
                prGreen(f"Now showing {args.portfolio[0]}")


            if action == 32:
                textPortfolioSetTime = time.time()
                if 'Others' in args.portfolio:
                    args.portfolio = ['Speculation']
                elif 'Speculation' in args.portfolio:
                    args.portfolio = ['Both']
                elif 'Both' in args.portfolio:
                    args.portfolio = ['Options']
                elif 'Options' in args.portfolio:
                    args.portfolio = ['Stocks']
                elif 'Stocks' in args.portfolio:
                    args.portfolio = ['All']
                elif 'All' in args.portfolio:
                    args.portfolio = ['Others']
                prGreen(f"Now showing {args.portfolio[0]}")

            if action == 21:
                textStockSetTime = time.time()
                index = equities.index(args.equity[0])
                if index == len(equities) - 1:
                    index = 0
                else:
                    index = index + 1
                args.equity = [equities[index]]
                prGreen(f"Now showing {args.equity[0]}")

            if action == 22:
                textStockSetTime = time.time()
                index = equities.index(args.equity[0])
                if index == 0:
                    index = len(equities) -1
                else:
                    index = index - 1
                args.equity = [equities[index]]
                prGreen(f"Now showing {args.equity[0]}")


            if action == -1:
                prGreen("Exiting program")
                stop_threads.value = True
                # stop_threads = True
                done = True
                print('stop_threads')
                print(stop_threads.value)
                print('done')
                print(done)
                p1.join()
                pygame.display.quit()
                pygame.quit()


