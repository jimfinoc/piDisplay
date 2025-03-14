import tkinter as tk
from tkinter import ttk

class notebook_with_tab():
    def __init__(self, window):
        self.notebook = ttk.Notebook(window)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.tab = {}
        self.canvas = {}
        self.scrollbar = {}
        self.scrollable_frame = {}
        self.fields_header = {}
        self.fields_stock = {}


    def add_tab(self, tab_name):
        self.tab[tab_name] = tk.Frame(self.notebook)
        self.notebook.add(self.tab[tab_name], text=tab_name)

        self.canvas[tab_name] = tk.Canvas(self.tab[tab_name])

        self.scrollbar[tab_name] = tk.Scrollbar(self.tab[tab_name], orient="vertical", command=self.canvas[tab_name].yview)
        self.scrollable_frame[tab_name] = tk.Frame(self.canvas[tab_name])

        self.scrollable_frame[tab_name].bind("<Configure>",lambda e: self.canvas[tab_name].configure(scrollregion=self.canvas[tab_name].bbox("all")))
        
        self.canvas[tab_name].create_window((0, 0), window=self.scrollable_frame[tab_name], anchor="nw")
        self.canvas[tab_name].configure(yscrollcommand=self.scrollbar[tab_name].set)
        self.canvas[tab_name].pack(side="left", fill="both", expand=True)
        self.scrollbar[tab_name] .pack(side="right", fill="y")
        # for i in range(50):
            # tk.Label(self.scrollable_frame[tab_name], text=f"Label {i}").pack()
        
    def create_overview_labels(self,tab_name, headers,My_position_details):
        self.Overview = tk.Canvas(self.scrollable_frame[tab_name])
        self.Overview.pack()

        stock_row = 0
        for each in headers:
            ttk.Label(self.Overview, text = each).grid(column = headers.index(each),  row = stock_row, padx = 10, pady = 0)

        stock_row += 1
        for each in headers:
            replaced_string = "-" * len(each)
            ttk.Label(self.Overview, text = replaced_string).grid(column = headers.index(each),  row = stock_row, padx = 10, pady = 0)

        total_market_value = 0.0
        total_profit_loss = 0.0
        stock_row = 1
        for each in My_position_details["securitiesAccount"]["positions"]:
            if each["instrument"]["assetType"] == "EQUITY":
                stock_row += 1
                ttk.Label(self.Overview, text = each["instrument"]["symbol"] ).grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
                ttk.Label(self.Overview, text = f'{each["longQuantity"]:.0f}' ).grid(column = 1,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
                # ttk.Label(self.Overview, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 10)
                # ttk.Label(self.Overview, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 10, pady = 10)
                ttk.Label(self.Overview, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 0, pady = 0 ,sticky="e")
                # ttk.Label(self.Overview, text = each["currentDayProfitLossPercentage"]).grid(column = 4,  row = stock_row, padx = 10, pady = 10)

                market_value = each["marketValue"]
                total_market_value += market_value
                ttk.Label(self.Overview, text = f'{market_value:.2f}').grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

                profit_loss = each["longOpenProfitLoss"]
                total_profit_loss += profit_loss
                ttk.Label(self.Overview, text = f'{profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   



    def update_overview_labels(self,tab_name, My_position_details):        
        total_market_value = 0.0
        total_profit_loss = 0.0
        stock_row = 1
        for each in My_position_details["securitiesAccount"]["positions"]:
            if each["instrument"]["assetType"] == "EQUITY":
                stock_row += 1
                # print(each)
                ttk.Label(self.Overview, text = each["instrument"]["symbol"] ).grid(column = 0,  row = stock_row, padx = 10, pady = 0)   
                ttk.Label(self.Overview, text = f'{each["longQuantity"]:.0f}' ).grid(column = 1,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   
                # ttk.Label(self.Overview, text ="Price").grid(column = 2,  row = stock_row, padx = 10, pady = 10)
                # ttk.Label(self.Overview, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 10, pady = 10)
                ttk.Label(self.Overview, text = f'{each["instrument"]["netChange"]:.2f}').grid(column = 3,  row = stock_row, padx = 0, pady = 0 ,sticky="e")
                # ttk.Label(self.Overview, text = each["currentDayProfitLossPercentage"]).grid(column = 4,  row = stock_row, padx = 10, pady = 10)

                market_value = each["marketValue"]
                total_market_value += market_value
                ttk.Label(self.Overview, text = f'{market_value:.2f}').grid(column = 5,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

                profit_loss = each["longOpenProfitLoss"]
                total_profit_loss += profit_loss
                ttk.Label(self.Overview, text = f'{profit_loss:.2f}').grid(column = 6,  row = stock_row, padx = 10, pady = 0 ,sticky="e")   

