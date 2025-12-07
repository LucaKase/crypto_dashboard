import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils.binance_api import get_klines
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from datetime import datetime
import numpy as np


class CandlestickPanel:
    def __init__(self, parent, symbol="btcusdt"):
        self.parent = parent
        self.symbol = symbol.upper()

        self.frame = ttk.Frame(
            parent, padding=10, relief="solid", borderwidth=1)

        title = ttk.Label(
            self.frame,
            text=f"{self.symbol} 1 Hour Candlestick Chart (Last 50)",
            font=("Arial", 13, "bold")
        )
        title.pack(pady=(0, 10))

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(211)
        self.ax_vol = self.fig.add_subplot(212, sharex=self.ax)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_chart()

    def update_chart(self):
        klines = get_klines(self.symbol, interval="1h", limit=50)
        if not klines:
            return

        times = [int(k[0]) / 1000 for k in klines]
        dates = [datetime.utcfromtimestamp(t) for t in times]
        x = mdates.date2num(dates)

        opens = np.array([float(k[1]) for k in klines])
        highs = np.array([float(k[2]) for k in klines])
        lows = np.array([float(k[3]) for k in klines])
        closes = np.array([float(k[4]) for k in klines])
        volumes = np.array([float(k[5]) for k in klines])

        self.ax.clear()
        self.ax_vol.clear()

        self.ax.xaxis_date()
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax.tick_params(axis='x', labelrotation=45)

        width = 0.03

        for xi, o, h, l, c in zip(x, opens, highs, lows, closes):
            color = 'green' if c >= o else 'red'

            self.ax.plot([xi, xi], [l, h], color='black', linewidth=1)

            lower = min(o, c)
            height = abs(c - o)
            rect = Rectangle(
                (xi - width/2, lower),
                width,
                height if height > 0 else 0.0001,
                facecolor=color,
                edgecolor='black',
                linewidth=0.5
            )
            self.ax.add_patch(rect)

        bar_colors = ['green' if c >=
                      o else 'red' for o, c in zip(opens, closes)]
        self.ax_vol.bar(x, volumes, width=width, color=bar_colors)

        self.ax.set_title(f"{self.symbol} — 1h Candles", fontsize=10)
        self.ax.grid(alpha=0.3)
        self.ax_vol.set_ylabel("Volume")
        self.ax_vol.grid(alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

        # Auto-update every 15s
        self.frame.after(15000, self.update_chart)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()
