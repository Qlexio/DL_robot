""" Fractal indicator on M5 and M30."""
import numpy as np
import math
import talib

def fractal_ind(pd_eurusd, start=0):
    # Test fractal *** signalperiod = 15, signalsmaperiod = 30
    signalperiod = 15
    signalsmaperiod = 30

    fractal = np.array([])
    signal = np.array([])
    signalsma = np.array([])
    typ_priceM30 = np.array([])
    typ_priceM5 = np.array([])
    diffM30 = np.array([])
    diffM5 = np.array([])

    for i in range(start, len(pd_eurusd)):
        typM5 = (pd_eurusd["high"].iloc[i] + pd_eurusd["low"].iloc[i] + pd_eurusd["close"].iloc[i]) / 3
        typM30 = (pd_eurusd["high_M30"].iloc[i] + pd_eurusd["low_M30"].iloc[i] + pd_eurusd["close_M30"].iloc[i]) / 3
        typ_priceM5 = np.append(typ_priceM5, typM5)
        typ_priceM30 = np.append(typ_priceM30, typM30)

    start_bool = False
    for i in range(start, len(pd_eurusd)):
        if i == 0:
            diffM5 = np.append(diffM5, np.nan)
            diffM30 = np.append(diffM30, np.nan)
            continue
        if pd_eurusd["time"].iloc[i] % 1800 == 1500:
            if not start_bool:
                start_bool = True
                diffM5 = np.append(diffM5, np.abs(typ_priceM5[i] - typ_priceM5[i-1]))
                diffM30 = np.append(diffM30, np.nan)
                prev_pos = i
            else:
                diffM5 = np.append(diffM5, np.abs(typ_priceM5[i] - typ_priceM5[i-1]))
                diffM30 = np.append(diffM30, np.abs(typ_priceM30[i] - typ_priceM30[prev_pos]))
                prev_pos = i
        else:
            if not start_bool:
                diffM5 = np.append(diffM5, np.abs(typ_priceM5[i] - typ_priceM5[i-1]))
                diffM30 = np.append(diffM30, np.nan)
            else:
                diffM5 = np.append(diffM5, np.abs(typ_priceM5[i] - typ_priceM5[i-1]))
                diffM30 = np.append(diffM30, np.abs(typ_priceM30[i] - typ_priceM30[prev_pos]))

    q = 0
    p = 1
    sum = 0
    start_bool = False
    for i in range(start, len(pd_eurusd)):
        if i < len([i for i in np.isnan(diffM30) if i]):
            fractal = np.append(fractal, np.nan)
            continue
        if pd_eurusd["time"].iloc[i] % 1800 == 1500:
            if not start_bool:
                start_bool = True
                prev_pos = i
                fractal = np.append(fractal, np.nan)
            else:
                sum += diffM5[i]
                if sum == 0 or diffM30[i] == 0:
                    fractal = np.append(fractal, 0.0)
                else:
                    q = sum / diffM30[i]
                    if (q == 1):
                        fractal = np.append(fractal, 0.0)
                    else:
                        calc = math.log(p) / math.log(q)
                        fractal = np.append(fractal, calc)
                p = 1
                sum = 0
        else:
            if not start_bool:
                fractal = np.append(fractal, np.nan)
            else:
                sum += diffM5[i]
                if sum == 0 or diffM30[i] == 0:
                    fractal = np.append(fractal, 0.0)
                else:
                    q = sum / diffM30[i]
                    if (q == 1):
                        fractal = np.append(fractal, 0.0)
                    else:
                        calc = math.log(p) / math.log(q)
                        fractal = np.append(fractal, calc)
                p += 1

    signal = talib.SMA(fractal, timeperiod = signalperiod)
    signalsma = talib.SMA(fractal, timeperiod = signalsmaperiod)

    return signal, signalsma

def M30create(pd_eurusd, start=0):
    # Adjust M30 open, high, low, close values
    open = np.array([])
    high = np.array([])
    low = np.array([])
    close = np.array([])

    for i in range(start, len(pd_eurusd)):
        if pd_eurusd["time"].iloc[i] % 1800 == 0:
            open = np.append(open, pd_eurusd["open"].iloc[i])
            high = np.append(high, pd_eurusd["high"].iloc[i])
            low = np.append(low, pd_eurusd["low"].iloc[i])
            close = np.append(close, pd_eurusd["close"].iloc[i])
        else:
            open = np.append(open, open[-1])
            close = np.append(close, pd_eurusd["close"].iloc[i])

            if pd_eurusd["high"].iloc[i] > high[-1]:
                  high = np.append(high,  pd_eurusd["high"].iloc[i])
            else:
                  high = np.append(high, high[-1])

            if pd_eurusd["low"].iloc[i] < low[-1]:
                  low = np.append(low, pd_eurusd["low"].iloc[i])
            else:
                  low = np.append(low, low[-1])

    return open, high, low, close