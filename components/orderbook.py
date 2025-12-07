import tkinter as tk
from tkinter import ttk
from utils.binance_api import get_orderbook


class OrderBookPanel:
    def __init__(self, parent, symbol="btcusdt"):
        self.parent = parent
        self.symbol = symbol.upper()

        self.frame = ttk.Frame(
            parent, padding=10, relief="solid", borderwidth=1)

        title = ttk.Label(
            self.frame,
            text=f"{self.symbol} Order Book",
            font=("Arial", 13, "bold")
        )
        title.pack(pady=(0, 10))

        content = ttk.Frame(self.frame)
        content.pack(fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(content)
        self.right_frame = ttk.Frame(content)

        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH,
                             expand=True, padx=(0, 10))
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH,
                              expand=True, padx=(10, 0))

        self.left_label = ttk.Label(
            self.left_frame,
            text="BIDS (Buys – Highest to Lowest Price)",
            font=("Arial", 9, "bold"),
            foreground="#00aa00"
        )
        self.left_label.pack(anchor="w", pady=(0, 5))

        self.right_label = ttk.Label(
            self.right_frame,
            text="ASKS (Sells – Lowest to Highest Price)",
            font=("Arial", 9, "bold"),
            foreground="#cc0000"
        )
        self.right_label.pack(anchor="e", pady=(0, 5))

        self._build_treeviews()

        self.update_loop()

    def _build_treeviews(self):
        left_table_frame = ttk.Frame(self.left_frame, relief="flat")
        left_table_frame.pack(fill=tk.BOTH, expand=True)

        self.bids = ttk.Treeview(
            left_table_frame,
            columns=("Price", "Quantity"),
            show="headings",
            selectmode="none",
            height=12
        )
        self.bids.heading("Price", text="Price")
        self.bids.heading("Quantity", text="Quantity")
        self.bids.column("Price", anchor="center", width=120)
        self.bids.column("Quantity", anchor="center", width=120)
        self.bids.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_table_frame = ttk.Frame(self.right_frame, relief="flat")
        right_table_frame.pack(fill=tk.BOTH, expand=True)

        self.asks = ttk.Treeview(
            right_table_frame,
            columns=("Price", "Quantity"),
            show="headings",
            selectmode="none",
            height=12
        )
        self.asks.heading("Price", text="Price")
        self.asks.heading("Quantity", text="Quantity")
        self.asks.column("Price", anchor="center", width=120)
        self.asks.column("Quantity", anchor="center", width=120)
        self.asks.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def update_loop(self):
        data = get_orderbook(self.symbol, limit=10)
        if data:
            self.update_tables(data)
        self.frame.after(2000, self.update_loop)

    def update_tables(self, data):
        self.bids.delete(*self.bids.get_children())
        self.asks.delete(*self.asks.get_children())

        for price, qty in data.get("bids", [])[:10]:
            self.bids.insert("", tk.END, values=(price, qty))

        for price, qty in data.get("asks", [])[:10]:
            self.asks.insert("", tk.END, values=(price, qty))

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def pack_forget(self):
        self.frame.pack_forget()
