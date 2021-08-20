# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 16:56:26 2021

@author: obaris

yfinance period declarations:
Days : 1d,5d
Months : 1mo,3mo,6mo
Years : 1y,2y,5y,10y
Year-to-date (current year): ytd
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import dateutil.relativedelta 
import yfinance as yf

st.title("Nasdaq Stock prices")
st.markdown("This application is a Streamlit dashboard that can be used "
"to check stock prices")
data = pd.read_csv(r'nasdaq_screener_1628085554651.csv')
stock = st.selectbox("Please select or type the company name of a stock", data["Name"])
st.header("Information for the stock of " + stock)

periodselection =  st.selectbox(
        "Select an interval to see the stock movements",
        ("1 day", "1 week", "1 month", "3 months", "6 months", "1 year", "5 years"))

st.markdown("Note: For periods higher than 3 months, "
            "30-day rolling average graph is automatically added")

perioddict = {"1 day": "1d", "1 week": "7d", "1 month":"1mo", "3 months":"3mo", "6 months":"6mo", "1 year":"1y", "5 years":"5y"}
period = perioddict[periodselection]

day=0,
month=0

if periodselection=="1 day":
    day=1
    month=0
elif periodselection=="1 week":
    day=7
    month=0
elif periodselection=="1 month":
    day=0
    month=1
    year=0
elif periodselection=="3 months":
    day=0
    month=3
elif periodselection=="6 months":
    day=0
    month=6
elif periodselection=="1 year":
    day=0
    month=12
elif periodselection=="5 years":
    day=0
    month=60

today = datetime.date.today()
d2 = today - dateutil.relativedelta.relativedelta(months=month, days=day)

tickerSym = data.loc[data["Name"]==stock, 'Symbol']
tickerSymbol = tickerSym.array[0]

tickerData = yf.Ticker(tickerSymbol)

tickerDF = tickerData.history(period=period, start=d2, end=today)
tickerRolling = tickerDF.rolling(window=30).mean()
tickerRolling.iloc[0:30,:]=tickerDF.iloc[0:30,:]

fig = go.Figure()
fig.add_trace(go.Scatter(x=tickerDF.index, y=tickerDF.Close, name="Daily Price"))

wide=800

if month>3:
    fig.add_trace(go.Scatter(x=tickerRolling.index, y=tickerRolling.Close, name="30-day Rolling Average"))
    wide = 950

fig.update_layout(
    title="Price for " + stock,
    xaxis_title="Date",
    yaxis_title="Price",
    legend_title="Price change",
    width=wide, height=500,
    font=dict(
        size=16,
    )
)

fig2 = px.bar(x=tickerDF.index, y=tickerDF.Volume, title="Daily Volume for " + stock,
              width=800, height=500,
              labels={"x": "Date", "y": "Volume"})
fig2.update_layout(
    font=dict(
        size=16,
    )
)
st.plotly_chart(fig)
st.plotly_chart(fig2)