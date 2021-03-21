import MetaTrader5 as mt5
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import talib
import pandas as pd
from fractal_indicator import *

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

timeframe = mt5.TIMEFRAME_M5

# Get dataset of previous trades recorded in order_dataset.csv
full_dataset = pd.read_csv("order_dataset.csv")
if len(full_dataset) == 0:
   closing = False
else:
   closing = True

# Wait until next bar before launching
while time() % 300 > 1:
   sleep(1)

# Set launching and start app
running = True

while running:
   if time() % 300 <= 10:
      pd_current = get_datas(symbol, timeframe, nb_bars)

      # Check to open positon

      # Test to buy
      lot = 0.1
      point = mt5.symbol_info(symbol).point
      price = mt5.symbol_info_tick(symbol).ask
      deviation = 20
      request = {
         "action": mt5.TRADE_ACTION_DEAL,
         "symbol": symbol,
         "volume": lot,
         "type": mt5.ORDER_TYPE_BUY,
         "price": price,
         # "sl": price - 100 * point,
         # "tp": price + 100 * point,
         "deviation": deviation,
         # "magic": 234000,
         # "comment": "python script open",
         "type_time": mt5.ORDER_TIME_GTC,
         "type_filling": mt5.ORDER_FILLING_RETURN,
      }
      # send a trading request
      result = mt5.order_send(request)
      # check the execution result
      print("1. order_send(): by {} {} lots at {}".format(symbol,lot,price))
      if result.retcode != mt5.TRADE_RETCODE_DONE:
         print("2. order_send failed, retcode={}".format(result.retcode))
      print("2. order_send done, ", result)
      closing = True

      # Check for closing position

      sleep(60)
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