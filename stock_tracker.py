"""Track a sample stock portfolio and append valuation snapshots to CSV.

Quotes are provided by yfinance. Example holdings are placeholders, not advice.
"""
import csv
from datetime import datetime, timezone
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    yf = None

# Replace these examples with your own ticker symbols and quantities.
HOLDINGS = {
    "AAPL": {"shares": 2, "average_cost": 180.00},
    "MSFT": {"shares": 1, "average_cost": 400.00},
}
LOG_FILE = Path("portfolio_log.csv")
COLUMNS = [
    "timestamp_utc", "ticker", "shares", "average_cost",
    "current_price", "market_value", "cost_basis", "profit_loss", "profit_loss_pct"
]


def fetch_price(ticker):
    """Return the latest available price from yfinance, or raise an error."""
    if yf is None:
        raise RuntimeError("Missing dependency. Run: python -m pip install -r task2_stock_tracker/requirements.txt")
    history = yf.Ticker(ticker).history(period="5d", interval="1d")
    if history.empty or "Close" not in history:
        raise ValueError(f"No quote data returned for {ticker}. Check ticker/internet access.")
    close = history["Close"].dropna()
    if close.empty:
        raise ValueError(f"No valid closing price found for {ticker}.")
    return float(close.iloc[-1])


def calculate_position(shares, average_cost, current_price):
    cost_basis = shares * average_cost
    market_value = shares * current_price
    profit_loss = market_value - cost_basis
    pct = (profit_loss / cost_basis * 100) if cost_basis else 0.0
    return {
        "market_value": market_value,
        "cost_basis": cost_basis,
        "profit_loss": profit_loss,
        "profit_loss_pct": pct,
    }


def append_log(rows, path=LOG_FILE):
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def run_tracker(holdings=HOLDINGS, price_fetcher=fetch_price, log_file=LOG_FILE):
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    total_value = total_cost = total_pl = 0.0

    for ticker, details in holdings.items():
        shares = float(details["shares"])
        average_cost = float(details["average_cost"])
        try:
            current_price = float(price_fetcher(ticker))
            position = calculate_position(shares, average_cost, current_price)
        except Exception as exc:
            print(f"Skipping {ticker}: {exc}")
            continue

        total_value += position["market_value"]
        total_cost += position["cost_basis"]
        total_pl += position["profit_loss"]
        rows.append({
            "timestamp_utc": timestamp,
            "ticker": ticker,
            "shares": shares,
            "average_cost": f"{average_cost:.2f}",
            "current_price": f"{current_price:.2f}",
            "market_value": f"{position['market_value']:.2f}",
            "cost_basis": f"{position['cost_basis']:.2f}",
            "profit_loss": f"{position['profit_loss']:.2f}",
            "profit_loss_pct": f"{position['profit_loss_pct']:.2f}",
        })

    if rows:
        append_log(rows, Path(log_file))
        print("\nPortfolio snapshot")
        print("-" * 62)
        for row in rows:
            print(f"{row['ticker']:8} shares={row['shares']:g}  price={row['current_price']:>9}  "
                  f"value={row['market_value']:>10}  P/L={row['profit_loss']:>9}")
        total_pct = total_pl / total_cost * 100 if total_cost else 0.0
        print("-" * 62)
        print(f"Total market value: {total_value:.2f}")
        print(f"Total cost basis:   {total_cost:.2f}")
        print(f"Total P/L:          {total_pl:.2f} ({total_pct:.2f}%)")
        print(f"Snapshot appended to: {Path(log_file).resolve()}")
    else:
        print("No positions were priced; no CSV snapshot was written.")


if __name__ == "__main__":
    run_tracker()
