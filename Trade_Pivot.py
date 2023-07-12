from tkinter import *
import threading
import time
from datetime import datetime
from datetime import date
import yfinance as yf
import talib as ta
import pandas as pd

#symbol = "TCS.NS"
#symbol = "^NSEBANK"
#symbol = "ITC.NS"
#symbol = "BAJAJFINSV.NS"
symbol = "^NSEI"
current5MinCandleNo = 0
entryPrice = 0.0

def roundtick(x) -> float:
    global ticksize
    ticksize = 0.05
    fprice = 0.0
    fprice = (round(x / ticksize)) * ticksize

    fprice = round(fprice, 2)

    return fprice


def getLTP():

    global secondPreviousCandle_close
    global previousCandle_close
    global currentCandle_close
    global secondPreviousCandle_low

    global secondPreviousCandle_open
    global previousCandle_open
    global currentCandle_open

    global noOfTrade

    global candle_no
    global current5MinCandleNo
    global price5Min
    global price1Min
    global noOfCandles5Min
    global noOfCandles1Min

    price5Min = yf.download(tickers=symbol, period='5d', interval='5m', progress=False, rounding=True)
    price1Min = yf.download(tickers=symbol, period='5d', interval='1m', progress=False, rounding=True)

    price5Min.to_csv('5min_data2.csv')
    price1Min.to_csv('1min_data2.csv')

    noOfCandles5Min = len(price5Min)
    noOfCandles1Min = len(price1Min)

    #res5Min = pd.read_csv('5min_data1.csv')
    #noOfCandles5Min = len(res5Min)

    #res1Min = pd.read_csv('1min_data1.csv')
    #noOfCandles1Min = len(res1Min)

    current5MinCandleNo = 2
    noOfTrade = 1
    while(current5MinCandleNo < noOfCandles5Min):

        secondPreviousCandle_close = price5Min.iloc[current5MinCandleNo - 2]['Adj Close']
        previousCandle_close = price5Min.iloc[current5MinCandleNo - 1]['Adj Close']
        currentCandle_close = price5Min.iloc[current5MinCandleNo]['Adj Close']

        secondPreviousCandle_low = price5Min.iloc[current5MinCandleNo - 1]['Low']

        secondPreviousCandle_open = price5Min.iloc[current5MinCandleNo - 2]['Open']
        previousCandle_open = price5Min.iloc[current5MinCandleNo - 1]['Open']
        currentCandle_open = price5Min.iloc[current5MinCandleNo]['Open']

        candle_no = current5MinCandleNo + 2
        if find_Setup_Buy() == True:
            #Buy()
            sell()
            noOfTrade = noOfTrade + 1

        current5MinCandleNo += 1

#def Buy():
    #print("Trade no.", noOfTrade, " of ", symbol, "BUY at ", entryPrice, " at 5min Candle No (open) ", current5MinCandleNo)
    #print("Trade no.", noOfTrade, " of ", symbol, "BUY at ", entryPrice, " at 5min Candle No (open) ",
    #    current5MinCandleNo, " next1MinCandleNo = ", current5MinCandleNo * 5 + 1)


def find_Setup_Buy():
    global entryPrice
    #if (secondPreviousCandle_open > secondPreviousCandle_close and  #  SecondToPrevious is red
    #        previousCandle_open < previousCandle_close and # Previous candle is Green
            # currentCandle_open < currentCandle_close and #
      #      currentCandle_open > previousCandle_close):  # current open is above last close


    if (secondPreviousCandle_open > secondPreviousCandle_close and  #  SecondToPrevious candle is RED
            previousCandle_open > previousCandle_close and # Previous candle is RED
            currentCandle_open < currentCandle_close ): #  Current candle is GREEN

        #next1MinCandleNo = current5MinCandleNo * 5 + 1
        next1MinCandle_open = price1Min.iloc[current5MinCandleNo * 5 + 1]['Open']

        if ( next1MinCandle_open > currentCandle_close  ): # Next 1 min open is above Current 5 min
            entryPrice = next1MinCandle_open  #Buy
            print("Trade no.", noOfTrade, " of ", symbol, "BUY at ", entryPrice, " at 5min Candle No (open) ",
              current5MinCandleNo, " next1MinCandleNo = ", current5MinCandleNo * 5 + 1)
            return True

def sell():
    global current5MinCandleNo
   # global entryPrice
    current1MinCandleNo = current5MinCandleNo * 5 + 1
    tradeDuration1Min = 1

    #current1MinCandle_open = price1Min.iloc[current1MinCandleNo]['Open']
    target = entryPrice * 1.00015 #0.02 %
    stopLoss = secondPreviousCandle_low #currentCandle_close  * 0.9998  #0.01 %

    #if (stopLoss < (entryPrice * 0.99995) ):
    #if ((currentCandle_close - currentCandle_open) > ):
    #    stopLoss = entryPrice * 0.99995
    #    print(" Default Stop Loss of 0.1 % used ")

    target = roundtick(target)
    stopLoss = roundtick(stopLoss)



    print("EntryPrice = ", entryPrice, "TARGET = ", target, "STOP LOSS = ", stopLoss)
    #print(" ")

    while (current1MinCandleNo < noOfCandles1Min):
        current1MinCandle_close = price1Min.iloc[current1MinCandleNo]['Close']

        if current1MinCandle_close > target:
            print("TARGET ACHIEVED: Trade no=", noOfTrade, " of symbol = ", symbol, " sell = ", current1MinCandle_close, " at 1min Candle No ", current1MinCandleNo)
            profit = 500 * (current1MinCandle_close - entryPrice)
            print(" Profit = ", profit )
            print(" ")
            break
        if current1MinCandle_close < stopLoss:
            print("STOP LOSS HIT: Trade no=", noOfTrade, " of symbol = ", symbol, " sell = ", current1MinCandle_close, " at 1min Candle No ", current1MinCandleNo)
            loss = 500 * (current1MinCandle_close - entryPrice)
            print(" Loss = ", loss)
            print(" ")
            break
        current1MinCandleNo = current1MinCandleNo + 1

        if tradeDuration1Min == 5:
            tradeDuration1Min = 0
            current5MinCandleNo = current5MinCandleNo + 1

        tradeDuration1Min = tradeDuration1Min + 1

    #print("Sell() Done without sell")

getLTP()