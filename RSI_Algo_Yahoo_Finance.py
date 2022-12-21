from tkinter import *
import threading
import time
from datetime import datetime
from datetime import date
import yfinance as yf
import talib as ta

#indexsymbol = "^DJI"
indexsymbol = "^NSEBANK"
stop_LTP_threads = False
currentRSI = 0.0
currentRSI60 = 0.0
currentRSI15 = 0.0
currentRSI5 = 0.0

def startRSICalculation():

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

    global stop_LTP_threads

    ltp = 0.0

    while (1):
        try:
            ltpsymbol = txt_NOption.get()

            try:
                price1Min = yf.download(tickers=indexsymbol, period='1d', interval='1m')
                #print(optionltp.iloc[-1]['Close'])
                ltp = roundtick(price1Min.iloc[-1]['Close'])
                rsi1all = ta.RSI(price1Min['Close'])
                currentRSI_l = roundtick(rsi1all.iloc[-1])

                #print(currentRSI)

                txt_LTP.delete(0, END)
                txt_LTP.insert(0, str(ltp))

                price1Hr = yf.download(tickers=indexsymbol, period='5d', interval='1h')
                rsi1Hrall = ta.RSI(price1Hr['Close'])
                currentRSI60_l = roundtick(rsi1Hrall.iloc[-1])

                price15min = yf.download(tickers=indexsymbol, period='2d', interval='15m')
                rsi15Minall = ta.RSI(price15min['Close'])
                currentRSI15_l = roundtick(rsi15Minall.iloc[-1])

                price5Min = yf.download(tickers=indexsymbol, period='2d', interval='5m')
                rsi5Minall = ta.RSI(price5Min['Close'])
                currentRSI5_l = roundtick(rsi5Minall.iloc[-1])

                if price5Min['open'].iloc[-1] >= price5Min['close'].iloc[-2]:
                    print("Current open is high than last close", "Close = ",price5Min['close'].iloc[-2], "Open = ", price5Min['open'].iloc[-1] )


                lock.acquire()
                currentRSI = currentRSI_l
                currentRSI60 = currentRSI60_l
                currentRSI15 = currentRSI15_l
                currentRSI5 = currentRSI5_l
                lock.release()

                txt_RSI60.delete(0, END)
                txt_RSI60.insert(0, str(currentRSI60_l))
                txt_RSI15.delete(0, END)
                txt_RSI15.insert(0, str(currentRSI15_l))
                txt_RSI5.delete(0, END)
                txt_RSI5.insert(0, str(currentRSI5_l))
                txt_RSI1.delete(0, END)
                txt_RSI1.insert(0, str(currentRSI_l))

            except Exception as e:
                txt_LTP.delete(0, END)
                print('7 Exception Occurred in LTP order = ', e)

            # if fTarget > 0.0:
            #     if ltp >= fTarget:
            #         print("Target Hit place exit orders")
            #         fTarget = 0.0
            #
            # if fSL > 0.0:
            #     if ltp <= fSL:
            #         print("Stop loss hit")
            #         fSL = 0.0

        except Exception as e:
            txt_LTP.delete(0, END)
            print('7.1 Exception Occurred in LTP thread = ', e)

        now = datetime.now()

        # current_time = now.strftime("%H:%M:%S")
        current_time = datetime.today().strftime("%I:%M:%S  %p")
        lbl_Time.config(text=current_time)

        if stop_LTP_threads:
            return

        time.sleep(1)

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

    t2 = threading.Thread(target=findSetup)
    t2.daemon = True
    t2.start()

    # t1.join()
    # t2.join()

# create root window
root = Tk()

# root window title and dimension
root.title("RSI Bounce")

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