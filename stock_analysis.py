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

    data = yf.download(stock, period="7d")  

    if data.empty:
        messagebox.showerror("Error", "Invalid stock name")
        return

    df = data.reset_index()
    df["MA"] = df["Close"].rolling(3).mean()

    profit = sell - buy
    result = f"Profit: ₹{profit}" if profit > 0 else f"Loss: ₹{abs(profit)}"

    result_label.config(text=result)
    
    root.update() 

    plt.plot(df["Date"], df["Close"], label="Price")
    plt.plot(df["Date"], df["MA"], label="Moving Avg")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()


def clear_fields():
    stock_var.set("")
    buy_var.set("")
    sell_var.set("")
    result_label.config(text="")


# Window
root = tk.Tk()
root.title("Stock Analyzer Pro")
root.geometry("420x350")
root.configure(bg="#1e1e2f")

# Style
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#1e1e2f", foreground="white", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TEntry", padding=5)

# Title
title = tk.Label(root, text="📊 Stock Analyzer", font=("Segoe UI", 16, "bold"), bg="#1e1e2f", fg="white")
title.pack(pady=10)

# Variables
stock_var = tk.StringVar()
buy_var = tk.StringVar()
sell_var = tk.StringVar()

# Input Frame
frame = tk.Frame(root, bg="#1e1e2f")
frame.pack(pady=10)

ttk.Label(frame, text="Stock (e.g. TCS.NS)").grid(row=0, column=0, sticky="w", pady=5)
stock_list = ["TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]

dropdown = ttk.Combobox(frame, textvariable=stock_var, values=stock_list, state="readonly")
dropdown.grid(row=0, column=1)
dropdown.current(0)

ttk.Label(frame, text="Buy Price").grid(row=1, column=0, sticky="w", pady=5)
ttk.Entry(frame, textvariable=buy_var).grid(row=1, column=1)

ttk.Label(frame, text="Sell Price").grid(row=2, column=0, sticky="w", pady=5)
ttk.Entry(frame, textvariable=sell_var).grid(row=2, column=1)

# Button
ttk.Button(root, text="Analyze Stock", command=analyze_stock).pack(pady=15)
ttk.Button(root, text="Clear", command=clear_fields).pack()

# Result
result_label = tk.Label(root, text="", font=("Segoe UI", 12, "bold"), bg="#1e1e2f", fg="#00ffcc")
result_label.pack()

# Footer
footer = tk.Label(root, text="Built with Python", bg="#1e1e2f", fg="gray")
footer.pack(side="bottom", pady=10)

root.mainloop()