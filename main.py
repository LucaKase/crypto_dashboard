# main.py

import tkinter as tk
from tkinter import ttk
import config
from components.ticker import CryptoTicker


class CryptoDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)

        # Main container
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Toggle area
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        # Ticker display area
        self.ticker_frame = ttk.Frame(main_frame)
        self.ticker_frame.pack(fill=tk.X, expand=True)

        # --- Create tickers ---
        self.btc = CryptoTicker(self.ticker_frame, "btcusdt", "BTC/USDT")
        self.eth = CryptoTicker(self.ticker_frame, "ethusdt", "ETH/USDT")
        self.sol = CryptoTicker(self.ticker_frame, "solusdt", "SOL/USDT")

        # BTC always visible
        self.btc.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.btc.start()

        # ETH/SOL toggles
        self.eth_visible = False
        self.sol_visible = False

        ttk.Button(control_frame, text="Toggle ETH/USDT",
                   command=self.toggle_eth).pack(side=tk.LEFT, padx=10)

        ttk.Button(control_frame, text="Toggle SOL/USDT",
                   command=self.toggle_sol).pack(side=tk.LEFT, padx=10)

        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ------------------------
    # Toggle handlers
    # ------------------------
    def toggle_eth(self):
        if self.eth_visible:
            self.eth.stop()
            self.eth.pack_forget()
            self.eth_visible = False
        else:
            self.eth.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.eth.start()
            self.eth_visible = True

    def toggle_sol(self):
        if self.sol_visible:
            self.sol.stop()
            self.sol.pack_forget()
            self.sol_visible = False
        else:
            self.sol.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
            self.sol.start()
            self.sol_visible = True

    # ------------------------
    # Shutdown handling
    # ------------------------
    def on_closing(self):
        self.btc.stop()
        self.eth.stop()
        self.sol.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoDashboard(root)
    root.mainloop()
