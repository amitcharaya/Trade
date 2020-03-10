import pandas as pd
from datetime import date
from nsepy import get_history
from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt

sbin=get_history("YESBANK",start=date(2020,1,1),end=date(2020,3,10))
sbin_close=sbin[['Close']]
#sbin_close.set_index('Date',inplace=True)
print((sbin_close))
plt.figure(figsize=(14,5))

plt.plot(sbin_close,'b')
plt.plot(sbin_close,'ro')
plt.grid(True)
plt.title(" Yes Bank Close price Graph")
plt.xlabel("Date")
plt.ylabel("Price")
plt.plot(sbin_close)
plt.show()


