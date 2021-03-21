import MetaTrader5 as mt5
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import talib
import pandas as pd
from fractal_indicator import *
from get_signals import *

from time import time, sleep
# connect to mt5
if not mt5.initialize():
   print("Unable to connect to MT5")
   mt5.shutdown()

# you code here
# 

# Connect to account
account = 36363563
authorized = mt5.login(account)
if authorized:
   print(f"Connected to account {account}")
else:
   print(f"Failed to connect to account {account}")

# symbol --argparse ???
symbol = "GBPUSD" # "EURCHF" "EURUSD"
nb_bars = 100 # 1_000
lots = 0.01

timeframe = mt5.TIMEFRAME_M5

# Wait until next bar before launching
while time() % 300 > 1:
   sleep(1)

# Set launching and start app
running = True

while running:
   # Get dataset of previous trades recorded in order_dataset.csv
   full_dataset = pd.read_csv("order_dataset.csv")
   if len(full_dataset) == 0:
      closing = False
   else:
      closing = True


   if time() % 300 <= 10:
      pd_current = get_datas(symbol, timeframe, nb_bars)

      # Check to open positon

      # Get signals
      signalFrac, signalCCI = signals(pd_current)
      # Open BUY
      if signalCCI == -1 and signalFrac:
         result, ticket = send_order(lot=lots, price=mt5.symbol_info_tick(symbol).ask, symbol=symbol, type=mt5.ORDER_TYPE_BUY)

         if result:
            # calculate sl and tp
            R1, S1 = pivot(pd_current["high"].iloc[-1], pd_current["low"].iloc[-1], pd_current["close"].iloc[-1])
            # Put type,symbole,ticket,stoploss,takeprofit,lots to csv
            order_dataset = pd.DataFrame([["BUY", symbol, ticket, S1, R1, lots]], columns=["type", "symbole", "ticket", "stoploss", "takeprofit", "lots"])
            # Refresh inital dataset
            full_dataset = pd.read_csv("order_dataset.csv")
            full_dataset = full_dataset.append(order_dataset, ignore_index=True)
            # Copy to csv
            full_dataset.to_csv("order_dataset.csv", index=False)
            closing = True

      # Open SELL
      if signalCCI == 1 and signalFrac:
         result, ticket = send_order(lot=lots, price=mt5.symbol_info_tick(symbol).bid, symbol=symbol, type=mt5.ORDER_TYPE_SELL)

         if result:
            # calculate sl and tp
            R1, S1 = pivot(pd_current["high"].iloc[-1], pd_current["low"].iloc[-1], pd_current["close"].iloc[-1])
            # Put type,symbole,ticket,stoploss,takeprofit,lots to csv
            order_dataset = pd.DataFrame([["SELL", symbol, ticket, R1, S1, lots]], columns=["type", "symbole", "ticket", "stoploss", "takeprofit", "lots"])
            # Refresh inital dataset
            full_dataset = pd.read_csv("order_dataset.csv")
            full_dataset = full_dataset.append(order_dataset, ignore_index=True)
            # Copy to csv
            full_dataset.to_csv("order_dataset.csv", index=False)
            closing = True

      # Check for closing position
      if closing:
         pass

      sleep(10)
   else:
      # Check for closing position

      # Test for closing position
      if closing:
         position_id=result.order
         price=mt5.symbol_info_tick(symbol).bid
         deviation=20
         request={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "position": position_id,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_RETURN,
         }
         # send a trading request
         result=mt5.order_send(request)
         # check the execution result
         print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation));
         if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("4. order_send failed, retcode={}".format(result.retcode))
            print("   result",result)
         else:
            print("4. position #{} closed, {}".format(position_id,result))
         running = False

      sleep(10)


mt5.shutdown()