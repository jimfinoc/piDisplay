import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import numpy as np
from matplotlib.widgets import Cursor, MultiCursor
import matplotlib.dates as mdates
from matplotlib.widgets import Button
from matplotlib.backend_bases import MouseButton

# from stockDataFunctions import return_details
# from stockDataFunctions import return_positions
# from stockDataFunctions import return_orders
from stockDataFunctions import RedisConnection

from datetime import datetime
import pandas as pd
# import time

import argparse

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prBlue(skk): print("\033[94m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--equity", type=str, default="", help = "This should be a stock (equity) symbol, if an equity is entered, the auto function will be overridden 'No'")
args = parser.parse_args()




current_time = datetime.now()
start_time = current_time
prYellow(f"starttime: {start_time}")

myRedis = RedisConnection()
myRedis.connect()

equities = myRedis.return_positions(type = "all")

equity_set = set(equities)
equities = list(equity_set)
equities.sort()
print("equities")
print(equities)

if args.equity == "":
    args.equity = [equities[0]]
if args.equity[0] not in equities:
    args.equity = [equities[0]]

stock_history = myRedis.return_details("My_stock_history")
# random_key = random.choice(equities)
random_key = args.equity[0]

stock_history_candles = myRedis.return_details("My_stock_history")[random_key]['candles']
print(random_key)
print("stock_history_candles")
print(stock_history_candles[0])
print("len(stock_history_candles)")
print(len(stock_history_candles))

data = {
    'Date': [],
    'Open': [],
    'High': [],
    'Low': [],
    'Close': []
}

for each in stock_history_candles:
    data['Date'].append(datetime.fromtimestamp(each['datetime'] / 1000))  # Convert milliseconds to datetime
    # data['Date'].append(each['datetime'] / 1000)  # Convert milliseconds to datetime
    data['Open'].append(each['open'])
    data['High'].append(each['high'])
    data['Low'].append(each['low'])
    data['Close'].append(each['close'])

df = pd.DataFrame(data).set_index('Date')

# mpl_date_num = mdates.date2num(date_object)
# df['Date_mpl'] = mdates.date2num(df.index)
df['Date_mpl'] = mdates.date2num(df.index.to_pydatetime())

up_color = 'green'
down_color = 'red'
width = 0.2
width2 = 1.0 # For wicks


print("df:")
print(df)

min_value = df['Date_mpl'].min()

# Get the maximum value of 'Column1'
max_value = df['Date_mpl'].max()

print(f"Minimum value of Column1: {min_value}")
print(f"Maximum value of Column1: {max_value}")

# quit()



displayStock = random_key

print("displayStock")
print(displayStock)
print()
all_options_dates_for_specific_stock = myRedis.return_details("All_stock_option_dates")[displayStock]

todays_date = current_time.strftime("%Y-%m-%d")
if todays_date not in all_options_dates_for_specific_stock:
    if todays_date < all_options_dates_for_specific_stock[0]:
        all_options_dates_for_specific_stock.insert(0, todays_date)
    else:
        all_options_dates_for_specific_stock.insert(1, todays_date)

# print(todays_date)


# print("all_options_dates_for_specific_stock")
# print(all_options_dates_for_specific_stock)

all_options__noyear_dates_for_specific_stock = []
for each in all_options_dates_for_specific_stock:
    all_options__noyear_dates_for_specific_stock.append(each[5:])

# print("all_options__noyear_dates_for_specific_stock")
# print(all_options__noyear_dates_for_specific_stock)


My_quotes = myRedis.return_details("My_quotes")

stock_52_week_high = My_quotes[displayStock]['52_week_high']
stock_52_week_low = My_quotes[displayStock]['52_week_low']
highPrice = stock_52_week_high
lowPrice = stock_52_week_low

currentPrice = My_quotes[displayStock]['price']
position_details = myRedis.return_details("My_position_details")

prYellow(f"time_hack 4: {datetime.now()}")

strikes_calls = []
strikes_puts = []
dates_index_calls = []
dates_index_puts = []
date_range = slice(6,12)
call_put_range = slice(12,13)
strike_range = slice(13,21)
for each in position_details["securitiesAccount"]["positions"]:
    if each["instrument"]["assetType"] == "OPTION":
        if each["instrument"]["underlyingSymbol"] == displayStock:
            optionSymbol = each["instrument"]["symbol"]
            # print()
            print('optionSymbol',optionSymbol)
            # print('len(optionSymbol)',len(optionSymbol))
            strike = float(optionSymbol[strike_range])/1000
            # print('strike',strike)
            highPrice = max(highPrice,strike)
            lowPrice = min(lowPrice,strike)
            # print('highPrice', highPrice)  
            # print('lowPrice', lowPrice)
            expirationDate = optionSymbol[date_range]
            datetime_object = datetime.strptime(expirationDate, '%y%m%d')
            output_format = '%Y-%m-%d'
            date_string = datetime_object.strftime(output_format)
            # dates.append(expirationDate)
            # date = "20"+expirationDate
            # print('expirationDate',expirationDate)
            # print("optionSymbol[call_put_range]")
            # print(optionSymbol[call_put_range])
            if optionSymbol[call_put_range] == 'C':
                strikes_calls.append(strike)
                dates_index_calls.append(all_options_dates_for_specific_stock.index(date_string))
            elif optionSymbol[call_put_range] == 'P':
                strikes_puts.append(strike)
                dates_index_puts.append(all_options_dates_for_specific_stock.index(date_string))  
            # print('date',date)



            # largestDate = str(max(int(largestDate),int(expirationDate)))
            # print ('largestDate',largestDate)
            # last_year = max(last_year,int(f'20{expirationDate[0:2]}'))
            # years.append(int(f'20{expirationDate[0:2]}'))
            # temp = list(set(years))
            # years = sorted(temp)

prYellow(f"time_hack 5: {datetime.now()}")

# print('highPrice', highPrice)
# print('lowPrice', lowPrice)
# print("stock_52_week_high",stock_52_week_high)
# print('stock_52_week_low',stock_52_week_low)

print()
print("strikes_calls",strikes_calls)
print()
print("dates_index_calls",dates_index_calls)
print()
print()
print("strikes_puts",strikes_puts)
print()
print("dates_index_puts",dates_index_puts)
print()

mosaic = """
         LR
         LR
         LR
         """

# Create the figure and axes
plt.style.use('dark_background')
fig, axd = plt.subplot_mosaic(mosaic, layout="constrained", figsize=(10, 6))
# fig, axd = plt.subplot_mosaic(mosaic, layout="constrained")
fig.get_layout_engine().set(
    w_pad=0.2,    # Set width padding to 4 points (approx inches)
    h_pad=0.05,    # Set height padding to 4 points
    hspace=0,       # Set vertical spacing as a fraction of subplot height
    wspace=0        # Set horizontal spacing as a fraction of subplot width
)

# Plot bullish days (close > open)
up = df[df['Close'] >= df['Open']]
axd['L'].bar(up['Date_mpl'], up['Close'] - up['Open'], width, bottom=up['Open'], color=up_color, edgecolor='black')
axd['L'].vlines(up['Date_mpl'], up['Low'], up['High'], color=up_color, linewidth=width2)

# Plot bearish days (close < open)
down = df[df['Close'] < df['Open']]
axd['L'].bar(down['Date_mpl'], down['Open'] - down['Close'], width, bottom=down['Close'], color=down_color, edgecolor='black')
axd['L'].vlines(down['Date_mpl'], down['Low'], down['High'], color=down_color, linewidth=width2)

# axd['L'].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'), rotation=80)
existing_ticks = axd['L'].get_xticks()
print("existing_ticks")
print(existing_ticks)
print("mdates.num2date(existing_ticks)")
print(mdates.num2date(existing_ticks))
format_pattern = "%m-%d"
date_string_list = [dt.strftime(format_pattern) for dt in mdates.num2date(existing_ticks)]
print("date_string_list")
print(date_string_list)
axd['L'].set_xticks(existing_ticks, date_string_list,rotation=80) # Rotate labels to prevent overlap
# quit() 

axd['R'].scatter(dates_index_calls, strikes_calls, color='green')
axd['R'].scatter(dates_index_puts, strikes_puts, color='red')
axd['R'].set_title('Options Timeline')
axd['L'].set_title('Stock History')
# axd['R'].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

axd['R'].axhline(y=stock_52_week_high, color='cyan', linestyle='--', label='52 Week High')
axd['R'].axhline(y=stock_52_week_low, color='cyan', linestyle='--', label='52 Week Low')
axd['L'].axhline(y=stock_52_week_high, color='cyan', linestyle='--', label='52 Week High')
axd['L'].axhline(y=stock_52_week_low, color='cyan', linestyle='--', label='52 Week Low')


    
##### This finds the index for the next new years dates so they may be plotted on the timeline
now = datetime.now()
next_nyd = []
next_nyd_index = []
next_nyd.append(datetime(year=now.year+0, month=1, day=1))
next_nyd.append(datetime(year=now.year+1, month=1, day=1))
next_nyd.append(datetime(year=now.year+2, month=1, day=1))
next_nyd.append(datetime(year=now.year+3, month=1, day=1))
next_nyd_index.append(0)
next_nyd_index.append(1)
next_nyd_index.append(2)
next_nyd_index.append(3)
for each_index in [1,2,3]:
    # prPurple(next_nyd[each_index].strftime('%Y-%m-%d'))
    # prGreen("all_options_dates_for_specific_stock")
    for each_date in range(len(all_options_dates_for_specific_stock)):
        # prRed(all_options_dates_for_specific_stock[each_date])
        if all_options_dates_for_specific_stock[each_date] < next_nyd[each_index].strftime('%Y-%m-%d'):
            next_nyd_index[each_index] = each_date + 0.5
        pass

axd['L'].axvline(next_nyd[0], color='0.3', linestyle=':')

axd['R'].axvline(next_nyd_index[1], color='0.3', linestyle=':')
axd['R'].axvline(next_nyd_index[2], color='0.3', linestyle=':')
axd['R'].axvline(next_nyd_index[3], color='0.3', linestyle=':')

if all_options_dates_for_specific_stock.index(todays_date) == 0:
    index = list(range(0, len(all_options_dates_for_specific_stock)))
    print("all ticks")
    axd['R'].set_xlim(left=0) # Use 'left' argument
    axd['R'].set_xticks(index, all_options__noyear_dates_for_specific_stock[0:],rotation=80) # Rotate labels to prevent overlap
    # plt.xticks(index, all_options__noyear_dates_for_specific_stock)
elif all_options_dates_for_specific_stock.index(todays_date) == 1:
    index = list(range(1, len(all_options_dates_for_specific_stock)))
    print("all but first tick")
    axd['R'].set_xlim(left=1) # Use 'left' argument
    axd['R'].set_xticks(index, all_options__noyear_dates_for_specific_stock[1:],rotation=80) # Rotate labels to prevent overlap
     
axd['R'].set_xlim(right=len(all_options_dates_for_specific_stock)) # Use 'left' argument

axd['L'].set_xlim(right= df['Date_mpl'].max()) # Use 'left' argument
axd['L'].set_xlim(left= df['Date_mpl'].min()) # Use 'left' argument


axd['L'].set_ylabel('Price ($)')
axd['L'].set_xlabel('Date')
axd['R'].set_ylabel('Strike Price ($)')
axd['R'].set_xlabel('Expiration Dates')
axd['L'].set_ylim(axd['R'].get_ylim())
# multi2 = MultiCursor(None, (axd['L'], axd['V']), color='r', lw=1, horizOn=True, vertOn=True)
multi1 = MultiCursor(None, (axd['L'], axd['R']), color='r', lw=1, horizOn=True, vertOn=False)
cursorR = Cursor(axd['R'], useblit=True, color='red', linewidth=1)
cursorL = Cursor(axd['L'], useblit=True, color='red', linewidth=1)

# first_term = 'A'
    # multi2 = MultiCursor(None, (axd['R'], axd['B'], axd['C']), color='w', lw=1, horizOn=True, vertOn=True)


# Add a title for the entire figure
# fig.suptitle('Basic Mosaic Layout Example')

change = My_quotes[displayStock]['change']
price_str = f"${currentPrice:.2f}"
change_str = f"{change:+.2f}"

updating_title = False

if updating_title:
    fig.text(
        x=0.5, y=0.96, # Adjust y position as needed, 0.96 works well for a suptitle
        s=displayStock,
        fontsize=20,
        ha="center", # Horizontal alignment
        color="yellow",
        transform=fig.transFigure # Use figure coordinates
    )

    change = My_quotes[displayStock]['change']

    price_str = f"${currentPrice:.2f}"
    change_str = f"{change:+.2f}"
    if change >= 0:
        change_color = 'green'
    elif change < 0:
        change_color = 'red'
    elif change == 0:
        change_color = 'white'

    fig.text(
        x=0.5, y=0.92, # Position slightly lower than the first part
        s=price_str + " " + change_str,
        fontsize=14,
        ha="center",
        color=change_color,
        transform=fig.transFigure
    )
else:
    fig.supxlabel(price_str + " " + change_str, color='white', fontsize=14)
    fig.suptitle(
        displayStock, color='yellow',
        fontsize=20,
)

# Optional: Adjust subplot parameters to prevent titles from overlapping with plots
plt.subplots_adjust(top=0.85)

tick_labels = axd['R'].get_xticklabels()
tick_lines = axd['R'].get_xticklines()
tick_labels[0].set_color('yellow')
tick_lines[0].set_color('yellow')

live_update = True

class Index:
    ind = 0

    def next(self, event):
        self.ind += 1
        i = self.ind % len(equities)
        fig.suptitle(equities[i], color='yellow', fontsize=20)

        plt.draw()

    def prev(self, event):
        self.ind -= 1
        i = self.ind % len(equities)
        fig.suptitle(equities[i], color='yellow', fontsize=20)
        # fig.suptitle(displayStock, color='red', fontsize=20)

        plt.draw()

callback = Index()
axprev = fig.add_axes([0.01, 0.01, 0.1, 0.05])
axnext = fig.add_axes([0.89, 0.01, 0.1, 0.05])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

keep_plotting = True
plt.ion() 

def time_to_close(event):
    prRed("time_to_close called")
    global keep_plotting
    keep_plotting = False
    plt.close()  # Close the plot window
    quit()
    
def on_click(event):
    prRed(f"you pressed: {event.key} {event.button}")
    global keep_plotting
    if event.button is MouseButton.RIGHT:
        keep_plotting = False
        # plt.close()  # Close the plot window
        quit()


# binding_id = plt.connect('motion_notify_event', on_move)
# plt.connect('button_press_event', on_click)


if live_update:
    while keep_plotting:
        My_quotes = myRedis.return_details("My_quotes")
        plt.connect('close_event', time_to_close)
        plt.connect('button_press_event', on_click)

        currentPrice = My_quotes[displayStock]['price']
        change = My_quotes[displayStock]['change']
        
        price_str = f"${currentPrice:.2f}"
        change_str = f"{change:+.2f}"

        change_str = f"{change:+.2f}"
        if change >= 0:
            change_color = 'green'
        elif change < 0:
            change_color = 'red'
        elif change == 0:
            change_color = 'white'

        # plt.title(f'Current Price: ${currentPrice:.2f}', color='yellow')
        fig.supxlabel(price_str + " " + change_str, color=change_color, fontsize=14)

        axd['L'].axhline(y=currentPrice, color='yellow', label='Current Price', linestyle=':')
        axd['R'].axhline(y=currentPrice, color='yellow', label='Current Price', linestyle=':')
        plt.draw()
        plt.pause(1)

else:
    plt.show()