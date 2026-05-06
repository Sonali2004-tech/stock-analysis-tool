import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Stock Analyzer Pro", layout="centered")

st.title("📊 Stock Analyzer Pro (Web App)")
st.write("Analyze stocks, calculate profit/loss, and view trends.")

# Stock list
stock_list = ["TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

# Input section
stock = st.selectbox("Select Stock", stock_list)
buy_price = st.number_input("Enter Buy Price", min_value=0.0, format="%.2f")
sell_price = st.number_input("Enter Sell Price", min_value=0.0, format="%.2f")

# Buttons
if st.button("Analyze"):

    if buy_price == 0 or sell_price == 0:
        st.error("Please enter valid buy and sell prices")
    else:
        # Fetch data
        data = yf.download(stock, period="6mo")

        if data.empty:
            st.error("Invalid stock or no data found")
        else:
            df = data.reset_index()

            # Moving averages
            df["MA20"] = df["Close"].rolling(window=20).mean()
            df["MA50"] = df["Close"].rolling(window=50).mean()

            # Profit/Loss
            profit = sell_price - buy_price

            if profit > 0:
                st.success(f"📈 Profit: ₹{profit:.2f}")
            else:
                st.error(f"📉 Loss: ₹{abs(profit):.2f}")

            # Trend detection
            if df["MA20"].iloc[-1] > df["MA50"].iloc[-1]:
                st.info("📈 Market Trend: Uptrend")
            else:
                st.info("📉 Market Trend: Downtrend")

            # Chart
            st.subheader("Stock Price Chart")

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df["Date"], df["Close"], label="Price")
            ax.plot(df["Date"], df["MA20"], label="MA20")
            ax.plot(df["Date"], df["MA50"], label="MA50")

            ax.set_title(f"{stock} Analysis")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend()

            plt.xticks(rotation=45)

            st.pyplot(fig)

# Clear info
st.write("---")
st.caption("Built using Streamlit + yfinance + pandas + matplotlib")