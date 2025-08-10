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
import os

SerialModuleEnabled = False
try:
    import serial
    print("Serial module enabled.")
    SerialModuleEnabled = True
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

    def receive_data():
        if ser.in_waiting > 0:
            received_bytes = ser.readline() # Read until newline or timeout
            try:
                decoded_data = received_bytes.decode('utf-8').strip()
                print(f"Received: {decoded_data}")
                return decoded_data
            except UnicodeDecodeError:
                print(f"Received non-UTF-8 data: {received_bytes}")
        return None

except ImportError:
    print("Serial module not found. Not communicating via serial.")


time_between_redis_pulls = 1
time_to_show_text = 2

textPortfolioSetTime = time.time()
textSortSetTime = time.time()
textAutoCheckTime = time.time()
textStockSetTime = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sort", choices=['Name','Percent'], default=['Name'], help = "Sort stocks by Name")
parser.add_argument("-p", "--portfolio", choices=['All','Stocks','Options','Both','Speculation','Others'], default=['Options'], help = "Who's portfolio to show")
parser.add_argument("-e", "--equity", type=str, default="", help = "This should be a stock (equity) symbol, if an equity is entered, the auto function will be overridden 'No'")
parser.add_argument("-a", "--auto", choices=['Yes','No','Sync'], default=["Yes"], help = "automatically select the next stock after a few seconds of inactivity")
parser.add_argument("-r", "--refresh", default=10, help = "time in seconds to advance to the next stock")
# parser.add_argument("stock")
args = parser.parse_args()

if not os.path.isfile(".env"): 
    print("No .env file found, please create one with your API keys")
    quit()

# if args.equity != "":
    if args.auto == 'Sync':
        args.auto = ['Sync']

print('args.sort', args.sort)
print('args.portfolio', args.portfolio)
print('args.equity', args.equity)
print('args.auto', args.auto)
print('args.refresh', args.refresh)


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
        cyan = (0, 255, 255)
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
        test_x = 5
        test_y = 450
        displayStock = ""
        highPrice = 0
        lowPrice = 0
        stock_52_week_high = 0
        stock_52_week_low = 0
        currentPrice = 0
        largestDate = 0

        current_year = 0
        last_year = 0
        years = []
        all_option_dates = []
        while not done:
            clock.tick(30)
            today = datetime.date.today()
            current_year = today.year
            years = [current_year]
            equities = []
            redisFilterData = {}
            redisAllDataPull = copy.deepcopy(temp_dict)
            if SerialModuleEnabled:
                received_message = receive_data()
                if received_message:
                    last_received_message = received_message

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


            if 'All' in args.portfolio:
                for each in redisAllDataPull:
                    redisFilterData[each] = redisAllDataPull[each]
                    equities.append(each)
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
                
            temp = sorted(set(equities))
            equities = list(temp)

            ################################################################
            ################################################################
            ################################################################
            ################################################################
            ################################################################
            # THIS IS WHERE WE CALCULATE THE DATA TO BE DISPLAYED
            ################################################################
            ################################################################
            ################################################################
            ################################################################
            ################################################################


            try:
                if SerialModuleEnabled:
                    if args.auto == ['Sync']:
                        args.equity = [last_received_message]
                if args.equity == "":
                    args.equity = [equities[0]]
                if args.equity[0] not in equities:
                    args.equity = [equities[0]]
                displayStock = args.equity[0]
                # print('displayStock',displayStock)
                # print(redisAllDataPull[displayStock])
                highPrice = redisAllDataPull[displayStock]['52_week_high']
                lowPrice = redisAllDataPull[displayStock]['52_week_low']
                stock_52_week_high = redisAllDataPull[displayStock]['52_week_high']
                stock_52_week_low = redisAllDataPull[displayStock]['52_week_low']
                currentPrice = redisAllDataPull[displayStock]['price']
                largestDate = 0

                # order_details

                position_details = return_details("My_position_details")
                for each in position_details["securitiesAccount"]["positions"]:
                    if each["instrument"]["assetType"] == "OPTION":
                        if each["instrument"]["underlyingSymbol"] == displayStock:
                            optionSymbol = each["instrument"]["symbol"]
                            # print()
                            # print('optionSymbol',optionSymbol)
                            # print('len(optionSymbol)',len(optionSymbol))
                            strike = float(optionSymbol[13:21])/1000
                            # print('strike',strike)
                            highPrice = max(highPrice,strike)
                            lowPrice = min(lowPrice,strike)
                            expirationDate = optionSymbol[6:12]
                            largestDate = str(max(int(largestDate),int(expirationDate)))
                            # print ('largestDate',largestDate)
                            last_year = max(last_year,int(f'20{expirationDate[0:2]}'))
                            years.append(int(f'20{expirationDate[0:2]}'))
                            temp = list(set(years))
                            years = sorted(temp)
                all_option_dates = return_details("My_stock_option_dates")[displayStock]

                # print('all_option_dates',all_option_dates)
                # for each in all_option_dates[displayStock]:
                #     all_option_dates
                #             optionSymbol = each["instrument"]["symbol"]
                #             # print()
                #             # print('optionSymbol',optionSymbol)
                #             # print('len(optionSymbol)',len(optionSymbol))
                #             strike = float(optionSymbol[13:21])/1000
                #             # print('strike',strike)
                #             highPrice = max(highPrice,strike)
                #             lowPrice = min(lowPrice,strike)
                #             expirationDate = optionSymbol[6:12]
                #             largestDate = str(max(int(largestDate),int(expirationDate)))
                #             # print ('largestDate',largestDate)
                #             # last_year = max(last_year,int(f'20{expirationDate[0:2]}'))
                #             # years.append(int(f'20{expirationDate[0:2]}'))
                #             # temp = list(set(years))
                #             # years = sorted(temp)




                # if each in redisAllDataPull:
                #         redisFilterData[each] = redisAllDataPull[each]
                #         equities.append(each)
                # print()
                # print('displayStock',displayStock)
                # print('highPrice',highPrice)
                # print('stock_52_week_high',stock_52_week_high)
                # print('currentPrice',currentPrice)
                # print('lowPrice',lowPrice)
                # print('stock_52_week_low',stock_52_week_low)

                ##### FOR EACH IN THE LIST, GET THE DATA

            except:
                prRed("Error selecting equity")

            my_rect={}
            count = 0
            stockList = []
            for each in redisFilterData:
                stockList.append(redisFilterData[each])

            if 'Name' in args.sort:
                stocksSorted = sorted(stockList, key=lambda item: item["symbol"])
            elif 'Percent' in args.sort:
                stocksSorted = sorted(stockList, key=lambda item: item["change_percent"])

            background = (0,0,0)


            ################################################################
            ################################################################
            ################################################################
            ################################################################
            ################################################################
            # THIS IS WHERE WE VISUALIZE THE DATA ON THE SCREEN
            ################################################################
            ################################################################
            ################################################################
            ################################################################
            ################################################################

            pygame.draw.rect(display_surface, background, (0,0,x,y),width=0)
            pygame.draw.rect(display_surface, (100,100,0), (50,20,x-50-20,y-20-40),width=2)
            
            test_x += moving_x
            test_y += moving_y

            # Stock, top left
            font = pygame.font.Font('freesansbold.ttf', 15)
            textStock = font.render(f"{displayStock}", True, yellow, background)
            textStockRect = textStock.get_rect()
            textStockRect.centery = 10
            textStockRect.left = 5

            display_surface.blit(textStock, textStockRect)

            # high price, on the top
            font = pygame.font.Font('freesansbold.ttf', 15)
            textPriceHigh = font.render(f"{highPrice:.2f}", True, white, background)
            textPriceHighRect = textPriceHigh.get_rect()
            textPriceHighRect.centery = 35
            textPriceHighRect.left = 5
            display_surface.blit(textPriceHigh, textPriceHighRect)

            # low price, on the bottom
            font = pygame.font.Font('freesansbold.ttf', 15)
            textPriceLow = font.render(f"{lowPrice:.2f}", True, white, background)
            textPriceLowRect = textPriceLow.get_rect()
            textPriceLowRect.centery = 425
            textPriceLowRect.left = 5
            display_surface.blit(textPriceLow, textPriceLowRect)

            # if highPrice > stock_52_week_high:
            font = pygame.font.Font('freesansbold.ttf', 15)
            textPrice52High = font.render(f"{stock_52_week_high:.2f}", True, cyan, background)
            textPrice52HighRect = textPrice52High.get_rect()
            textPrice52HighRect.centery = textPriceLowRect.centery + (stock_52_week_high - lowPrice) * (textPriceHighRect.centery - textPriceLowRect.centery) / (highPrice - lowPrice)
            textPrice52HighRect.left = 5
            display_surface.blit(textPrice52High, textPrice52HighRect)
            leftside = 50
            rightside = 778
            for xskip in range(leftside, rightside, rightside//80):
                pygame.draw.line(display_surface, cyan, (xskip, textPrice52HighRect.centery), (xskip+5, textPrice52HighRect.centery), 1)
            # pygame.draw.line(display_surface, cyan, (50, textPrice52HighRect.centery), (778, textPrice52HighRect.centery), 1)
            

            # if lowPrice > stock_52_week_low:
            font = pygame.font.Font('freesansbold.ttf', 15)
            textPrice52Low = font.render(f"{stock_52_week_low:.2f}", True, cyan, background)
            textPrice52LowRect = textPrice52Low.get_rect()
            textPrice52LowRect.centery = textPriceLowRect.centery + (stock_52_week_low - lowPrice) * (textPriceHighRect.centery - textPriceLowRect.centery) / (highPrice - lowPrice)
            textPrice52LowRect.left = 5
            display_surface.blit(textPrice52Low, textPrice52LowRect)
            leftside = 50
            rightside = 778
            for xskip in range(leftside, rightside, rightside//80):
                pygame.draw.line(display_surface, cyan, (xskip, textPrice52LowRect.centery), (xskip+5, textPrice52LowRect.centery), 1)
            # pygame.draw.line(display_surface, cyan, (50, textPrice52LowRect.centery), (778, textPrice52LowRect.centery), 1)


            # current price, proportional to the high and low price
            font = pygame.font.Font('freesansbold.ttf', 15)
            textPriceCur = font.render(f"{currentPrice:.2f}", True, yellow, background)
            textPriceCurRect = textPriceCur.get_rect()
            textPriceCurRect.centery = textPriceLowRect.centery + (currentPrice - lowPrice) * (textPriceHighRect.centery - textPriceLowRect.centery) / (highPrice - lowPrice)
            textPriceCurRect.left = 5
            display_surface.blit(textPriceCur, textPriceCurRect)
            leftside = 45
            rightside = 778
            for xskip in range(leftside, rightside, rightside//30):
                pygame.draw.line(display_surface, yellow, (xskip, textPriceCurRect.centery), (xskip+10, textPriceCurRect.centery), 1)
            # pygame.draw.line(display_surface, yellow, (45, textPriceCurRect.centery), (778, textPriceCurRect.centery), 1)

            


            # First date, on the left
            font = pygame.font.Font('freesansbold.ttf', 15)
            today = datetime.date.today()
            current_month = today.month
            current_day = today.day
            current_year = today.year
            textDate1 = font.render(f"{current_month}/{current_day}", True, white, background)
            textDateRect1 = textDate1.get_rect()
            textDateRect1.center = (50 , 450)
            display_surface.blit(textDate1, textDateRect1)

            # last date. on the right
            font = pygame.font.Font('freesansbold.ttf', 15)
            # print ('largestDate',largestDate)
            lastdateString = str(f'20{largestDate}')
            # last_date = datetime.datetime.strptime(str(f'20{largestDate}'), '%Y%m%d')
            
            today = datetime.datetime.today()
            last_date = today
            for each in all_option_dates:
                each_datetime = datetime.datetime.strptime(each, '%Y-%m-%d')
                if each_datetime >= last_date:
                    last_date = each_datetime
                years.append(each_datetime.year)
            # print(last_date,'last_date')
            last_month = last_date.month
            last_day = last_date.day
            last_year = last_date.year
            textDateN = font.render(f"{last_month}/{last_day}", True, white, background)
            textDateRectN = textDateN.get_rect()
            textDateRectN.center = (780, 450)
            display_surface.blit(textDateN, textDateRectN)
            # print(args.equity[0])
            # print('years',years)

            all_dates = copy.deepcopy(all_option_dates)
            all_dates.insert(0,f'{today.year}-{today.month:02d}-{today.day:02d}')
            # print('all_dates',all_dates)
            # between dates

            # print()
            # print('test dates')
            for each in all_dates[1:-1]:
                font = pygame.font.Font('freesansbold.ttf', 15)
                each_datetime = datetime.datetime.strptime(each, '%Y-%m-%d')
                each_month = each_datetime.month
                each_day = each_datetime.day
                # print('each_month/each_day')
                # print(f'{each_month}/{each_day}')
                text1 = font.render(f"{each_month}/{each_day}", True, white, background)
                textRect1 = text1.get_rect()
                textRect1.centery = textDateRect1.centery
                textRect1.centerx = 50 + (all_dates.index(each)) * (textDateRectN.centerx - textDateRect1.centerx) / (len(all_dates)-1)
                display_surface.blit(text1, textRect1)

            for each in position_details["securitiesAccount"]["positions"]:
                if each["instrument"]["assetType"] == "OPTION":
                    if each["instrument"]["underlyingSymbol"] == displayStock:
                        optionSymbol = each["instrument"]["symbol"]
                        typeOption = optionSymbol[12:13]
                        strike = float(optionSymbol[13:21])/1000
                        tempDate = optionSymbol[6:12]
                        expirationDateTime = datetime.datetime.strptime(f'20{tempDate}', '%Y%m%d')
                        expirationDate = expirationDateTime.strftime('%Y-%m-%d')
                        # print('optionSymbol',optionSymbol)
                        # print('typeOption',typeOption)
                        # print('expirationDate',expirationDate)
                        # print('strike',strike)
                        circlex = 50 + (all_dates.index(expirationDate)) * (textDateRectN.centerx - textDateRect1.centerx) / (len(all_dates)-1)
                        circley = textPriceLowRect.centery + (strike - lowPrice) * (textPriceHighRect.centery - textPriceLowRect.centery) / (highPrice - lowPrice)
                        if optionSymbol in list_of_symbol_open_orders:
                            circleColor = yellow
                            pygame.draw.circle(display_surface, circleColor, (circlex,circley), 6)
                            circleSize = 4
                        else:
                            circleSize = 5
                        if typeOption == 'C':
                            circleColor = (0,255,0)
                        elif typeOption == 'P':
                            circleColor = (255,0,0)
                        pygame.draw.circle(display_surface, circleColor, (circlex,circley), circleSize)

                        # circley = 50 + (all_dates.index(expirationDate)) * (textDateRectN.centerx - textDateRect1.centerx) / (len(all_dates)-1)



            try:
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

                if time.time() - textAutoCheckTime  < time_to_show_text:
                    font2 = pygame.font.Font('freesansbold.ttf', 30)
                    textSort = font2.render(f'Auto scrolling: {args.auto[0]}', True, yellow, background)
                    textSortRect = textSort.get_rect()
                    x, y = display_surface.get_size()
                    cx = x * 1/3
                    SortOption = {'Yes':3,'No':4,'Sync':5}
                    cy = y * SortOption[args.auto[0]]/7
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
            except:
                prRed("Error checking text against time")
                # time.sleep(1)
                # pass

                
            # elif DataShown == 1: #'Stocks'

            pygame.display.update()

            moving_x = 0
            moving_y = 0

            action = 0
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        action = 6
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

            if action == 6:
                    textAutoCheckTime = time.time()
                    if 'No' in args.auto:
                        args.auto = ['Yes']
                        prRed("Now auto scrolling")
                    elif 'Sync' in args.auto:
                        args.auto = ['No']
                        prRed("Now NOT auto scrolling")
                    elif 'Yes' in args.auto:
                        if SerialModuleEnabled:
                            args.auto = ['Sync']
                            prRed("Now syncing to Serial Input")
                        else:
                            args.auto = ['No']
                            prRed("Now NOT auto scrolling")



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


