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
ttk.Label(side_left, text ="Symbol").grid(column = 0,  row = stock_row, padx = 10, pady = 10,sticky="n")   
ttk.Label(side_left, text ="Quantity").grid(column = 1,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="net Change").grid(column = 3,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
# ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="Market Value").grid(column = 5,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
ttk.Label(side_left, text ="Profit/Loss").grid(column = 6,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   


total_market_value = 0.0
total_profit_loss = 0.0
for each in My_position_details["securitiesAccount"]["positions"]:
    if each["instrument"]["assetType"] == "EQUITY":
        stock_row += 1
        # print(each)
        ttk.Label(side_left, text = each["instrument"]["symbol"] ).grid(column = 0,  row = stock_row, padx = 10, pady = 10)   
        ttk.Label(side_left, text = f'{each["longQuantity"]:.0f}' ).grid(column = 1,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
        # ttk.Label(side_left, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 10)
        # ttk.Label(side_left, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 10, pady = 10)
        ttk.Label(side_left, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 10, pady = 10 ,sticky="e")
        # ttk.Label(side_left, text = each["currentDayProfitLossPercentage"]).grid(column = 4,  row = stock_row, padx = 10, pady = 10)

        market_value = each["marketValue"]
        total_market_value += market_value
        ttk.Label(side_left, text = f'{market_value:.2f}').grid(column = 5,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   

        profit_loss = each["longOpenProfitLoss"]
        total_profit_loss += profit_loss
        ttk.Label(side_left, text = f'{profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   

stock_row += 1
ttk.Label(side_left, text ="-----").grid(column = 0,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="-----").grid(column = 1,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="-----").grid(column = 2,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="-------").grid(column = 3,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
# ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text ="----------").grid(column = 5,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
ttk.Label(side_left, text ="----------").grid(column = 6,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   

stock_row += 1
# ttk.Label(side_left, text ="").grid(column = 0,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="").grid(column = 1,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="").grid(column = 2,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="net Change").grid(column = 3,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
# ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
ttk.Label(side_left, text =f'{total_market_value}').grid(column = 5,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
ttk.Label(side_left, text =f'{total_profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 10, sticky="e")


########################################################################
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
label.grid(column = 0, row = date_row, pady=5,padx=10,sticky='E')
label = ttk.Label(side_right,text="Calls")
label.grid(column = 1, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="Puts")
label.grid(column = 2, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="Days")
label.grid(column = 3, row = date_row, pady=5,padx=10)

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
    label.grid(column = 0, row = date_row, pady=1,padx=10)
    
    if each in total_calls:
        label = ttk.Label(side_right,text=f'{total_calls[each]:.0f}')
        label.grid(column = 1, row = date_row, pady=1,padx=10)
    else:
        label = ttk.Label(side_right,text="0", foreground="gray")
        label.grid(column = 1, row = date_row, pady=1,padx=10)

    if each in total_puts:
        label = ttk.Label(side_right,text=f'{total_puts[each]:.0f}')
        label.grid(column = 2, row = date_row, pady=1,padx=10)
    else:
        label = ttk.Label(side_right,text="0", foreground="gray")
        label.grid(column = 2, row = date_row, pady=1,padx=10)
    # print(each)
    now = datetime.datetime.now()
    date1 = datetime.date(now.year,now.month,now.day)
    date2 = datetime.date.fromisoformat(each)
    differece = date2-date1
    # print(date1,date2,differece.days)
    label = ttk.Label(side_right,text=str(differece.days), foreground="gray")
    label.grid(column = 3, row = date_row, pady=1,padx=10)

    # option_label.append(label)
# ttk.Label(tab["Options"], text ="This should contain a table of my options expiring over time").grid(column = 0, row = 0, padx = 30, pady = 30) 

date_row += 1
label = ttk.Label(side_right,text="-------------")
label.grid(column = 0, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="----")
label.grid(column = 1, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="----")
label.grid(column = 2, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="----")
label.grid(column = 3, row = date_row, pady=5,padx=10)

date_row += 1
number_calls = 0
for each in total_calls:
    number_calls += total_calls[each]
label = ttk.Label(side_right,text=f'{number_calls:.0f}')
label.grid(column = 1, row = date_row, pady=5,padx=10)

number_puts = 0
for each in total_puts:
    number_puts += total_puts[each]
label = ttk.Label(side_right,text=f'{number_puts:.0f}')
label.grid(column = 2, row = date_row, pady=5,padx=10)



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
for each in My_involved_all:
    tab[each] = ttk.Frame(tabControl)
    tabControl.add(tab[each], text=each)

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
