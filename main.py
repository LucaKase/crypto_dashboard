import tkinter as tk
from tkinter import ttk
import config
from components.ticker import CryptoTicker
from components.orderbook import OrderBookPanel
from components.candles import CandlestickPanel


class CryptoDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_SIZE)

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        self.ticker_frame = ttk.Frame(main_frame)
        self.ticker_frame.pack(fill=tk.X, pady=10)

        self.lower_frame = ttk.Frame(main_frame)
        self.lower_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.lower_frame.columnconfigure(0, weight=1, uniform="half")
        self.lower_frame.columnconfigure(1, weight=1, uniform="half")

        self.orderbook = OrderBookPanel(self.lower_frame, symbol="btcusdt")
        self.candles = CandlestickPanel(self.lower_frame, symbol="btcusdt")

        self.orderbook.frame.grid(row=0, column=0, sticky="nsew", padx=10)
        self.candles.frame.grid(row=0, column=1, sticky="nsew", padx=10)

        self.ob_visible = True
        self.candles_visible = True

        self.btc = CryptoTicker(self.ticker_frame, "btcusdt", "BTC/USDT")
        self.eth = CryptoTicker(self.ticker_frame, "ethusdt", "ETH/USDT")
        self.sol = CryptoTicker(self.ticker_frame, "solusdt", "SOL/USDT")

        self.btc.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.btc.start()

        self.eth.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.eth.start()

        self.sol.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.sol.start()

        self.eth_visible = True
        self.sol_visible = True

        ttk.Button(control_frame, text="Toggle ETH/USDT",
                   command=self.toggle_eth).pack(side=tk.LEFT, padx=10)

        ttk.Button(control_frame, text="Toggle SOL/USDT",
                   command=self.toggle_sol).pack(side=tk.LEFT, padx=10)

        ttk.Button(control_frame, text="Toggle Orderbook",
                   command=self.toggle_orderbook).pack(side=tk.LEFT, padx=10)

        ttk.Button(control_frame, text="Toggle Candles",
                   command=self.toggle_candles).pack(side=tk.LEFT, padx=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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

    def toggle_orderbook(self):
        if self.ob_visible:
            self.orderbook.frame.grid_remove()
        else:
            self.orderbook.frame.grid(row=0, column=0, sticky="nsew", padx=10)
        self.ob_visible = not self.ob_visible

    def toggle_candles(self):
        if self.candles_visible:
            self.candles.frame.grid_remove()
        else:
            self.candles.frame.grid(row=0, column=1, sticky="nsew", padx=10)
        self.candles_visible = not self.candles_visible

    def on_closing(self):
        self.btc.stop()
        self.eth.stop()
        self.sol.stop()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoDashboard(root)
    root.mainloop()
