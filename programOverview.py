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
My_stock_option_dates = return_details("My_stock_option_dates")
My_involved_all = list(return_positions("all"))
My_involved_all.sort()
My_sorted_option_dates = list(all_dates(My_stock_option_dates))
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

special = "Stocks and Options"
myNotebook.add_tab(special)

headers = [
    "Symbol",
    "Quantity",
    "Price",
    "net Change",
    "Day Percent Change",
    "Market Value",
    "Profit/Loss"
]

myNotebook.create_overview_labels(special, headers,My_position_details)
# myNotebook.update_overview_labels(special, My_position_details)


# ttk.Label(side_left, text ="Symbol").grid(column = 0,  row = stock_row, padx = 10, pady = 0,sticky="n")   
# ttk.Label(side_left, text ="Quantity").grid(column = 1,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="net Change").grid(column = 3,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# # ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="Market Value").grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# ttk.Label(side_left, text ="Profit/Loss").grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

# stock_row += 1
# ttk.Label(side_left, text ="-----").grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="-----").grid(column = 1,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="-----").grid(column = 2,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="-------").grid(column = 3,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# # ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="----------").grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# ttk.Label(side_left, text ="----------").grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

# total_market_value = 0.0
# total_profit_loss = 0.0
# for each in My_position_details["securitiesAccount"]["positions"]:
#     if each["instrument"]["assetType"] == "EQUITY":
#         stock_row += 1
#         # print(each)
#         ttk.Label(side_left, text = each["instrument"]["symbol"] ).grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
#         ttk.Label(side_left, text = f'{each["longQuantity"]:.0f}' ).grid(column = 1,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
#         # ttk.Label(side_left, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 10)
#         # ttk.Label(side_left, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 10, pady = 10)
#         ttk.Label(side_left, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 0, pady = 0 ,sticky="e")
#         # ttk.Label(side_left, text = each["currentDayProfitLossPercentage"]).grid(column = 4,  row = stock_row, padx = 10, pady = 10)

#         market_value = each["marketValue"]
#         total_market_value += market_value
#         ttk.Label(side_left, text = f'{market_value:.2f}').grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

#         profit_loss = each["longOpenProfitLoss"]
#         total_profit_loss += profit_loss
#         ttk.Label(side_left, text = f'{profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

# stock_row += 1
# ttk.Label(side_left, text ="-----").grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="-----").grid(column = 1,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="-----").grid(column = 2,  row = stock_row, padx = 10, pady = 0)   
# ttk.Label(side_left, text ="-------").grid(column = 3,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# # ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text ="----------").grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# ttk.Label(side_left, text ="----------").grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

# stock_row += 1
# # ttk.Label(side_left, text ="").grid(column = 0,  row = stock_row, padx = 10, pady = 10)   
# # ttk.Label(side_left, text ="").grid(column = 1,  row = stock_row, padx = 10, pady = 10)   
# # ttk.Label(side_left, text ="").grid(column = 2,  row = stock_row, padx = 10, pady = 10)   
# # ttk.Label(side_left, text ="net Change").grid(column = 3,  row = stock_row, padx = 10, pady = 10 ,sticky="e")   
# # ttk.Label(side_left, text ="Day Percent Change").grid(column = 4,  row = stock_row, padx = 10, pady = 10)   
# ttk.Label(side_left, text =f'{total_market_value}').grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
# ttk.Label(side_left, text =f'{total_profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 0, sticky="e")





window.mainloop()