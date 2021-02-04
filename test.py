from datetime import datetime
import MetaTrader5 as mt5
#import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#connect to mt5
if not mt5.initialize():
   print("Unable to connect to MT5")
   mt5.shutdown()

# you code here
# 
# get formatted datetme
date = datetime.now().strftime("%Y %m %d %H %M").split()
date[3] = (int(date[3]) + 3) % 24
for num, d in enumerate(date):
   date[num] = int(d)

eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(date[0],date[1],date[2],date[3],date[4]), 10080)
# for eurusd in eurusd_rates:
#    print(datetime.fromtimestamp(eurusd[0]))
print(type(eurusd_rates))
print(eurusd_rates)

mt5.shutdown()