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
x_geometry = 800
y_geometry = 720-16
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
# print(5)
# My_stock_option_strikes = return_details("My_stock_option_strikes")

# All_stock_option_dates = all_dates(My_stock_option_dates)
all_dates(My_stock_option_dates)
My_dates = list(all_dates(My_stock_option_dates))
My_dates.sort()

print()
print("My_dates")
print(My_dates)
print(len(My_dates))
print()


# My_stocks = return_positions("all")

My_owned_stocks = return_positions("stock")
# My_involved_options = return_positions("option")

# My_open_orders = return_orders("open")
# My_filled_orders = return_orders("filled")
My_involved_all = list(return_positions("all"))
My_involved_all.sort()


print()
print("My_involved_all")
print(My_involved_all)
print(len(My_involved_all))
print()

tabControl = ttk.Notebook(window)
tab = {}
special = "Stocks"
tab[special] = ttk.Frame(tabControl)
tabControl.add(tab[special], text=special)
# ttk.Label(tab["Stocks"], text ="This should contain a table of my owned stocks").grid(column = 0,  row = 0, padx = 30, pady = 30)   
stock_row = 0
ttk.Label(tab[special], text ="Symbol").grid(column = 0,  row = 0, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Quantity").grid(column = 1,  row = 0, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Price").grid(column = 2,  row = 0, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Day Change").grid(column = 3,  row = 0, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Day Percent Change").grid(column = 4,  row = 0, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Market Value").grid(column = 5,  row = 0, padx = 10, pady = 10)   
ttk.Label(tab[special], text ="Profit/Loss").grid(column = 6,  row = 0, padx = 10, pady = 10)   

for each in My_position_details["securitiesAccount"]["positions"]:
    if each["instrument"]["assetType"] == "EQUITY":
        stock_row = stock_row + 1
        # print(each)
        ttk.Label(tab[special], text = each["instrument"]["symbol"]).grid(column = 0,  row = stock_row, padx = 10, pady = 10)   
        ttk.Label(tab[special], text = each["longQuantity"]).grid(column = 1,  row = stock_row, padx = 10, pady = 10)   
        # ttk.Label(tab[special], text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 10)   
        ttk.Label(tab[special], text = each["instrument"]["netChange"]).grid(column = 3,  row = stock_row, padx = 10, pady = 10)   
        ttk.Label(tab[special], text = each["currentDayProfitLossPercentage"]).grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
        ttk.Label(tab[special], text = each["marketValue"]).grid(column = 5,  row = stock_row, padx = 10, pady = 10)   
        ttk.Label(tab[special], text = each["longOpenProfitLoss"]).grid(column = 6,  row = stock_row, padx = 10, pady = 10)   




special = "Options"
tab[special] = ttk.Frame(tabControl)
tabControl.add(tab[special], text=special)
side_left = ttk.Frame(tab[special], width = tab[special].winfo_width()/2)
side_left.pack(side=tk.LEFT, fill=tk.Y)
side_right = ttk.Frame(tab[special], width = tab[special].winfo_width()/2)
side_right.pack(side=tk.RIGHT, fill=tk.Y)
# option_label = []

date_row = 0
label = ttk.Label(side_right,text="Expiration Date")
label.grid(column = 0, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="Calls")
label.grid(column = 1, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="Puts")
label.grid(column = 2, row = date_row, pady=5,padx=10)
label = ttk.Label(side_right,text="Days")
label.grid(column = 3, row = date_row, pady=5,padx=10)

for each in My_dates:
    date_row = date_row + 1
    label = ttk.Label(side_right,text=str(each))
    label.grid(column = 0, row = date_row, pady=1,padx=10)
    label = ttk.Label(side_right,text="0", foreground="gray")
    label.grid(column = 1, row = date_row, pady=1,padx=10)
    label = ttk.Label(side_right,text="0", foreground="gray")
    label.grid(column = 2, row = date_row, pady=1,padx=10)
    print(each)
    now = datetime.datetime.now()
    date1 = datetime.date(now.year,now.month,now.day)
    date2 = datetime.date.fromisoformat(each)
    differece = date2-date1

    print(date1,date2,differece.days)
    label = ttk.Label(side_right,text=str(differece.days), foreground="gray")
    label.grid(column = 3, row = date_row, pady=1,padx=10)

    # option_label.append(label)
# ttk.Label(tab["Options"], text ="This should contain a table of my options expiring over time").grid(column = 0, row = 0, padx = 30, pady = 30) 

special = "Open"
tab[special] = ttk.Frame(tabControl)
tabControl.add(tab[special], text=special)
ttk.Label(tab["Open"], text ="This should contain a list of open orders").grid(column = 0, row = 0, padx = 30, pady = 30) 




# for each in range(len(My_involved_all)):
# for each in My_involved_all:
#     tab[each] = ttk.Frame(tabControl)
#     tabControl.add(tab[each], text=each)

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
