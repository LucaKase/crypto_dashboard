# Crypto Dashboard – Programming Final Project

## Overview

This project is a **real-time cryptocurrency dashboard** implemented in Python using **Tkinter** for the graphical user interface. It visualizes live and near real-time market data from the **Binance API**, combining WebSocket streams and REST endpoints.

The application displays:

- Live cryptocurrency price tickers
- A REST-based order book (top 10 bids and asks)
- A candlestick chart with volume data
- A responsive and toggleable dashboard layout

The project follows **object-oriented design principles** and clean separation of concerns.

---

## Features

### Core Functionality

- Clean OOP-based architecture
- Modular project structure
- Responsive UI layout
- Graceful shutdown of background connections

### Price Tickers

- BTC/USDT, ETH/USDT, SOL/USDT
- Real-time updates via Binance WebSocket streams
- Color-coded price movements (green/red)
- Display of 24-hour price change and percentage
- Toggle buttons for individual tickers

### Order Book

- REST API integration (Binance `/depth` endpoint)
- Displays top 10 bids and asks
- Clear labeling and separation of buy/sell sides
- Periodic refresh (every 2 seconds)
- Responsive panel layout

### Candlestick Chart

- 1-hour candlestick data (last 50 candles)
- Volume bars included
- Time-based x-axis
- Matplotlib embedded inside Tkinter
- Automatic refresh every 15 seconds

---

## Project Structure

```text
crypto_dashboard/
├── main.py # Entry point
├── components/
│ ├── init.py # Marks components as a Python package
│ ├── ticker.py # CryptoTicker class (WebSocket price ticker)
│ ├── orderbook.py # OrderBookPanel class (REST order book)
│ └── candles.py # CandlestickPanel class (candlestick chart)
├── utils/
│ ├── init.py # Utility package marker
│ └── binance_api.py # Binance REST API helper functions
├── config.py # Global configuration
└── requirements.txt # Project dependencies
```

---

## File Descriptions

### `main.py`

The main entry point of the application.

Responsibilities:

- Initializes the Tkinter root window
- Defines the overall dashboard layout
- Combines `pack` and `grid` for responsive UI behavior
- Creates and manages all dashboard components
- Implements toggle functionality for tickers, order book, and candles
- Handles graceful application shutdown

---

### `config.py`

Central configuration file.

Contains:

- Window title and size
- Cryptocurrency symbols
- Color constants for price movements

This allows easy UI and behavior changes without modifying application logic.

---

### `components/ticker.py`

Defines the `CryptoTicker` class.

Responsibilities:

- Connects to Binance WebSocket ticker streams
- Runs WebSocket connections in background threads
- Updates the GUI using `Tk.after()` for thread safety
- Displays:
  - Current price
  - 24h absolute change
  - 24h percentage change
- Supports start/stop behavior for toggling visibility

---

### `components/orderbook.py`

Defines the `OrderBookPanel` class.

Responsibilities:

- Fetches order book data using Binance REST API
- Displays top 10 bids and asks using `ttk.Treeview`
- Clearly separates buy and sell sides
- Periodically refreshes data every 2 seconds
- Designed to resize dynamically with the dashboard

---

### `components/candles.py`

Defines the `CandlestickPanel` class.

Responsibilities:

- Fetches OHLCV data using Binance REST API
- Converts timestamps into a time-based matplotlib axis
- Renders candlesticks manually using rectangles and wicks
- Displays volume bars below the price chart
- Embeds Matplotlib figures into Tkinter
- Automatically refreshes data every 15 seconds

---

### `utils/binance_api.py`

Utility module for Binance REST API access.

Responsibilities:

- Centralizes all REST requests
- Provides helper functions for:
  - Order book data (`get_orderbook`)
  - Candlestick data (`get_klines`)
- Handles request errors gracefully

---

### `__init__.py`

The `__init__.py` files are intentionally empty.

Purpose:

- Mark directories as Python packages
- Enable clean module imports across the project
- Required for proper package structure

---

## Installation & Setup

Clone the repository and run the pip install and then the main.py:

```bash
git clone https://github.com/LucaKase/crypto_dashboard
pip install -r requirements.txt
python3 main.py
```
