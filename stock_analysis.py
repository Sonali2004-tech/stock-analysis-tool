import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def analyze_stock():
    stock = stock_var.get()
    buy = buy_var.get()
    sell = sell_var.get()

    if not stock or not buy or not sell:
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        buy = float(buy)
        sell = float(sell)
    except:
        messagebox.showerror("Error", "Enter valid numbers")
        return

    data = yf.download(stock, period="6mo")

    if data.empty:
        messagebox.showerror("Error", "Invalid stock name")
        return

    df = data.reset_index()

    df["MA20"] = df["Close"].rolling(window=20).mean()
    df["MA50"] = df["Close"].rolling(window=50).mean()

    profit = sell - buy
    result = f"Profit: ₹{profit:.2f}" if profit > 0 else f"Loss: ₹{abs(profit):.2f}"

    if df["MA20"].iloc[-1] > df["MA50"].iloc[-1]:
        trend = "Uptrend 📈"
    else:
        trend = "Downtrend 📉"

    icon = "📈" if profit > 0 else "📉"
    color = "green" if profit > 0 else "red"

    result_label.config(text=f"{icon} {result} | {trend}", fg=color)

    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["Close"], label="Price")
    plt.plot(df["Date"], df["MA20"], label="20-Day MA")
    plt.plot(df["Date"], df["MA50"], label="50-Day MA")

    plt.title(f"{stock} Stock Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def clear_fields():
    stock_var.set("")
    buy_var.set("")
    sell_var.set("")
    result_label.config(text="")

root = tk.Tk()
root.title("Stock Analyzer Pro")
root.geometry("500x450")
root.configure(bg="#0f172a")

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#0f172a", foreground="white", font=("Segoe UI", 10))

title = tk.Label(root, text="📊 Stock Analyzer", font=("Segoe UI", 16, "bold"),
                 bg="#0f172a", fg="white")
title.pack(pady=10)

stock_var = tk.StringVar()
buy_var = tk.StringVar()
sell_var = tk.StringVar()

frame = tk.Frame(root, bg="#0f172a")
frame.pack(pady=10)

ttk.Label(frame, text="Stock (Select)").grid(row=0, column=0, pady=5)
stock_list = ["TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

dropdown = ttk.Combobox(frame, textvariable=stock_var, values=stock_list)
dropdown.grid(row=0, column=1)
dropdown.current(0)
ttk.Label(frame, text="Buy Price").grid(row=1, column=0, pady=5)
ttk.Entry(frame, textvariable=buy_var).grid(row=1, column=1)

ttk.Label(frame, text="Sell Price").grid(row=2, column=0, pady=5)
ttk.Entry(frame, textvariable=sell_var).grid(row=2, column=1)

ttk.Button(root, text="Analyze", command=analyze_stock).pack(pady=10)
ttk.Button(root, text="Clear", command=clear_fields).pack()

result_label = tk.Label(root, text="", font=("Segoe UI", 12, "bold"),
                        bg="#0f172a", fg="green")
result_label.pack(pady=10)

root.mainloop()