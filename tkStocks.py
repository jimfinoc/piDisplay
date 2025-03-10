import tkinter as tk
from tkinter import ttk

import datetime
import math
import json
from urllib.request import urlopen 
import redis
from dotenv import load_dotenv
import os

window = tk.Tk()
my_geometry = 700
afterTime = 5 * 60 * 1000 # time is in milliseconds
# x_geometry = my_geometry
# y_geometry = my_geometry
x_geometry = 1280
y_geometry = 720-16
# x_geometry = 800
# y_geometry = 400-16
pad = 10
padx = pad
pady = pad
window.geometry(f"{x_geometry}x{y_geometry}+0+0")
window.title("Stock Details")

style = ttk.Style()
style.configure("W.TLabel", foreground="white")
style.configure("G.TLabel", foreground="green")
style.configure("R.TLabel", foreground="red")

def return_details(key):
    # try:
    load_dotenv(".env")
    r = redis.Redis(db=0,host=os.getenv("redis_database_name"),port=os.getenv("redis_database_port"),password=os.getenv("redis_database_password"))
    My_details_string = r.get(key)
    My_details = json.loads(My_details_string)
    with open("."+str(key)+".json", "w") as file:
        json.dump(My_details, file, indent=4)

    # except:
        # pass
    return My_details

def return_orders(status = "open"):
    returnData = []
    orders_details = return_details("My_orders_details")
    for each in orders_details:
        # print()
        # print(each)
        if status == "all":
            pass
        elif status == "open":
            if each['status'] == 'PENDING_ACTIVATION':
                returnData.append(each)
        elif status == "filled":
            if each['status'] == 'FILLED':
                returnData.append(each)
    return returnData

def return_positions(type = "all"):
    returnData = []
    stocks = set()
    position_details = return_details("My_position_details")
    for each in position_details["securitiesAccount"]["positions"]:
        if type == "all" or type == "option":
            if each["instrument"]["assetType"] == "OPTION":
                # print(each["instrument"]["underlyingSymbol"])
                stocks.add(each["instrument"]["underlyingSymbol"])
        if type == "all" or type == "stock":
            if each["instrument"]["assetType"] == "EQUITY":
                # print(each["instrument"]["symbol"])
                stocks.add(each["instrument"]["symbol"])
    return stocks

def all_dates(stock_option_dates):
    key = set()
    for each_stock in stock_option_dates:
        for each_date in stock_option_dates[each_stock]:
            key.add(each_date)
        # with open("."+str(key)+".json", "w") as file:
            # json.dump(My_details, file, indent=4)
    return key

print(1)
My_stocks = return_details("My_stocks")
print(2)
My_order_details = return_details("My_orders_details")
print(3)
My_position_details = return_details("My_position_details")
print(4)
My_stock_option_dates = return_details("My_stock_option_dates")
print(5)
My_lot_details = return_details("My_lot_details")
# print(6)
# My_stock_option_strikes = return_details("My_stock_option_strikes")

# All_stock_option_dates = all_dates(My_stock_option_dates)
all_dates(My_stock_option_dates)
My_dates = list(all_dates(My_stock_option_dates))
My_dates.sort()

# print()
# print("My_dates")
# print(My_dates)
# print(len(My_dates))
# print()


# My_stocks = return_positions("all")

My_owned_stocks = return_positions("stock")
# My_involved_options = return_positions("option")

My_open_orders = return_orders("open")

# My_filled_orders = return_orders("filled")
My_involved_all = list(return_positions("all"))
My_involved_all.sort()


# print()
# print("My_involved_all")
# print(My_involved_all)
# print(len(My_involved_all))
# print()

########################################################################
#### Set up of the tabs
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

tabControl = ttk.Notebook(window)
tabControl.columnconfigure(0, weight=1)

tab = {}
########################################################################
special = "Stocks and Options"

# special = "Options"
tab[special] = ttk.Frame(tabControl,padding=5)
tab[special].columnconfigure(0, weight=1)
tab[special].columnconfigure(1, weight=1)
tabControl.add(tab[special], text=special)
side_left = ttk.Frame(tab[special], width = tab[special].winfo_width()/2)#.grid(column=0, row=0,sticky="new")
side_right = ttk.Frame(tab[special], width = tab[special].winfo_width()/2)#.grid(column=1, row=0,sticky="new")
# side_left.columnconfigure(1, weight=1)
# side_right.columnconfigure(1, weight=1)

# side_left.pack(side=tk.LEFT, fill=tk.X)
# side_left.pack(fill=tk.Y)
# side_left.pack(side=tk.LEFT, fill="both")
# side_right.pack(side=tk.TOP, fill=tk.Y)
# side_right.pack(side=tk.TOP, fill="both")
# side_right.pack(side=tk.RIGHT, fill="both")

side_left.grid(column=0, row=0,padx=30, pady=30,sticky=(tk.W, tk.E, tk.N, tk.S))
# side_left.grid(sticky=tk.N+tk.E+tk.S+tk.W)
side_right.grid(column=1, row=0,padx=30, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
# side_right.grid(sticky=tk.E+tk.S+tk.W)
# side_left.columnconfigure(0, weight=1)
# side_right.columnconfigure(1, weight=1)

# tab[special] = ttk.Frame(tabControl)
# tabControl.add(tab[special], text=special)
# ttk.Label(tab["Stocks"], text ="This should contain a table of my owned stocks").grid(column = 0,  row = 0, padx = 30, pady = 30)   
stock_row = 0
# ttk.Label(side_left, text ="Symbol",anchor=tk.CENTER).grid(column = 0,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="Symbol").grid(column = 0,  row = stock_row, padx = 10, pady = 0,sticky="n")   
ttk.Label(side_left, text ="Quantity").grid(column = 1,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="net Change").grid(column = 3,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="Market Value").grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
ttk.Label(side_left, text ="Profit/Loss").grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

stock_row += 1
ttk.Label(side_left, text ="-----").grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="-----").grid(column = 1,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="-----").grid(column = 2,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="-------").grid(column = 3,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="----------").grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
ttk.Label(side_left, text ="----------").grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

total_market_value = 0.0
total_profit_loss = 0.0
for each in My_position_details["securitiesAccount"]["positions"]:
    if each["instrument"]["assetType"] == "EQUITY":
        stock_row += 1
        # print(each)
        ttk.Label(side_left, text = each["instrument"]["symbol"] ).grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
        ttk.Label(side_left, text = f'{each["longQuantity"]:.0f}' ).grid(column = 1,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
        # ttk.Label(side_left, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 10)
        # ttk.Label(side_left, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 10, pady = 10)
        ttk.Label(side_left, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 0, pady = 0 ,sticky="e")
        # ttk.Label(side_left, text = each["currentDayProfitLossPercentage"]).grid(column = 4,  row = stock_row, padx = 10, pady = 10)

        market_value = each["marketValue"]
        total_market_value += market_value
        ttk.Label(side_left, text = f'{market_value:.2f}').grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

        profit_loss = each["longOpenProfitLoss"]
        total_profit_loss += profit_loss
        ttk.Label(side_left, text = f'{profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

stock_row += 1
ttk.Label(side_left, text ="-----").grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="-----").grid(column = 1,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="-----").grid(column = 2,  row = stock_row, padx = 10, pady = 0)   
ttk.Label(side_left, text ="-------").grid(column = 3,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="----------").grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
ttk.Label(side_left, text ="----------").grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

stock_row += 1
# ttk.Label(side_left, text ="").grid(column = 0,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="").grid(column = 1,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="").grid(column = 2,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="net Change").grid(column = 3,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
# ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text =f'{total_market_value}').grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
ttk.Label(side_left, text =f'{total_profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 0, sticky="e")


########################################################################
# Not SEPERATE! this is combined with the Stock tab
# special = "Options"
# tab[special] = ttk.Frame(tabControl)
# tabControl.add(tab[special], text=special)
# side_left = ttk.Frame(tab[special], width = tab[special].winfo_width()/2)
# side_left.pack(side=tk.LEFT, fill=tk.Y)
# side_right = ttk.Frame(tab[special], width = tab[special].winfo_width()/2)
# # side_right.pack(side=tk.RIGHT, fill=tk.Y)
# side_right.pack(fill=tk.Y)
# option_label = []

date_row = 0
label = ttk.Label(side_right,text="Expiration Date")
label.grid(column = 0, row = date_row, pady=0,padx=10,sticky='E')
label = ttk.Label(side_right,text="Calls")
label.grid(column = 1, row = date_row, pady=0,padx=10)
label = ttk.Label(side_right,text="Puts")
label.grid(column = 2, row = date_row, pady=0,padx=10)
label = ttk.Label(side_right,text="Days")
label.grid(column = 3, row = date_row, pady=0,padx=10)

total_calls = {}
total_puts = {}
for each in My_position_details["securitiesAccount"]["positions"]:
    if each["instrument"]["assetType"] == "OPTION":
        year = f'20{each["instrument"]["symbol"][6:8]}'
        month = f'{each["instrument"]["symbol"][8:10]}'
        day = f'{each["instrument"]["symbol"][10:12]}'
        special_date = f'{year}-{month}-{day}'
        quantity = each["shortQuantity"]
            # print("special_date")
            # print(special_date)
        if each["instrument"]["putCall"] == "CALL":
            if special_date in total_calls:
                total_calls[special_date] += quantity
            else:
                total_calls[special_date] = quantity
        elif each["instrument"]["putCall"] == "PUT":
            if special_date in total_puts:
                total_puts[special_date] += quantity
            else:
                total_puts[special_date] = quantity

for each in My_dates:
    date_row += 1
    label = ttk.Label(side_right,text=str(each))
    label.grid(column = 0, row = date_row, pady=0,padx=10)
    
    if each in total_calls:
        label = ttk.Label(side_right,text=f'{total_calls[each]:.0f}')
    else:
        label = ttk.Label(side_right,text="0", foreground="gray")
    label.grid(column = 1, row = date_row, pady=0,padx=10)

    if each in total_puts:
        label = ttk.Label(side_right,text=f'{total_puts[each]:.0f}')
    else:
        label = ttk.Label(side_right,text="0", foreground="gray")
    label.grid(column = 2, row = date_row, pady=0,padx=10)
    # print(each)
    now = datetime.datetime.now()
    date1 = datetime.date(now.year,now.month,now.day)
    date2 = datetime.date.fromisoformat(each)
    differece = date2-date1
    # print(date1,date2,differece.days)
    label = ttk.Label(side_right,text=str(differece.days), foreground="gray")
    label.grid(column = 3, row = date_row, pady=0,padx=10)

    # option_label.append(label)
# ttk.Label(tab["Options"], text ="This should contain a table of my options expiring over time").grid(column = 0, row = 0, padx = 30, pady = 30) 

date_row += 1
label = ttk.Label(side_right,text="-------------")
label.grid(column = 0, row = date_row, pady=0,padx=10)
label = ttk.Label(side_right,text="----")
label.grid(column = 1, row = date_row, pady=0,padx=10)
label = ttk.Label(side_right,text="----")
label.grid(column = 2, row = date_row, pady=0,padx=10)
label = ttk.Label(side_right,text="----")
label.grid(column = 3, row = date_row, pady=0,padx=10)

date_row += 1
number_calls = 0
for each in total_calls:
    number_calls += total_calls[each]
label = ttk.Label(side_right,text=f'{number_calls:.0f}')
label.grid(column = 1, row = date_row, pady=0,padx=10)

number_puts = 0
for each in total_puts:
    number_puts += total_puts[each]
label = ttk.Label(side_right,text=f'{number_puts:.0f}')
label.grid(column = 2, row = date_row, pady=0,padx=10)



########################################################################
special = "Open"
tab[special] = ttk.Frame(tabControl)
tab[special].grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
tab[special].columnconfigure(0, weight=4)
tab[special].columnconfigure(1, weight=1)
tab[special].columnconfigure(2, weight=1)
tab[special].columnconfigure(3, weight=1)
tab[special].columnconfigure(4, weight=1)
# tab[special].rowconfigure(0, weight=1)

tabControl.add(tab[special], text=special)
# ttk.Label(tab["Open"], text ="This should contain a list of open orders").grid(column = 0, row = 0, padx = 30, pady = 30) 

order_row = 0
ttk.Label(tab[special], text ="Description").grid(column = 0,  row = order_row, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Remaining Quantity").grid(column = 1,  row = order_row, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Price").grid(column = 2,  row = order_row, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Duration").grid(column = 3,  row = order_row, padx = 10, pady = 10)
ttk.Label(tab[special], text ="Instruction").grid(column = 4,  row = order_row, padx = 10, pady = 10)
# ttk.Label(tab[special], text ="Day Percent Change").grid(column = 4,  row = order_row, padx = 10, pady = 10)   
# ttk.Label(tab[special], text ="Market Value").grid(column = 5,  row = order_row, padx = 10, pady = 10 ,sticky="e")   
# ttk.Label(tab[special], text ="Profit/Loss").grid(column = 6,  row = order_row, padx = 10, pady = 10 ,sticky="e")   

for each in My_open_orders:
    for leg in each['orderLegCollection']:
        order_row += 1
        description = leg['instrument']['description']
        remainingQuantity = each['quantity']
        price = each['price']
        duration = each['duration']
        if duration == "GOOD_TILL_CANCEL":
            duration = "GTC"
        instruction = leg['instruction']
        if instruction == "BUY_TO_CLOSE":
            instruction = 'BTC'
        elif instruction == "BUY_TO_OPEN":
            instruction = 'BTO'
        elif instruction == "SELL_TO_CLOSE":
            instruction = 'STC'
        elif instruction == "SELL_TO_OPEN":
            instruction = 'STO'


        ttk.Label(tab[special], text = f'{description}').grid(column = 0,  row = order_row, padx = 10, pady = 10, sticky="e")   
        ttk.Label(tab[special], text = f'{remainingQuantity:.0f}').grid(column = 1,  row = order_row, padx = 10, pady = 10)   
        ttk.Label(tab[special], text = f'{price:.02f}').grid(column = 2,  row = order_row, padx = 10, pady = 10, sticky="e")   
        ttk.Label(tab[special], text = f'{duration}').grid(column = 3,  row = order_row, padx = 10, pady = 10)   
        ttk.Label(tab[special], text = f'{instruction}').grid(column = 4,  row = order_row, padx = 10, pady = 10)   
# print()
# print("My_open_orders")
# print(My_open_orders)
# print(len(My_open_orders))
# print()

########################################################################
#this is for each of the individual stocks

# for each in range(len(My_involved_all)):
for each_stock in My_involved_all:
    tab[each_stock] = ttk.Frame(tabControl,padding=5)
    tab[each_stock].columnconfigure(0, weight=1) # for centering the left half of the tab
    tab[each_stock].columnconfigure(1, weight=1) # for centering the right half of the tab
    tabControl.add(tab[each_stock], text=each_stock)
    side_left = ttk.Frame(tab[each_stock], width = tab[special].winfo_width()/2)#.grid(column=0, row=0,sticky="new")
    side_right = ttk.Frame(tab[each_stock], width = tab[special].winfo_width()/2)#.grid(column=1, row=0,sticky="new")
    side_left.grid(column=0, row=0,padx=30, pady=30,sticky=(tk.W, tk.E, tk.N, tk.S))
    side_right.grid(column=1, row=0,padx=30, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    lot_row = 0
    print("Stock:")
    print(each_stock)
    ttk.Label(side_left, text = each_stock).grid(column = 0,  row = lot_row, padx = 10, pady = 1,sticky="n")   
    if each_stock in My_lot_details:
        as_of = f'As of: {My_lot_details[each_stock]["data_pull_time_date"]}'
    else:
        as_of = f"No shares owned"
    ttk.Label(side_left, text = as_of).grid(column = 1,  row = lot_row, padx = 10, pady = 1,sticky="w",columnspan=3)
    print(as_of)
        
    lot_row += 1
    ttk.Label(side_left, text ="Open Date").grid(column = 0,  row = lot_row, padx = 10, pady = 0,sticky="n")   
    ttk.Label(side_left, text ="Quantity").grid(column = 1,  row = lot_row, padx = 10, pady = 0)   
    ttk.Label(side_left, text ="Cost/Share").grid(column = 2,  row = lot_row, padx = 10, pady = 0)   
    ttk.Label(side_left, text ="Market Value").grid(column = 3,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="Cost Basis").grid(column = 4,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="Gain/Loss").grid(column = 5,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="Gain/Loss %").grid(column = 6,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="Holding Period").grid(column = 7,  row = lot_row, padx = 10, pady = 0)   
    
    if each_stock in My_lot_details:

        lot_row += 1
        ttk.Label(side_left, text ="-----------").grid(column = 0,  row = lot_row, padx = 10, pady = 0,sticky="n")
        ttk.Label(side_left, text ="------------").grid(column = 1,  row = lot_row, padx = 10, pady = 0,sticky="n")
        ttk.Label(side_left, text ="---------").grid(column = 2,  row = lot_row, padx = 10, pady = 0)
        ttk.Label(side_left, text ="------------").grid(column = 3,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
        ttk.Label(side_left, text ="---------").grid(column = 4,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
        ttk.Label(side_left, text ="---------").grid(column = 5,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
        ttk.Label(side_left, text ="---------").grid(column = 6,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
        ttk.Label(side_left, text ="---------").grid(column = 7,  row = lot_row, padx = 10, pady = 0)   

    total_lot_sum_quantity = 0
    total_market_value = 0
    total_cost = 0
    total_gain_loss = 0
    if each_stock in My_lot_details:
        for each_lot in My_lot_details[each_stock]["data"]:
            lot_row += 1
            # print("each_lot")
            # print(each_lot)
            # print(type(each_lot))
            open_date = each_lot["Open Date"]
            quantity = each_lot["Quantity"]
            total_lot_sum_quantity += float(quantity)

            cost_share = f'${float(each_lot["Cost/Share"].replace("$", "")):.2f}'
            market_value_float = float(each_lot["Market Value"].replace("$", ""))
            total_market_value += market_value_float 
            market_value = f'${market_value_float:.2f}'

            cost_basis_float = float(each_lot["Cost Basis"].replace("$", ""))
            total_cost += cost_basis_float
            cost_basis = f'${cost_basis_float:.2f}'

            gain_loss_float = float(each_lot["Gain/Loss ($)"].replace("$", ""))
            total_gain_loss += gain_loss_float
            gain_loss = f'{gain_loss_float:.02f}'
            # gain_loss = each_lot["Gain/Loss ($)"]
            gain_loss_percent = each_lot["Gain/Loss (%)"]
            holding_period = each_lot["Holding Period"]


            ttk.Label(side_left, text =open_date).grid(column = 0,  row = lot_row, padx = 10, pady = 0,sticky="n")   
            ttk.Label(side_left, text =quantity).grid(column = 1,  row = lot_row, padx = 10, pady = 0,sticky="e")     
            ttk.Label(side_left, text =cost_share).grid(column = 2,  row = lot_row, padx = 10, pady = 0,sticky="e")   
            ttk.Label(side_left, text =market_value).grid(column = 3,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
            ttk.Label(side_left, text =cost_basis).grid(column = 4,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
            ttk.Label(side_left, text =gain_loss).grid(column = 5,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
            ttk.Label(side_left, text =gain_loss_percent).grid(column = 6,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
            ttk.Label(side_left, text =holding_period).grid(column = 7,  row = lot_row, padx = 10, pady = 0)   
    

    lot_row += 1
    ttk.Label(side_left, text ="----------").grid(column = 0,  row = lot_row, padx = 10, pady = 0,sticky="n")   
    ttk.Label(side_left, text ="------------").grid(column = 1,  row = lot_row, padx = 10, pady = 0)   
    ttk.Label(side_left, text ="---------").grid(column = 2,  row = lot_row, padx = 10, pady = 0)   
    ttk.Label(side_left, text ="------------").grid(column = 3,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="---------").grid(column = 4,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="---------").grid(column = 5,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="---------").grid(column = 6,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="---------").grid(column = 7,  row = lot_row, padx = 10, pady = 0 )   

    lot_row += 1
    ttk.Label(side_left, text ='Lot Sum').grid(column = 0,  row = lot_row, padx = 10, pady = 0,sticky="n")   
    ttk.Label(side_left, text =f'{total_lot_sum_quantity:.0f}').grid(column = 1,  row = lot_row, padx = 10, pady = 0,sticky="e")     
    if total_lot_sum_quantity != 0:
        pershare = total_cost/total_lot_sum_quantity
    else:
        pershare = 0
    ttk.Label(side_left, text =f'{(pershare):.2f}').grid(column = 2,  row = lot_row, padx = 10, pady = 0,sticky="e")   

    ttk.Label(side_left, text =f'{total_market_value:.2f}').grid(column = 3,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text =f'{total_cost:.2f}').grid(column = 4,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text =f'{total_gain_loss:.2f}').grid(column = 5,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    # ttk.Label(side_left, text =gain_loss_percent).grid(column = 6,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    # ttk.Label(side_left, text =holding_period).grid(column = 7,  row = lot_row, padx = 10, pady = 0)   

    lot_row += 1
    ttk.Label(side_left, text ="=========").grid(column = 0,  row = lot_row, padx = 10, pady = 0,sticky="n")   
    ttk.Label(side_left, text ="=========").grid(column = 1,  row = lot_row, padx = 10, pady = 0)   
    ttk.Label(side_left, text ="=========").grid(column = 2,  row = lot_row, padx = 10, pady = 0)   
    ttk.Label(side_left, text ="============").grid(column = 3,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="=========").grid(column = 4,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="=========").grid(column = 5,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="=========").grid(column = 6,  row = lot_row, padx = 10, pady = 0 ,sticky="e")   
    ttk.Label(side_left, text ="=========").grid(column = 7,  row = lot_row, padx = 10, pady = 0 )   

    lot_row += 1
    ttk.Label(side_left, text ='Positions').grid(column = 0,  row = lot_row, padx = 10, pady = 0,sticky="n")   

    for each_positon in My_position_details["securitiesAccount"]["positions"]:
        if each_positon["instrument"]["assetType"] == "EQUITY":
            if each_positon["instrument"]["symbol"] == each_stock:
                long_quantity = each_positon["longQuantity"]
                ttk.Label(side_left, text =f"{long_quantity:.0f}").grid(column = 1,  row = lot_row, padx = 10, pady = 0,sticky="e")   
                if int(long_quantity) == int(total_lot_sum_quantity):
                    ttk.Label(side_left,style="G.TLabel", text ="The Position data matches the sum of lots.").grid(column = 2,  row = lot_row, padx = 10, pady = 0, columnspan=4, sticky="w")
                else:
                    print(long_quantity)
                    print(total_lot_sum_quantity)
                    ttk.Label(side_left,style="R.TLabel", text ="Counts do not match! Ingest this stock lot again!").grid(column = 2,  row = lot_row, padx = 10, pady = 0, columnspan=4, sticky="w")

    date_row = 0
    ttk.Label(side_right, text = "").grid(column = 0,  row = date_row, padx = 10, pady = 0,sticky="n")   
    date_row += 1
    ttk.Label(side_right, text = "").grid(column = 0,  row = date_row, padx = 10, pady = 0,sticky="n")   
    date_row += 1
    ttk.Label(side_right, text = "").grid(column = 0,  row = date_row, padx = 10, pady = 0,sticky="n")   

    ttk.Label(side_right, text = "Expiration").grid(column = 0,  row = date_row, padx = 10, pady = 0,sticky="n")   
    ttk.Label(side_right, text = "Calls").grid(column = 1,  row = date_row, padx = 10, pady = 0,sticky="w")
    ttk.Label(side_right, text = "Puts").grid(column = 2,  row = date_row, padx = 10, pady = 0,sticky="w")
    ttk.Label(side_right, text = "Days").grid(column = 3,  row = date_row, padx = 10, pady = 0,sticky="w")
    
    date_row += 1
    ttk.Label(side_right, text = "----------").grid(column = 0,  row = date_row, padx = 10, pady = 0,sticky="n")   
    ttk.Label(side_right, text = "-----").grid(column = 1,  row = date_row, padx = 10, pady = 0,sticky="w")
    ttk.Label(side_right, text = "-----").grid(column = 2,  row = date_row, padx = 10, pady = 0,sticky="w")
    ttk.Label(side_right, text = "-----").grid(column = 3,  row = date_row, padx = 10, pady = 0,sticky="w")
    
    for each_date in My_stock_option_dates[each_stock]:
        date_row += 1
        print("each_date")
        print(each_date)
        ttk.Label(side_right, text = each_date).grid(column = 0,  row = date_row, padx = 10, pady = 0,sticky="n")   
        
        total_calls = 0
        for each_position in My_position_details["securitiesAccount"]["positions"]:
            if each_position["instrument"]["assetType"] == "OPTION":
                if each_position["instrument"]["underlyingSymbol"] == each_stock:
                    year = f'20{each_position["instrument"]["symbol"][6:8]}'
                    month = f'{each_position["instrument"]["symbol"][8:10]}'
                    day = f'{each_position["instrument"]["symbol"][10:12]}'
                    special_date = f'{year}-{month}-{day}'
                    if special_date == each_date:
                        if each_position["instrument"]["putCall"] == "CALL":
                            total_calls += each_position["shortQuantity"]
                            total_calls += each_position["longQuantity"]
        if total_calls != 0:
            ttk.Label(side_right, text = f'{total_calls:.0f}').grid(column = 1,  row = date_row, padx = 10, pady = 0,sticky="w")
        else:
            ttk.Label(side_right, text = f'{total_calls:.0f}',foreground="gray").grid(column = 1,  row = date_row, padx = 10, pady = 0,sticky="w")

        
        total_puts = 0
        for each_position in My_position_details["securitiesAccount"]["positions"]:
            if each_position["instrument"]["assetType"] == "OPTION":
                if each_position["instrument"]["underlyingSymbol"] == each_stock:
                    year = f'20{each_position["instrument"]["symbol"][6:8]}'
                    month = f'{each_position["instrument"]["symbol"][8:10]}'
                    day = f'{each_position["instrument"]["symbol"][10:12]}'
                    special_date = f'{year}-{month}-{day}'
                    if special_date == each_date:
                        if each_position["instrument"]["putCall"] == "PUT":
                            total_puts += each_position["shortQuantity"]
                            total_puts += each_position["longQuantity"]
        if total_puts != 0:
            ttk.Label(side_right, text = f'{total_puts:.0f}').grid(column = 2,  row = date_row, padx = 10, pady = 0,sticky="w")
        else:
            ttk.Label(side_right, text = f'{total_puts:.0f}',foreground="gray").grid(column = 2,  row = date_row, padx = 10, pady = 0,sticky="w")

        now = datetime.datetime.now()
        date1 = datetime.date(now.year,now.month,now.day)
        date2 = datetime.date.fromisoformat(each_date)
        differece = date2-date1

        ttk.Label(side_right, text = str(differece.days),foreground="gray" ).grid(column = 3,  row = date_row, padx = 10, pady = 0,sticky="w")
        print("days_until")
        print(differece)
        



tabControl.pack(expand=1, fill="both")



window.mainloop()




# My_orders_details = client.account_orders(account_hash,datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1), datetime.datetime.now(datetime.timezone.utc) ).json()
# My_orders_details_json_string = json.dumps(My_orders_details)


# print("Setting My_orders_details")
# result = r.set('My_orders_details',My_orders_details_json_string)
# with open(".My_orders_details.json", "w") as file:
#     json.dump(My_orders_details, file, indent=4)
# Size = sys.getsizeof(My_orders_details)
# print("Size My_orders_details")
# print(Size)
# print()
