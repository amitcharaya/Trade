import plotly    
from nsepy import get_history
import plotly.graph_objs as go
from datetime import date
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

df=get_history(symbol="NIFTY 50",start=date(2020,6,1),end=date(2020,6,17),index=True)
trace = go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],

                close=df['Close'])
data2 = [trace]

plot(data2)