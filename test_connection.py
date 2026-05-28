"""
Test ket noi QuantVN API.

Chay:
    python test_connection.py

Yeu cau:
    - File .env co bien QUANTVN_API_KEY
    - Da `pip install quantvn pandas python-dotenv`
"""

import os
import sys

from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    api_key = os.getenv("QUANTVN_API_KEY", "").strip()

    if not api_key or api_key.startswith("PASTE_") or api_key == "your_api_key_here":
        print("[ERROR] Chua dien QUANTVN_API_KEY vao file .env")
        print("        Mo file .env, paste key 'trading_quant' tu platform quantvn.com")
        return 1

    from quantvn.vn.data.utils import client
    from quantvn.vn.data import get_stock_hist

    print(f"[1/3] Khoi tao client voi api_key (***{api_key[-4:]})...")
    client(apikey=api_key)
    print("      OK")

    print("[2/3] Lay du lieu lich su VIC (resolution=1H)...")
    df = get_stock_hist("VIC", resolution="1H")
    print(f"      OK - shape={df.shape}")

    print("[3/3] 5 dong cuoi cua DataFrame:")
    print(df.tail().to_string())

    print("\n[SUCCESS] Ket noi thanh cong - san sang viet strategy.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
