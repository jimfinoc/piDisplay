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
y_geometry = 720
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



# My_order_details = return_details("My_orders_details")
# My_position_details = return_details("My_position_details")
# My_stocks = return_details("My_stocks")
# My_stocks = return_positions("all")

# My_involved_stocks = return_positions("stock")
# My_involved_options = return_positions("option")
My_involved_all = list(return_positions("all"))
My_involved_all.sort()

# My_open_orders = return_orders("open")
# My_filled_orders = return_orders("filled")

print()
# print(My_order_details)
print(My_involved_all)
# print(len(My_involved_all))
print()

tabControl = ttk.Notebook(window)
tab = {}
special = "Stocks"
tab[special] = ttk.Frame(tabControl)
tabControl.add(tab[special], text=special)

special = "Options"
tab[special] = ttk.Frame(tabControl)
tabControl.add(tab[special], text=special)

special = "Open"
tab[special] = ttk.Frame(tabControl)
tabControl.add(tab[special], text=special)

# for each in range(len(My_involved_all)):
for each in My_involved_all:
    tab[each] = ttk.Frame(tabControl)
    tabControl.add(tab[each], text=each)

tabControl.pack(expand=1, fill="both")

ttk.Label(tab["Stocks"], text ="This should contain a table of my owned stocks").grid(column = 0,  row = 0, padx = 30, pady = 30)   
ttk.Label(tab["Options"], text ="This should contain a table of my options expiring over time").grid(column = 0, row = 0, padx = 30, pady = 30) 
ttk.Label(tab["Open"], text ="This should contain a list of open orders").grid(column = 0, row = 0, padx = 30, pady = 30) 


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
