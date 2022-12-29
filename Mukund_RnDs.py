from tkinter import *
import threading
import time
from datetime import datetime
#from datetime import date
import yfinance as yf
import talib as ta
import csv
#import pandas as pd

#indexsymbol = "^DJI"
#indexsymbol = "^NSEBANK"
stocksSymbol = 'TCS.NS'


def on_closing():
    root.destroy()

def getDataYF():
    print('stock_list:', stocksSymbol)
   # data = yf.download(stocksSymbolList, start="2022-12-20", end="2022-12-23", interval = "1D")
    data = yf.download(tickers=stocksSymbol, period = '2D', interval = '5m', progress = False, rounding = True)
    #set(data.columns.get_level_values(0))

    #save Dataframe into CSV file
    data.to_csv(path_or_buf='Data1.csv' )






# create root window
root = Tk()

# root window title and dimension
root.title("Mukund RnD")

# creating a lock
#lock = threading.Lock()

# Set geometry (widthxheight)
root.geometry('500x350')

lbl_Index = Label(root, text="Index")
lbl_Index.place(x=25, y=10, width=50, height=25)

lbl_Index1_Spot = Label(root, text="", borderwidth=1, relief="solid")
lbl_Index1_Spot.place(x=80, y=10, width=100, height=25)

lbl_Index2_Spot = Label(root, text="", borderwidth=1, relief="solid")
lbl_Index2_Spot.place(x=200, y=10, width=100, height=25)

# lbl_Bnifty_spot = Label(root, text="")
lbl_NOption = Label(root, text="Symbol")
lbl_NOption.place(x=10, y=50, width=100, height=25)
txt_NOption = Entry(root)
txt_NOption.place(x=120, y=50, width=100, height=25)

symbol = stocksSymbol  # "NIFTY22JUN15800"
txt_NOption.insert(0, symbol)

lbl_Time = Label(root, text="", borderwidth=1, relief="solid")
lbl_Time.place(x=395, y=10, width=100, height=25)

lbl_LTP = Label(root, text="LTP")
lbl_LTP.place(x=10, y=100, width=100, height=25)

txt_LTP = Entry(root)
txt_LTP.place(x=120, y=100, width=100, height=25)

lbl_RSI = Label(root, text="RSI")
lbl_RSI.place(x=10, y=150, width=100, height=25)

txt_RSI60 = Entry(root)
txt_RSI60.place(x=40, y=190, width=50, height=25)

txt_RSI15 = Entry(root)
txt_RSI15.place(x=150, y=190, width=50, height=25)

txt_RSI5 = Entry(root)
txt_RSI5.place(x=40, y=230, width=50, height=25)

txt_RSI1 = Entry(root)
txt_RSI1.place(x=150, y=230, width=50, height=25)

lbl_RSI_Msg = Label(root, text="", borderwidth=1, relief="solid")
lbl_RSI_Msg.place(x=10, y=265, width=200, height=25)


# startthreading()
getDataYF()
# all widgets will be here
# Execute Tkinter
root.protocol("WM_DELETE_WINDOW", on_closing)
#root.mainloop()
