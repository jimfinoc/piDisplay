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
from stockDataFunctions import return_orders
import copy
import argparse

time.sleep(2)
pygame.init()

time_between_redis_pulls = 1
time_to_show_text = 2

textPortfolioSetTime = time.time()
textSortSetTime = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sort", choices=['Name','Date','Type & Name','Type & Date'], default=['Date'], help = "Sort stocks by Name")
parser.add_argument("-p", "--filter", choices=['All','Calls','Puts'], default=['All'], help = "Who's filter to show")
parser.add_argument("-e", "--equity", choices=['All'], default=['All'], help = "Who's filter to show")
args = parser.parse_args()

# print("args")
# print('args.sort', args.sort)
# print('args.filter', args.filter)

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


        time.sleep(2)

        stop_threads = Value('b', False)
        p1 = Process(target=redisPullDataFunction, args=(lock, temp_dict, stop_threads))
        p1.start()

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
            # screen_width=2560
            # screen_height=1024
            screen_width=800
            screen_height=480
            
        display_surface = pygame.display.set_mode([screen_width, screen_height],flags)

        pygame.mouse.set_visible(True)
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
        
        zoomInBox = False
        BlockText1 = "No Data"
        BlockText2 = "No Data"
        BlockText3 = "No Data"
        BlockSymbol = "No Data"
        BlockStock = "No Data"
        BlockStockPrice = "No Data"
        strike_lookup_counter = 0
        # My_stock_option_strikes = return_details("My_stock_option_strikes")
        # prGreen('My_stock_option_strikes loaded for the first time')
        while not done:
            equity_set = set()
            clock.tick(30)
            today = datetime.date.today()
            position_temp_dict = return_details("My_position_details")
            strike_lookup_counter = strike_lookup_counter + 1
            # if strike_lookup_counter%10==0:
            #     My_stock_option_strikes = return_details("My_stock_option_strikes")
            #     print('refreshed My_stock_option_strikes')
            try:
                for each in position_temp_dict["securitiesAccount"]["positions"]:
                    if each["instrument"]["assetType"] == "OPTION":
                        equity_set.add(each["instrument"]["symbol"][0:6])
                equity_list = sorted(list(equity_set))
            except:
                print('Error in equity_list creation')

            list_of_symbol_open_orders = []
            My_open_orders = return_orders("open")
            for each in My_open_orders:
                # print ('each')
                # print (each)
                for each_leg in each["orderLegCollection"]:
                    # print ('each_leg')
                    # print (each_leg)
                    if each_leg["orderLegType"] == "OPTION":
                        list_of_symbol_open_orders.append(each_leg["instrument"]["symbol"])

            squares = 0
            while squares == 0:
                redisFilterData = {}
                redisAllDataPull = {}
                # redisAllDataPull = position_temp_dict.copy()
                # redisAllDataPull = copy.deepcopy(position_temp_dict)
                try:
                    for each in position_temp_dict["securitiesAccount"]["positions"]:
                    # if each["instrument"]["assetType"] == "EQUITY":
                        # redisFilterData[each["instrument"]["symbol"]] = each
                        if each["instrument"]["assetType"] == "OPTION":
                            redisAllDataPull[each["instrument"]["symbol"]] = each
                except:
                    print('Error in redisAllDataPull creation')
                        # equity_set.add(each["instrument"]["underlyingSymbol"])
                        # print ('each')
                        # print (each)


                # print('redisAllDataPull')
                # print(redisAllDataPull)
                # if DataShown == 0: #'All'
                if 'All' in args.filter:
                    redisFilterData = redisAllDataPull.copy()
                # elif DataShown == 1: #'Stocks'
                elif 'Calls' in args.filter:
                    for each in redisAllDataPull:
                        if each[12:13] == 'C':
                            redisFilterData[each] = redisAllDataPull[each]
                elif 'Puts' in args.filter:
                    for each in redisAllDataPull:
                        if each[12:13] == 'P':
                            redisFilterData[each] = redisAllDataPull[each]



                if 'All' in args.equity:
                    pass
                else:
                    temp = copy.deepcopy(redisFilterData)
                    # print('temp')
                    # print(temp)
                    redisFilterData.clear()
                    for each in temp:
                        if temp[each]["instrument"]["symbol"][0:6] == args.equity[0]:
                            redisFilterData[each] = temp[each]



                #     for each in return_positions("stock"):
                #         if each in redisAllDataPull:
                #             redisFilterData[each] = redisAllDataPull[each]
                # elif 'Options' in args.filter:
                #     for each in return_positions("option"):
                #         if each in redisAllDataPull:
                #             redisFilterData[each] = redisAllDataPull[each]
                # elif 'Both' in args.filter:
                #     for each in return_positions("stock"):
                #         if each in redisAllDataPull:
                #             redisFilterData[each] = redisAllDataPull[each]
                #     for each in return_positions("option"):
                #         if each in redisAllDataPull:
                #             redisFilterData[each] = redisAllDataPull[each]
                # elif 'Speculation' in args.filter:
                #     for each in return_details("My_speculation_stocks"):
                #         if each in redisAllDataPull:
                #             redisFilterData[each] = redisAllDataPull[each]
                # elif 'Others' in args.filter:
                #     for each in return_details("My_other_stocks"):
                #         if each in redisAllDataPull:
                #             redisFilterData[each] = redisAllDataPull[each]

                # elif DataShown == 2: #'Options'
                #     pass
                # elif DataShown == 3: #'Both'
                #     pass
                # elif DataShown == 4: #'Speculation'
                #     pass
                # elif DataShown == 5: #'Others'
                #     pass
                # prLightPurple('redisFilterData')
                # prLightPurple(redisFilterData)
                # print ('equity_list')
                # print (equity_list)
                squares = len(redisFilterData)
                if squares == 0:
                    squares = 1
            
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
            optionList = []
            for each in redisFilterData:
                optionList.append(redisFilterData[each])

            if 'Name' in args.sort:
                optionsSorted = sorted(optionList, key=lambda item: item['instrument']["symbol"])
            if 'Date' in args.sort:
                optionsSorted = sorted(optionList, key=lambda item: item['instrument']["symbol"][6:12])
            if 'Type & Name' in args.sort:
                optionsSorted = sorted(optionList, key=lambda item: item['instrument']["symbol"][0:6])
                optionsSorted = sorted(optionsSorted, key=lambda item: item['instrument']["symbol"][12:13])
            if 'Type & Date' in args.sort:
                optionsSorted = sorted(optionList, key=lambda item: item['instrument']["symbol"][6:12])
                optionsSorted = sorted(optionsSorted, key=lambda item: item['instrument']["symbol"][12:13])

            if 'Type & Date' in args.sort:
                optionsSorted = sorted(optionList, key=lambda item: item['instrument']["symbol"])
                optionsSorted = sorted(optionsSorted, key=lambda item: item['shortQuantity'])


            # elif 'Percent' in args.sort:
                # optionsSorted = sorted(optionList, key=lambda item: item["change_percent"])
            # else :
                # optionsSorted = optionList
            # optionsSorted = optionList


            # for each in range(len(optionsSortedByName)):
            #     print (optionsSortedByName[each])
            #     pass

            optiontype = "C"
            fullname = ""
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
                    my_rect[count]["Rect"] = pygame.Rect( (X1,Y1) , (X2-X1+1,Y2-Y1+1) )
                    my_rect[count]["Rect2"] = pygame.Rect( (X1,Y1) , (X2-X1,Y2-Y1) )
                    # my_rect[count]["Rect2"] = pygame.Rect( (X1+10,Y1+10) , (X2-10,Y2-10) )
                    if len(optionsSorted) > 0:

                        my_rect[count]["Text1"] = f'{optionsSorted[count]["instrument"]["symbol"][0:6].replace(" ","")} - {optionsSorted[count]["shortQuantity"]:.0f} x {optionsSorted[count]["instrument"]["symbol"][12:13]}'
                        my_rect[count]["Text2"] = optionsSorted[count]['instrument']["symbol"][6:12]
                        strike_price = f'{(float(optionsSorted[count]["instrument"]["symbol"][13:19])/10):.2f}'
                        my_rect[count]["Text3"] = strike_price
                        my_rect[count]["symbol"] = optionsSorted[count]["instrument"]["symbol"]


                        # my_rect[count]["Text2"] = str(optionsSorted[count]["price"])
                        # my_rect[count]["Text3"] = f'{optionsSorted[count]["change"]:.2f}   {optionsSorted[count]["change_percent"]:.1f}%'
                        # my_rect[count]["Text1"] = "No 1"
                    else:
                        my_rect[count]["Text1"] = "No Data"
                        my_rect[count]["Text2"] = "No Data"
                        my_rect[count]["Text3"] = "No Data"
                    try:
                        # backgroundNumber = float(optionsSorted[count]["change_percent"])
                        # I would like to get the difference between the current price and the strike price
                        
                        symbol = optionsSorted[count]["instrument"]["symbol"][0:6].replace(" ", "")
                        current_price = float(temp_dict[symbol]["price"])
                        # print()
                        # print('symbol')
                        # print(symbol)
                        # print('current_price')
                        # print(current_price)
                        # print('strike_price')
                        # print(strike_price)
                        fullname = optionsSorted[count]["instrument"]["symbol"]
                        if optionsSorted[count]["instrument"]["symbol"][12:13] == 'P':
                            backgroundNumber = float((float(strike_price) - float(current_price))/float(current_price))
                            optiontype = "P"
                            
                        elif optionsSorted[count]["instrument"]["symbol"][12:13] == 'C':
                            backgroundNumber = float((float(strike_price) - float(current_price))/float(current_price))
                            optiontype = "C"
                            # backgroundNumber = float((strike_price - current_price)/current_price)
                        # print('optionsSorted[count]["instrument"]["symbol"]')
                        # print(optionsSorted[count]["instrument"]["symbol"])
                        # print('backgroundNumber')
                        # print(backgroundNumber)
                    except:
                        backgroundNumber = 0.0


                    if optiontype == "C":
                        # print("C",backgroundNumber)
                        # backgroundColor = (max(0,min(int(backgroundNumber*128.0),255)),0,0)
                        backgroundColor = (0,0,0)
                        if backgroundNumber > 0.0:
                            backgroundColor = (0,4,0)
                        else:   
                            backgroundColor = (0,96,0)

                    elif optiontype == "P":
                        if backgroundNumber < 0.0:
                            backgroundColor = (4,0,0)
                        else:   
                            backgroundColor = (96,0,0)
                        
                        # if backgroundNumber > 0.0:
                            # backgroundColor = (max(32,min(int((1-backgroundNumber)*255.0+0),255)),0,0)
                        # else:
                            # backgroundColor = (0,0,0)                            # backgroundColor = (255,0,0)
                        # backgroundColor = (max(16,min(int(backgroundNumber*128.0),255)),0,0)
                        # print(fullname,backgroundNumber,backgroundColor)

                    # if backgroundNumber < 0.0:
                    #     backgroundColor = (max(0,min(int(backgroundNumber*128.0),255)),0,0)
                    #     # backgroundColor = (255,0,0)
                    # elif backgroundNumber > 0.0:
                    #     backgroundColor = (0,max(0,min(int(backgroundNumber*128.0),255)),0)
                    else:
                        backgroundColor = (0,0,0)
                    # print('backgroundColor')
                    # print(backgroundColor)
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

                font = pygame.font.Font('freesansbold.ttf', 110//rows)
                if size[0][0] < size[0][1]:
                    font = pygame.font.Font('freesansbold.ttf', 110//rows)


                # backgroundColor = random.choice(stock_color)


                background = my_rect[square]["backgroundColor"]
                # print('background')
                # print(background)


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

                # if an order exists draw a box around it
                try:
                    if my_rect[square]["symbol"] in list_of_symbol_open_orders:
                        pygame.draw.rect(display_surface, yellow, my_rect[square]["Rect2"],width=3,border_radius=10)
                except:
                    print('Error in my_rect[square]["symbol"]')
                    # pygame.draw.rect(display_surface, yellow, my_rect[square]["Rect"],width=5,border_radius=50)
                    # print()
                    # print('my_rect[square]["symbol"]')
                    # print(my_rect[square]["symbol"])
                    # print('my_rect[square]["Rect"]')
                    # print(my_rect[square]["Rect"])
                    # print('my_rect[square]["Rect2"]')
                    # print(my_rect[square]["Rect2"])

                    # pygame.draw.rect(display_surface, yellow, my_rect[square]["Rect"],width=3,border_radius=10)




            # time.sleep(1)

            # pygame.screen.fill((0,0,0))
            # if DataShown == 0: # 'All'
            # if 'All' in args.filter:
            if time.time() - textPortfolioSetTime  < time_to_show_text:
                font2 = pygame.font.Font('freesansbold.ttf', 30)
                textPortfolio = font2.render(f'Filter shown is {args.filter[0]}', True, yellow, background)
                textPortfolioRect = textPortfolio.get_rect()
                x, y = display_surface.get_size()
                cx = x * 1/2
                cy = y * 2/3 
                # print('cx')
                # print(cx)
                # print('cy')
                # print(cy)
                textPortfolioRect.center = (cx, cy)
                display_surface.blit(textPortfolio, textPortfolioRect)
            if time.time() - textSortSetTime  < time_to_show_text:
                font2 = pygame.font.Font('freesansbold.ttf', 30)
                textSort = font2.render(f'Sort by {args.sort[0]}', True, yellow, background)
                textSortRect = textSort.get_rect()
                x, y = display_surface.get_size()
                cx = x * 1/2
                cy = y * 1/3
                # print('cx')
                # print(cx)
                # print('cy')
                # print(cy)
                textSortRect.center = (cx, cy)
                display_surface.blit(textSort, textSortRect)
            # elif DataShown == 1: #'Stocks'

            if zoomInBox == True:
                BlockFont = pygame.font.Font('freesansbold.ttf', 30)
                Block = pygame.Rect( 0,0 , x, y)
                pygame.draw.rect(display_surface, black, Block)

                BlockRenderText1 = BlockFont.render(BlockText1, True, white, black)
                BlockTextX = x * 1/2
                BlockTextY1 = y * 1/12
                BlockRectText1 = BlockRenderText1.get_rect()
                BlockRectText1.center = (BlockTextX , BlockTextY1)
                display_surface.blit(BlockRenderText1, BlockRectText1)

                BlockRenderText2 = BlockFont.render(BlockText2, True, white, black)
                BlockTextY2 = y * 2/12
                BlockRectText2 = BlockRenderText2.get_rect()
                BlockRectText2.center = (BlockTextX , BlockTextY2)
                display_surface.blit(BlockRenderText2, BlockRectText2)

                BlockRenderText3 = BlockFont.render(BlockText3, True, white, black)
                BlockTextY3 = y * 3/12
                BlockRectText3 = BlockRenderText3.get_rect()
                BlockRectText3.center = (BlockTextX , BlockTextY3)
                display_surface.blit(BlockRenderText3, BlockRectText3)

                BlockRenderText5a = BlockFont.render("Stock Price", True, white, black)
                BlockTextY5 = y * 5/12
                BlockRectText5a = BlockRenderText5a.get_rect()
                BlockRectText5a.center = (x*1/4 , BlockTextY5)
                display_surface.blit(BlockRenderText5a, BlockRectText5a)

                BlockRenderText5b = BlockFont.render("Days Away", True, white, black)
                BlockRectText5b = BlockRenderText5b.get_rect()
                BlockRectText5b.center = (x*3/4 , BlockTextY5)
                display_surface.blit(BlockRenderText5b, BlockRectText5b)

                BlockRenderText6a = BlockFont.render(f"{BlockStockPrice:.2f}", True, white, black)
                BlockTextY6 = y * 6/12
                BlockRectText6a = BlockRenderText6a.get_rect()
                BlockRectText6a.center = (x*1/4 , BlockTextY6)
                display_surface.blit(BlockRenderText6a, BlockRectText6a)

                BlockRenderText6b = BlockFont.render(f"{difference.days}", True, white, black)
                BlockRectText6b = BlockRenderText6b.get_rect()
                BlockRectText6b.center = (x*3/4 , BlockTextY6)
                display_surface.blit(BlockRenderText6b, BlockRectText6b)

                BlockRenderText8a = BlockFont.render("Option Income", True, white, black)
                BlockTextY8 = y * 8/12
                BlockRectText8a = BlockRenderText8a.get_rect()
                BlockRectText8a.center = (x*1/4 , BlockTextY8)
                display_surface.blit(BlockRenderText8a, BlockRectText8a)

                BlockRenderText8b = BlockFont.render("Bid Ask (x100)", True, white, black)
                BlockRectText8b = BlockRenderText8b.get_rect()
                BlockRectText8b.center = (x*3/4 , BlockTextY8)
                display_surface.blit(BlockRenderText8b, BlockRectText8b)


                BlockRenderText9a = BlockFont.render(f'{BlockOptionIncome}', True, white, black)
                BlockTextY9 = y * 9/12
                BlockRectText9a = BlockRenderText9a.get_rect()
                BlockRectText9a.center = (x*1/4 , BlockTextY9)
                display_surface.blit(BlockRenderText9a, BlockRectText9a)

                BlockRenderText9b = BlockFont.render(BlockBidAsk, True, white, black)
                BlockTextY9 = y * 9/12
                BlockRectText9b = BlockRenderText9b.get_rect()
                BlockRectText9b.center = (x*3/4 , BlockTextY9)
                display_surface.blit(BlockRenderText9b, BlockRectText9b)

                BlockRenderTextB = BlockFont.render(f"{CounterOrder}, Placed time, price", True, white, black)
                BlockTextYB = y * 11/12
                BlockRectTextB = BlockRenderTextB.get_rect()
                BlockRectTextB.center = (BlockTextX , BlockTextYB)
                display_surface.blit(BlockRenderTextB, BlockRectTextB)

            pygame.display.update()


            action = 0
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if zoomInBox == False:
                            # prPurple(f"zoomInBox is {zoomInBox}")
                            for each in my_rect:
                                if my_rect[each]["Rect"].collidepoint(event.pos):
                                    # action = 1
                                    prYellow("You clicked on a square")
                                    BlockText1 = my_rect[each]["Text1"]
                                    BlockText2 = my_rect[each]["Text2"]
                                    BlockText3 = my_rect[each]["Text3"]
                                    BlockSymbol = my_rect[each]["symbol"]

                                    # BlockOptionIncome = -1
                                    try:
                                        for each in position_temp_dict["securitiesAccount"]["positions"]:
                                            if each["instrument"]["assetType"] == "OPTION":
                                                if each["instrument"]["symbol"] == BlockSymbol:
                                                    BlockOptionIncome = f'{each["averagePrice"]*100:.2f}'
                                    except:
                                        print('Error in equity_list creation')
                                        BlockOptionIncome = f'{0:.2f}'

                                    try:
                                        My_stock_option_strikes = return_details("My_stock_option_strikes")
                                        Bid = My_stock_option_strikes[BlockSymbol]["bid"]
                                        Ask = My_stock_option_strikes[BlockSymbol]["ask"]
                                        BlockBidAsk = f'{Bid*100:.2f} - {Ask*100:.2f}'
                                    except:
                                        BlockBidAsk = f'{0:.2f} {0:.2f}'
                                        
                                    try:
                                        CounterOrder = "No Order"
                                        for eachOrder in My_open_orders:
                                            for each_leg in eachOrder["orderLegCollection"]:
                                                if each_leg["orderLegType"] == "OPTION":
                                                    if each_leg["instrument"]["symbol"] == BlockSymbol:
                                                        CounterOrder = f"Buying back at {eachOrder["price"]:.2f}"
    

                                        # CounterOrder = My_stock_option_strikes[BlockSymbol]["CounterOrder"]
                                    except:
                                        CounterOrder = "No Order"

                                    BlockFont = pygame.font.Font('freesansbold.ttf', 30)
                                    BlockRenderText9b = BlockFont.render(BlockBidAsk, True, white, black)
                                    BlockTextY9 = y * 9/12
                                    BlockRectText9b = BlockRenderText9b.get_rect()
                                    BlockRectText9b.center = (x*3/4 , BlockTextY9)
                                    display_surface.blit(BlockRenderText9b, BlockRectText9b)


                                    prGreen(BlockText1)
                                    prGreen(BlockText2)
                                    dateobjectFut = datetime.datetime.strptime("20"+BlockText2, '%Y%m%d')
                                    delta = datetime.timedelta(days=1, hours=0, minutes=0)
                                    dateobjectNow = datetime.datetime.today() - delta
                                    # dateobjectNow = datetime.datetime.now()
                                    difference = dateobjectFut - dateobjectNow

                                    prRed(f"{dateobjectFut,dateobjectNow, difference.days}")
                                    prGreen(BlockText3)
                                    prGreen(BlockSymbol)
                                    BlockStock = BlockSymbol[0:6].replace(" ", "")
                                    BlockCallPut = BlockSymbol[12:13]
                                    BlockOptionDate = BlockSymbol[6:12]
                                    BlockStockPrice = temp_dict[BlockStock]["price"]
                                    prRed("BlockStock")
                                    print(f"{BlockStock}")
                                    prRed("BlockCallPut")
                                    prRed( BlockCallPut)
                                    prRed("BlockStockPrice")
                                    prRed( BlockStockPrice)
                                    prRed("BlockOptionDate")
                                    prRed(BlockOptionDate)
                                    prRed("BlockOptionSpecialDate")
                                    BlockOptionSpecialDate = "20"+BlockOptionDate[0:2] + "-" + BlockOptionDate[2:4] + "-" + BlockOptionDate[4:6]
                                    prRed(BlockOptionSpecialDate)



                                    # print('my_rect[each]')
                                    # print(my_rect[each])
                            prYellow("Left mouse button clicked")
                            zoomInBox = True
                        elif zoomInBox == True:
                            # prPurple(f"zoomInBox is {zoomInBox}")
                            zoomInBox = False

                    if pygame.mouse.get_pressed()[1]:
                        # action = 20
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
                        action = 31
                        prYellow("Wheel rolled up")
                    if event.y > 0:
                        action = 30
                        prYellow("Wheel rolled down")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        action = 1
                        prYellow("1 key pressed")
                    if event.key == pygame.K_2:
                        if event.mod & pygame.KMOD_LSHIFT or event.mod & pygame.KMOD_RSHIFT:
                            action = 21
                            prYellow("shift 2 key pressed")
                        else:
                            action = 20
                            prYellow("2 key pressed")
                    if event.key == pygame.K_3:
                        if event.mod & pygame.KMOD_LSHIFT or event.mod & pygame.KMOD_RSHIFT:
                            action = 31
                            prYellow("shift 3 key pressed")
                        else:
                            action = 30
                            prYellow("3 key pressed")
                    if event.key == pygame.K_ESCAPE:
                        action = -1
                        prYellow("Escape key pressed")
                    if event.key == pygame.K_q:
                        action = -1
                        prYellow("q key pressed")
                if event.type == pygame.QUIT:
                        prGreen("Quit event detected")
                        prGreen("Exiting program")
                        action = -1

            if action == 1:
                    textSortSetTime = time.time()
                    if 'Name' in args.sort:
                        args.sort = ['Date']
                        prGreen("Now sorting by Date")
                    elif 'Date' in args.sort:
                        args.sort = ['Type & Name']
                        prGreen("Now sorting by Type & Name")
                    elif 'Type & Name' in args.sort:
                        args.sort = ['Type & Date']
                        prGreen("Now sorting by Type & Date")
                    elif 'Type & Date' in args.sort:
                        args.sort = ['Name']
                        prGreen("Now sorting by Name")

            if action == 20:
                textPortfolioSetTime = time.time()
                if 'All' in args.filter:
                    args.filter = ['Calls']
                    prGreen(f'Now showing {args.filter[0]}')
                elif 'Calls' in args.filter:
                    args.filter = ['Puts']
                    prGreen(f'Now showing {args.filter[0]}')
                elif 'Puts' in args.filter:
                    args.filter = ['All']
                    prGreen(f"Now showing {args.filter[0]}")
                # elif 'Options' in args.filter:
                #     args.filter = ['Both']
                #     prGreen("Now showing Both")
                # elif 'Both' in args.filter:
                #     args.filter = ['Speculation']
                #     prGreen("Now showing Speculation")
                # elif 'Speculation' in args.filter:
                #     args.filter = ['Others']
                #     prGreen("Now showing Others")
                # elif 'Others' in args.filter:
                #     args.filter = ['All']
                #     prGreen("Now showing All")

            if action == 21:
                textPortfolioSetTime = time.time()
                if 'All' in args.filter:
                    args.filter = ['Others']
                    prGreen("Now showing Others")
                elif 'Stocks' in args.filter:
                    args.filter = ['All']
                    prGreen("Now showing All")
                elif 'Options' in args.filter:
                    args.filter = ['Stocks']
                    prGreen("Now showing Stocks")
                elif 'Both' in args.filter:
                    args.filter = ['Speculation']
                    prGreen("Now showing Speculation")
                elif 'Speculation' in args.filter:
                    args.filter = ['Both']
                    prGreen("Now showing Both")
                elif 'Others' in args.filter:
                    args.filter = ['Options']
                    prGreen("Now showing Options")

            if action == 20 or action == 21:
                args.equity = ['All']
            
            if action == 30:
                if args.equity == ['All']:
                    args.equity = [equity_list[0]]
                else:
                    for i in range(len(equity_list)):
                        if args.equity == [equity_list[i]]:
                            if i < len(equity_list) - 1:
                                args.equity = [equity_list[i+1]]
                            else:
                                args.equity = ['All']
                            break
            if action == 31:
                if args.equity == ['All']:
                    args.equity = [equity_list[-1]]
                else:
                    for i in range(len(equity_list)):
                        if args.equity == [equity_list[i]]:
                            if i > 0:
                                args.equity = [equity_list[i-1]]
                            else:
                                args.equity = ['All']
                            break

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


