import tkinter as tk
from tkinter import ttk
import websocket
import json
import threading
import config


class CryptoTicker:
    def __init__(self, parent, symbol, display_name):
        self.parent = parent
        self.symbol = symbol.lower()
        self.display_name = display_name

        self.is_active = False
        self.ws = None

        # Create UI frame
        self.frame = ttk.Frame(parent, relief="solid",
                               borderwidth=1, padding=20)

        # Title
        ttk.Label(self.frame, text=self.display_name,
                  font=("Arial", 16, "bold")).pack()

        # Price
        self.price_label = tk.Label(self.frame, text="--",
                                    font=("Arial", 40, "bold"))
        self.price_label.pack(pady=10)

        # Change %
        self.change_label = ttk.Label(
            self.frame, text="--", font=("Arial", 12))
        self.change_label.pack()

    # WebSocket management
    def start(self):
        if self.is_active:
            return

        self.is_active = True
        ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@ticker"

        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=self.on_message,
            on_error=lambda ws, err: print(f"{self.symbol} error:", err),
            on_close=lambda ws, s, m: print(f"{self.symbol} closed"),
            on_open=lambda ws: print(f"{self.symbol} connected")
        )

        threading.Thread(target=self.ws.run_forever, daemon=True).start()

    def stop(self):
        self.is_active = False
        if self.ws:
            self.ws.close()
            self.ws = None

    # WebSocket events
    def on_message(self, ws, message):
        if not self.is_active:
            return

        try:
            data = json.loads(message)
            price = float(data["c"])
            change = float(data["p"])
            percent = float(data["P"])
        except Exception:
            return

        self.parent.after(0, self.update_display, price, change, percent)

    def update_display(self, price, change, percent):
        if not self.is_active:
            return

        color = config.COLOR_UP if change >= 0 else config.COLOR_DOWN

        self.price_label.config(text=f"{price:,.2f}", fg=color)

        sign = "+" if change >= 0 else ""
        self.change_label.config(
            text=f"{sign}{change:,.2f} ({sign}{percent:.2f}%)",
            foreground=color
        )

    # Layout helpers
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()
