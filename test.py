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

# currency --argparse ???
currency = "GBPUSD" # "EURCHF" "EURUSD"

# indicator initialization
initialization = True
while initialization:
   if time() % 300 < 300-30:
      print("Test ok")
      initialization = False

      start = time()
      # Get forex datas
      eurusd_M5 = mt5.copy_rates_from_pos(currency, mt5.TIMEFRAME_M5, 1, 1_000) # 1_000

      pd_eurusd = pd.DataFrame(eurusd_M5)

      # Get indicators
      # CCI
      pd_eurusd["CCI_M5"] = talib.CCI(pd_eurusd["high"], pd_eurusd["low"], pd_eurusd["close"], timeperiod= 14)
      # Relative Strength Index
      pd_eurusd["RSI_M5"] = talib.RSI(pd_eurusd["close"], timeperiod=14)

      # Remove first empty lines of M30
      for i in range(0,7):
         if pd_eurusd["time"].iloc[0] % 1800 == 0:
            break
         else:
            pd_eurusd = pd_eurusd.drop([i])

      # Adjust M30 open, high, low, close values
      pd_eurusd["open_M30"], pd_eurusd["high_M30"], pd_eurusd["low_M30"], pd_eurusd["close_M30"] = M30create(pd_eurusd)

      # Test fractal *** signalperiod = 15, signalsmaperiod = 30
      pd_eurusd["CustFractSignal"], pd_eurusd["CustFractSignalSMA"] = fractal_ind(pd_eurusd)

      test = pd.DataFrame(pd_eurusd, columns=["time", "open_M30", "high_M30", "low_M30", "close_M30"])
      print(test[-15:])
      print("Time running: ", time()-start)

   else:
      print(datetime.fromtimestamp(time()))
      sleep(1)

running = True

while running:
   if time() % 300 <= 10:
      # Get bar -1 to calculate current indicator values
      current_M5 = mt5.copy_rates_from_pos(currency, mt5.TIMEFRAME_M5, 1, 1) # 1_000

      pd_current = pd.DataFrame(current_M5)
      print(pd_current)
   else:
      sleep(10)

# # get formatted datetme
# date = datetime.now().strftime("%Y %m %d %H %M").split()
# date[3] = (int(date[3]) + 3) % 24
# for num, d in enumerate(date):
#    date[num] = int(d)

# eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(date[0],date[1],date[2],date[3],date[4]), 10080)
# # for eurusd in eurusd_rates:
# #    print(datetime.fromtimestamp(eurusd[0]))
# print(type(eurusd_rates))
# print(eurusd_rates)

mt5.shutdown()