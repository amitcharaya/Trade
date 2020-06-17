import plotly    
import webbrowser

import plotly.graph_objs as go

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from datetime import date
from nsepy import get_history
from nsepy.history import get_price_list
from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
prices = get_price_list(dt=date(2020,3,9))

#print(prices)


    #if row.TOTALTRADES>1000:
#print(prices[prices.TOTALTRADES>300000])


df=get_history(symbol="NIFTY 50",start=date(2020,6,1),end=date(2020,6,17),index=True)





#
#
def candle_df(df):
    #df_candle=first_letter_upper(df)
    df_candle=df.copy()
    df_candle['candle_score']=0
    df_candle['candle_pattern']=''


    for c in range(2,len(df_candle)):
        cscore,cpattern=0,''
        lst_2=[df_candle['Open'].iloc[c-2],df_candle['High'].iloc[c-2],df_candle['Low'].iloc[c-2],df_candle['Close'].iloc[c-2]]
        lst_1=[df_candle['Open'].iloc[c-1],df_candle['High'].iloc[c-1],df_candle['Low'].iloc[c-1],df_candle['Close'].iloc[c-1]]
        lst_0=[df_candle['Open'].iloc[c],df_candle['High'].iloc[c],df_candle['Low'].iloc[c],df_candle['Close'].iloc[c]]
        cscore,cpattern=candle_score(lst_0,lst_1,lst_2)    
        df_candle['candle_score'].iat[c]=cscore
        df_candle['candle_pattern'].iat[c]=cpattern
    
    df_candle['candle_cumsum']=df_candle['candle_score'].rolling(3).sum()
    
    return df_candle

def candle_score(lst_0,lst_1,lst_2):    
    
    O_0,H_0,L_0,C_0=lst_0[0],lst_0[1],lst_0[2],lst_0[3]
    O_1,H_1,L_1,C_1=lst_1[0],lst_1[1],lst_1[2],lst_1[3]
    O_2,H_2,L_2,C_2=lst_2[0],lst_2[1],lst_2[2],lst_2[3]
    
    DojiSize = 0.1
    
    doji=(abs(O_0 - C_0) <= (H_0 - L_0) * DojiSize)
    
    hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((C_0 - L_0)/(.001 + H_0 - L_0) > 0.6) & ((O_0 - L_0)/(.001 + H_0 - L_0) > 0.6))
    
    inverted_hammer=(((H_0 - L_0)>3*(O_0 -C_0)) &  ((H_0 - C_0)/(.001 + H_0 - L_0) > 0.6) & ((H_0 - O_0)/(.001 + H_0 - L_0) > 0.6))
    
    bullish_reversal= (O_2 > C_2)&(O_1 > C_1)&doji
    
    bearish_reversal= (O_2 < C_2)&(O_1 < C_1)&doji
    
    evening_star=(C_2 > O_2) & (min(O_1, C_1) > C_2) & (O_0 < min(O_1, C_1)) & (C_0 < O_0 )
    
    morning_star=(C_2 < O_2) & (min(O_1, C_1) < C_2) & (O_0 > min(O_1, C_1)) & (C_0 > O_0 )
    
    shooting_Star_bearish=(O_1 < C_1) & (O_0 > C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
    shooting_Star_bullish=(O_1 > C_1) & (O_0 < C_1) & ((H_0 - max(O_0, C_0)) >= abs(O_0 - C_0) * 3) & ((min(C_0, O_0) - L_0 )<= abs(O_0 - C_0)) & inverted_hammer
    
    bearish_harami=(C_1 > O_1) & (O_0 > C_0) & (O_0 <= C_1) & (O_1 <= C_0) & ((O_0 - C_0) < (C_1 - O_1 ))
    
    Bullish_Harami=(O_1 > C_1) & (C_0 > O_0) & (C_0 <= O_1) & (C_1 <= O_0) & ((C_0 - O_0) < (O_1 - C_1))
    
    Bearish_Engulfing=((C_1 > O_1) & (O_0 > C_0)) & ((O_0 >= C_1) & (O_1 >= C_0)) & ((O_0 - C_0) > (C_1 - O_1 ))
    
    Bullish_Engulfing=(O_1 > C_1) & (C_0 > O_0) & (C_0 >= O_1) & (C_1 >= O_0) & ((C_0 - O_0) > (O_1 - C_1 ))
    
    Piercing_Line_bullish=(C_1 < O_1) & (C_0 > O_0) & (O_0 < L_1) & (C_0 > C_1)& (C_0>((O_1 + C_1)/2)) & (C_0 < O_1)

    Hanging_Man_bullish=(C_1 < O_1) & (O_0 < L_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

    Hanging_Man_bearish=(C_1 > O_1) & (C_0>((O_1 + C_1)/2)) & (C_0 < O_1) & hammer

    strCandle=''
    candle_score=0
    
    if doji:
        strCandle='doji'
    if evening_star:
        strCandle=strCandle+'/ '+'evening_star'
        candle_score=candle_score-1
    if morning_star:
        strCandle=strCandle+'/ '+'morning_star'
        candle_score=candle_score+1
    if shooting_Star_bearish:
        strCandle=strCandle+'/ '+'shooting_Star_bearish'
        candle_score=candle_score-1
    if shooting_Star_bullish:
        strCandle=strCandle+'/ '+'shooting_Star_bullish'
        candle_score=candle_score-1
    if    hammer:
        strCandle=strCandle+'/ '+'hammer'
    if    inverted_hammer:
        strCandle=strCandle+'/ '+'inverted_hammer'
    if    bearish_harami:
        strCandle=strCandle+'/ '+'bearish_harami'
        candle_score=candle_score-1
    if    Bullish_Harami:
        strCandle=strCandle+'/ '+'Bullish_Harami'
        candle_score=candle_score+1
    if    Bearish_Engulfing:
        strCandle=strCandle+'/ '+'Bearish_Engulfing'
        candle_score=candle_score-1
    if    bullish_reversal:
        strCandle=strCandle+'/ '+'Bullish_Engulfing'
        candle_score=candle_score+1
    if    bullish_reversal:
        strCandle=strCandle+'/ '+'bullish_reversal'
        candle_score=candle_score+1
    if    bearish_reversal:
        strCandle=strCandle+'/ '+'bearish_reversal'
        candle_score=candle_score-1
    if    Piercing_Line_bullish:
        strCandle=strCandle+'/ '+'Piercing_Line_bullish'
        candle_score=candle_score+1
    if    Hanging_Man_bearish:
        strCandle=strCandle+'/ '+'Hanging_Man_bearish'
        candle_score=candle_score-1
    if    Hanging_Man_bullish:
        strCandle=strCandle+'/ '+'Hanging_Man_bullish'
        candle_score=candle_score+1
        
    #return candle_score
    return candle_score,strCandle
    

df=candle_df(df)
html = df.to_html()
text_file = open("index.html", "w")
text_file.write(html)
text_file.close()
url = "index.html"
webbrowser.open(url,new=2)


df['signal']=np.where(df['candle_cumsum']>1,1,-1)
df['signal2']=np.where(df['signal']==df['signal'].shift(1),0,df['signal'])
##Lets visualize it
df.plot(y=['Close','signal2'],secondary_y='signal2',figsize=(12,8))


trace = go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],

                close=df['Close'])
data2 = [trace]

plot(data2)
