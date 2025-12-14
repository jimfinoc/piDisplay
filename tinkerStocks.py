import tkinter as tk
from tkinter import ttk

import datetime
import math
import json
from urllib.request import urlopen 
import redis
from dotenv import load_dotenv
import os

from stockDataFunctions import return_details
from stockDataFunctions import return_orders
from stockDataFunctions import return_positions
from stockDataFunctions import all_dates
from stockDataFunctions import total_calls_and_puts

from ttkTabs import notebook_with_tab

x_geometry = 1280
y_geometry = 720-16
afterTime = 5 * 60 * 1000 # time is in milliseconds, this waits 5 minutes

My_position_details = return_details("My_position_details")
My_orders_details = return_details("My_orders_details")

My_stocks = return_details("My_stocks")
My_owned_stocks = return_positions("stock")
My_open_orders = return_orders("open")
My_involved_all = list(return_positions("all"))
My_involved_all.sort()
All_stock_option_dates = return_details("All_stock_option_dates")
My_involved_all = list(return_positions("all"))
My_involved_all.sort()
My_sorted_option_dates = list(all_dates(All_stock_option_dates))
My_sorted_option_dates.sort()

total_calls = {}
total_puts = {}

total_calls, total_puts = total_calls_and_puts(My_position_details)
    # "My_calls_and_puts")
# options_by_date(total_calls,"calls")
# options_by_date(total_puts,"puts")


window = tk.Tk()
window.geometry(f"{x_geometry}x{y_geometry}+0+0")
window.title("Stock Scrolling Details")

myNotebook = notebook_with_tab(window)

# special = "Stocks and Options"
# myNotebook.add_tab(special)
# special = "Open"
# myNotebook.add_tab(special)
for each_stock in My_involved_all:
    myNotebook.add_tab(each_stock)





window.mainloop()