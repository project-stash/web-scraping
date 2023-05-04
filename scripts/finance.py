import yfinance as yf
import pandas as pd
import scripts.plotly_layout as ply
import datetime as dt

def get_data(ticker,options):
    ticker = yf.Ticker(ticker)

    ## Data
    if (options == "hist"):
        data = ticker.history()
        data.index = pd.to_datetime(data.index)
        data['Date'] = data.index.date
    else:
        data = ticker.dividends
        data = data.to_frame()
        ## reset the index to have the date as a column 
        data = data.reset_index()
        ## we extract the year from the date column to aggregate it to year 
        data["year"] = data["Date"].dt.year
        data = data.groupby("year")["Dividends"].sum()
        data = data.to_frame()
        data = data.reset_index()

    return ply.create_plotly(data,options)