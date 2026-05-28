"""
Multi-MA Crossover Strategy cho VN30F1M khung 1H.

Logic:
    - Tinh 4 duong MA tren gia Close: MA10, MA20, MA50, MA200
    - LONG  ( 1): MA10 > MA20 > MA50 > MA200 (bullish stack)
    - SHORT (-1): MA10 < MA20 < MA50 < MA200 (bearish stack)
    - HOLD  ( 0): cac truong hop con lai

Input format (chuan QuantVN platform):
    DataFrame phai co cac cot: Date, time, Open, High, Low, Close, volume

Output:
    DataFrame goc + 4 cot ma_X + cot 'position' ({-1, 0, 1}).
"""

import os
import sys

import numpy as np
import pandas as pd


MA_WINDOWS = (10, 20, 50, 200)


def gen_position(df: pd.DataFrame) -> pd.DataFrame:
    """Tao tin hieu Multi-MA stack (10/20/50/200) symmetric long/short.

    Tham so
    -------
    df : pd.DataFrame
        DataFrame OHLCV co cac cot: Date, time, Open, High, Low, Close, volume.

    Tra ve
    ------
    pd.DataFrame
        DataFrame goc + ma_10, ma_20, ma_50, ma_200, 'position' ({-1, 0, 1}).
    """
    df = df.copy()

    # Tinh 4 duong MA tren Close
    for w in MA_WINDOWS:
        df[f"ma_{w}"] = df["Close"].rolling(w).mean()

    # Bullish stack: MA10 > MA20 > MA50 > MA200 -> Long
    bullish = (
        (df["ma_10"] > df["ma_20"])
        & (df["ma_20"] > df["ma_50"])
        & (df["ma_50"] > df["ma_200"])
    )
    # Bearish stack: MA10 < MA20 < MA50 < MA200 -> Short
    bearish = (
        (df["ma_10"] < df["ma_20"])
        & (df["ma_20"] < df["ma_50"])
        & (df["ma_50"] < df["ma_200"])
    )

    df["position"] = 0
    df.loc[bullish, "position"] = 1
    df.loc[bearish, "position"] = -1

    return df


# ===== Helper for local testing (khong dung khi upload platform) =====

def load_vn30f1m_1h() -> pd.DataFrame:
    """Lay du lieu VN30F1M va resample 1m -> 1H voi format chuan.

    Tra ve DataFrame co cac cot: Date, time, Open, High, Low, Close, volume.
    """
    from quantvn.vn.data import get_derivatives_hist

    df = get_derivatives_hist("VN30F1M", "1m")
    # df hien tai co: Date, time, Open, High, Low, Close, volume, Datetime
    # Resample sang 1H
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df = df.set_index("Datetime")
    agg = df.resample("1h", label="left", closed="left").agg({
        "Open":   "first",
        "High":   "max",
        "Low":    "min",
        "Close":  "last",
        "volume": "sum",
    }).dropna(subset=["Close"]).reset_index()

    # Tao Date, time tu Datetime, giu dung 7 cot chuan
    agg["Date"] = agg["Datetime"].dt.strftime("%Y-%m-%d")
    agg["time"] = agg["Datetime"].dt.strftime("%H:%M:%S")
    return agg[["Date", "time", "Open", "High", "Low", "Close", "volume"]]


def main() -> int:
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("QUANTVN_API_KEY", "").strip()
    if not api_key or api_key.startswith("PASTE_"):
        print("[ERROR] Chua dien QUANTVN_API_KEY vao .env")
        return 1

    from quantvn import client
    from quantvn.vn.metrics import Backtest_Derivates, Metrics

    print(f"[1/5] client(***{api_key[-4:]})... OK")
    client(apikey=api_key)

    print("[2/5] Loading VN30F1M data, resample to 1H...")
    df = load_vn30f1m_1h()
    print(f"      OK - shape={df.shape}")
    print(f"      Columns: {list(df.columns)}")
    print(f"      Range: {df['Date'].iloc[0]} {df['time'].iloc[0]} -> {df['Date'].iloc[-1]} {df['time'].iloc[-1]}")

    print("\n[3/5] gen_position - Multi-MA 10/20/50/200 stack...")
    df_pos = gen_position(df)
    counts  = df_pos["position"].value_counts().sort_index().to_dict()
    bars_in = int((df_pos["position"] != 0).sum())
    flips   = int((df_pos["position"].diff().fillna(0) != 0).sum())
    print(f"      OK - position dist: {counts}")
    print(f"      Bars in market: {bars_in} ({bars_in/len(df_pos)*100:.1f}%)")
    print(f"      Flips: {flips}")

    print("\n[4/5] Backtest_Derivates(pnl_type='raw')...")
    bt_raw  = Backtest_Derivates(df_pos, pnl_type="raw")
    pnl_raw = bt_raw.PNL().dropna()
    print(f"      Final PnL raw    : {pnl_raw.iloc[-1]:,.2f}")
    print(f"      Max  PnL raw    : {pnl_raw.max():,.2f}")
    print(f"      Min  PnL raw    : {pnl_raw.min():,.2f}")

    print("\n[5/5] Backtest_Derivates(pnl_type='after_fees') + Metrics...")
    bt_af  = Backtest_Derivates(df_pos, pnl_type="after_fees")
    pnl_af = bt_af.PNL().dropna()
    print(f"      Final PnL after-fees: {pnl_af.iloc[-1]:,.2f}")
    print(f"      Max  PnL after-fees: {pnl_af.max():,.2f}")
    print(f"      Min  PnL after-fees: {pnl_af.min():,.2f}")

    if pnl_raw.iloc[-1] != 0:
        fee_pct = (1 - pnl_af.iloc[-1] / pnl_raw.iloc[-1]) * 100
        print(f"      Phi tieu hao: {pnl_raw.iloc[-1] - pnl_af.iloc[-1]:,.2f} ({fee_pct:.1f}% raw PnL)")

    # Metrics chinh thuc QuantVN
    metrics = Metrics(bt_af)
    print(f"\n      === Metrics chinh thuc QuantVN ===")
    print(f"      Sharpe Ratio    : {metrics.sharpe():.3f}")
    print(f"      Sortino Ratio   : {metrics.sortino():.3f}")
    print(f"      Calmar Ratio    : {metrics.calmar():.3f}")
    print(f"      Max Drawdown    : {metrics.max_drawdown()*100:.2f}%")
    print(f"      Win Rate        : {metrics.win_rate()*100:.2f}%")
    print(f"      Profit Factor   : {metrics.profit_factor():.3f}")
    print(f"      Average Win     : {metrics.avg_win():,.2f}")
    print(f"      Average Loss    : {metrics.avg_loss():,.2f}")
    print(f"      VaR (95%)       : {metrics.value_at_risk(confidence_level=0.95):,.2f}")
    print(f"      Risk of Ruin    : {metrics.risk_of_ruin():.4f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
