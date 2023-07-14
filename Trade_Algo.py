import os
import sys
from tkinter import *
import threading
import time
from datetime import datetime
#from datetime import date
import yfinance as yf
import talib as ta

#indexsymbol = "^DJI"
#indexsymbol = "^NSEBANK"
indexsymbol = "^NSEI"
stop_LTP_threads = False
currentRSI = 0.0
currentRSI60 = 0.0
currentRSI15 = 0.0
currentRSI5 = 0.0

noOfTrade = 0

def startRSICalculation():
    print("ToDo: RSI Calculation")
    return

def roundtick(x) -> float:
    global ticksize
    ticksize = 0.05
    fprice = 0.0
    fprice = (round(x / ticksize)) * ticksize

    fprice = round(fprice, 2)

    return fprice

def on_closing():
    global stop_LTP_threads
    global root
    global t1
    global exit_event

    stop_LTP_threads = True
    root.destroy()


def CheckPivotSetup(secondPreviousCandle_open, secondPreviousCandle_close,
                    previousCandle_open, previousCandle_close, currentCandle_open,
                    currentCandle_close, priceTF):

    global noOfTrade
    entryPrice = 0.0

    next1MinCandle_open = priceTF.iloc[-1]['Open']

    if (#secondPreviousCandle_open > secondPreviousCandle_close and  # SecondToPrevious candle is RED
            previousCandle_open < previousCandle_close and  # Previous candle is GREEN
            currentCandle_close <= next1MinCandle_open):  # Current candle opened above 5 mins close

    # if (secondPreviousCandle_open > secondPreviousCandle_close and  #  SecondToPrevious candle is RED
    #         previousCandle_open > previousCandle_close and # Previous candle is RED
    #         currentCandle_open < currentCandle_close ): #  Current candle is GREEN
    #
    #     #next1MinCandleNo = current5MinCandleNo * 5 + 1
    #     next1MinCandle_open = priceTF.iloc[-1]['Open']

        if ( next1MinCandle_open > currentCandle_close  ): # Next 1 min open is above Current 5 min
            entryPrice = next1MinCandle_open  #Buy
            strmsg = "Trade no." + str(noOfTrade) + " of " + symbol + "BUY at " + str(entryPrice) + " at 5min Candle No (open)"
            #print("Trade no.", noOfTrade, " of ", symbol, "BUY at ", entryPrice, " at 5min Candle No (open)")
            printTrace(strmsg)

            return True, entryPrice

    return False, entryPrice

def CheckPivot_Target_SL(stopLoss, current1MinCandle_close, target, entryPrice):

    if current1MinCandle_close > target:
        #print("TARGET ACHIEVED: Trade no=", noOfTrade, " of symbol = ", symbol, " sell = ", current1MinCandle_close)
        strMsg = "TARGET ACHIEVED: Trade no="+ str(noOfTrade) + " of symbol = " + symbol + " sell = " + str(current1MinCandle_close)
        printTrace(strMsg)
        profit = 500 * (current1MinCandle_close - entryPrice)
        printTrace(" Profit = ", profit)
        print(" ")
        return True

    if current1MinCandle_close < stopLoss:
        strmsg = "STOP LOSS HIT: Trade no="+ str(noOfTrade) + " of symbol = " + symbol + " sell = " + str(current1MinCandle_close)
        #print("STOP LOSS HIT: Trade no=", noOfTrade, " of symbol = ", symbol, " sell = ", current1MinCandle_close)
        printTrace(strmsg)
        loss = 500 * (current1MinCandle_close - entryPrice)
        printTrace(" Loss = ", loss)
        print(" ")
        return True

    return False

def printTrace(message, var1=None):

    try:
        timestamp = datetime.now().strftime("%m-%d-%Y::%H:%M:%S")
        strMsg = timestamp + "=>" + str(message)

        if var1 is not None:
            strMsg +=  str(var1)

        print(strMsg)

    except Exception as e:
        print("Exceptin in PrintTrace: {}".format(str(e)))

def getLTP():
    global txt_LTP
    global symbol
    global txt_NOption
    global lbl_Time
    global lbl_Index1_Spot
    global txt_RSI60
    global txt_RSI15
    global txt_RSI5
    global txt_RSI1

    global currentRSI
    global currentRSI60
    global currentRSI15
    global currentRSI5

    global fTarget
    global fSL
    global lbl_RSI_Msg

    rsi_5Min_below40 = False
    rsi_5Min_crossed40 = False
    OrderPlace = False
    entry = 0.0
    target = 0.0
    stoploss = 0.0

    global stop_LTP_threads

    ltp = 0.0
    entryprice = 0.0

    secondPreviousCandle_close = 0.0
    previousCandle_close = 0.0
    currentCandle_close = 0.0

    secondPreviousCandle_low = 0.0

    secondPreviousCandle_open = 0.0
    previousCandle_open = 0.0
    currentCandle_open = 0.0

    while (1):
        try:
            ltpsymbol = txt_NOption.get()

            try:
                price1Min = yf.download(tickers=indexsymbol, period='2d', interval='1m', progress=False, rounding=True)
                #print(price1Min.iloc[-1]['Close'])
                ltp = roundtick(price1Min.iloc[-1]['Close'])
                #print(type(price1Min['Close']))
                #print(price1Min['Close'])
                rsi1all = ta.RSI(price1Min['Close'])
                currentRSI_l = roundtick(rsi1all.iloc[-1])

                #print(currentRSI)

                txt_LTP.delete(0, END)
                txt_LTP.insert(0, str(ltp))

                if OrderPlace == False:
                    st = time.time()

                    price1Hr = yf.download(tickers=indexsymbol, period='5d', interval='1h', progress=False, rounding=True)
                    rsi1Hrall = ta.RSI(price1Hr['Close'])
                    currentRSI60_l = roundtick(rsi1Hrall.iloc[-1])

                    price15min = yf.download(tickers=indexsymbol, period='2d', interval='15m', progress=False, rounding=True)
                    rsi15Minall = ta.RSI(price15min['Close'])
                    currentRSI15_l = roundtick(rsi15Minall.iloc[-1])

                    price5Min = yf.download(tickers=indexsymbol, period='2d', interval='5m', progress=False, rounding=True)
                    rsi5Minall = ta.RSI(price5Min['Close'])
                    currentRSI5_l = roundtick(rsi5Minall.iloc[-1])

                    et = time.time()

                    elapsed_time = et - st
                    #print('Execution time price1Hr:', (elapsed_time * 1000), 'miliseconds')
                    strmsg = 'Execution time price1Hr:'+ str((elapsed_time * 1000)) + 'miliseconds'

                    #printTrace(strmsg)

                    txt_RSI60.delete(0, END)
                    txt_RSI60.insert(0, str(currentRSI60_l))
                    txt_RSI15.delete(0, END)
                    txt_RSI15.insert(0, str(currentRSI15_l))
                    txt_RSI5.delete(0, END)
                    txt_RSI5.insert(0, str(currentRSI5_l))
                    txt_RSI1.delete(0, END)
                    txt_RSI1.insert(0, str(currentRSI_l))

                    secondPreviousCandle_close = price5Min.iloc[-3]['Close']
                    previousCandle_close = price5Min.iloc[-2]['Close']
                    currentCandle_close = price5Min.iloc[-1]['Close']

                    secondPreviousCandle_low = price5Min.iloc[-2]['Low']

                    secondPreviousCandle_open = price5Min.iloc[-3]['Open']
                    previousCandle_open = price5Min.iloc[-2]['Open']
                    currentCandle_open = price5Min.iloc[-1]['Open']

                    # if Check40BounceSetup(currentRSI5_l, price5Min) == True:
                    #     OrderPlace = True

                    OrderPlace, entryprice = CheckPivotSetup(secondPreviousCandle_open, secondPreviousCandle_close,
                    previousCandle_open, previousCandle_close, currentCandle_open,
                    currentCandle_close, price1Min)

                    if OrderPlace:
                        target = entryprice * 1.00015
                        stopLoss = secondPreviousCandle_low

                        target = roundtick(target)
                        stopLoss = roundtick(stopLoss)

                        strMsg = "EntryPrice = " + str(entryprice) + "TARGET = " + str(target) + "STOP LOSS = " + str(stopLoss)
                        #print("EntryPrice = ", entryprice, "TARGET = ", target, "STOP LOSS = ", stopLoss)
                        printTrace(strMsg)

                    lock.acquire()
                    currentRSI60 = currentRSI60_l
                    currentRSI15 = currentRSI15_l
                    currentRSI5 = currentRSI5_l
                    lock.release()
                else:
                    # check for Target or SL for 40 Bounce Setup
                    #Check40Bounce_Target_SL(price5Min)

                    #Check for Target or SL for Pivot setup
                    #ToDo Validate input variables
                    if CheckPivot_Target_SL(stopLoss, ltp, target, entryprice) == True:
                        OrderPlace = False

                lock.acquire()
                currentRSI = currentRSI_l
                lock.release()

            except Exception as e:
                txt_LTP.delete(0, END)
                print('7 Exception Occurred in LTP order = ', e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)

        except Exception as e:
            txt_LTP.delete(0, END)
            print('7.1 Exception Occurred in LTP thread = ', e)

        now = datetime.now()

        # current_time = now.strftime("%H:%M:%S")
        current_time = datetime.today().strftime("%I:%M:%S  %p")
        lbl_Time.config(text=current_time)

        if stop_LTP_threads:
            return

        #ToDo no sleep required for yahoo, may be required for other
        #time.sleep(1)


def Check40Bounce_Target_SL(price5Min):

    global target
    global stoploss

    if price5Min['Close'].iloc[-1] >= target:
        print("Exit order as Target Hit")
        OrderPlace = False
        rsi_5Min_crossed40 = False
        rsi_5Min_below40 = False
        lbl_RSI_Msg.config(text="Target Hit")
        print("Exit @ = ", price5Min['Close'].iloc[-1], "Exit @ : ", price5Min.index[-1])
        entry = 0.0
        target = 0.0
        stoploss = 0.0

    if price5Min['Close'].iloc[-1] < stoploss:
        print("Exit order as Stoploss Hit")
        OrderPlace = False
        rsi_5Min_crossed40 = False
        rsi_5Min_below40 = False
        lbl_RSI_Msg.config(text="Stoploss hit")
        print("Stoploss Exit @ = ", price5Min['Close'].iloc[-1], "Exit @ : ", price5Min.index[-1])
        entry = 0.0
        target = 0.0
        stoploss = 0.0

def Check40BounceSetup(currentRSI5_l, price5Min):

    global rsi_5Min_crossed40
    global rsi_5Min_below40
    global lbl_RSI_Msg

    if rsi_5Min_crossed40 == False:
        if currentRSI5_l < 40:
            rsi_5Min_below40 = True
            lbl_RSI_Msg.config(text="5 Min RSI is below 40")
            return False

        if rsi_5Min_below40:
            if currentRSI5_l > 40:
                rsi_5Min_crossed40 = True
                lbl_RSI_Msg.config(text="5 Min RSI crossed 40")

    if rsi_5Min_crossed40:
        if price5Min['Open'].iloc[-1] >= price5Min['Close'].iloc[-2]:
            print("Current open is high than last close", "Close = ", price5Min['Close'].iloc[-2], "Open = ",
                  price5Min['Open'].iloc[-1])
            print("Open Candle: ", price5Min.index[-1], "Close Candle: ", price5Min.index[-2])
            entry = price5Min['Open'].iloc[-1]
            target = price5Min['Open'].iloc[-1] + 10
            stoploss = price5Min['Low'].iloc[-2]
            OrderPlace = True
            print("Order @ = ", entry, "Target = ", target, "Stoploss = ", stoploss)
            lbl_RSI_Msg.config(text="Order placed")

            return True

def findSetup():
    global currentRSI
    global currentRSI60
    global currentRSI15
    global currentRSI5
    global lbl_RSI_Msg
    global stop_LTP_threads

    while (1):

        lock.acquire()
        if currentRSI < 42 and currentRSI > 35:
            print("1 Min RSI is @ 40")
            lbl_RSI_Msg.config(text="1 Min RSI is @ 40")

        # currentRSI60
        # currentRSI15
        # currentRSI5
        lock.release()

        time.sleep(2)

        if stop_LTP_threads:
            break
    return

def startthreading():
    global txt_LTP
    global t1
    global t2

    global exit_event
    exit_event = threading.Event()
    # Call work function
    t1 = threading.Thread(target=getLTP)
    t1.daemon = True
    t1.start()

    # t2 = threading.Thread(target=findSetup)
    # t2.daemon = True
    # t2.start()

    # t1.join()
    # t2.join()

# create root window
root = Tk()

# root window title and dimension
root.title("Yahoo RSI Bounce")

# creating a lock
lock = threading.Lock()

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

symbol = indexsymbol  # "NIFTY22JUN15800"
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

mtm = 0.0
startthreading()

# all widgets will be here
# Execute Tkinter
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()