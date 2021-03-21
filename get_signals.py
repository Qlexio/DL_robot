import pandas as pd
import MetaTrader5 as mt5

def signals(pd_eurusd):
    signalFrac = False
    signalCCI = 0
    
    # Fractal crossing
    if (( pd_eurusd["CustFractSignal"].iloc[-2] < pd_eurusd["CustFractSignalSMA"].iloc[-2] and
        pd_eurusd["CustFractSignal"].iloc[-1] > pd_eurusd["CustFractSignalSMA"].iloc[-1] ) or
        ( pd_eurusd["CustFractSignal"].iloc[-2] > pd_eurusd["CustFractSignalSMA"].iloc[-2] and
        pd_eurusd["CustFractSignal"].iloc[-1] < pd_eurusd["CustFractSignalSMA"].iloc[-1] )):
        signalFrac = True
    #CCI signal
    if pd_eurusd["CCI_M5"].iloc[-1] >= 100 and pd_eurusd["RSI_M5"].iloc[-1] >= 70:
        signalCCI = 1
    elif pd_eurusd["CCI_M5"].iloc[-1] <= -100 and pd_eurusd["RSI_M5"].iloc[-1] <= 30:
        signalCCI = -1

    return signalFrac, signalCCI

def send_order(lot, price, symbol, type):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": type,
        "price": price,
        "deviation": 20,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        # order not passed
        return False, None
    else:
        # order passed
        return True, result.order

def pivot(high, low, close):
    point = (high + low + close) / 3
    R1 = point + 0.382 * (high - low) # (2 * point) - low
    S1 = point - 0.382 * (high - low) # (2 * point) - high
    return R1, S1