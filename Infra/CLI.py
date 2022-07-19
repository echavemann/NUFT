# Command Line Interface 
import argparse
import sys

CURRENCY = {
    "btc" : "BTC",
    "eth" : "ETH",
    "usd" : "USD"
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NUFT Command Line Interface")
    parser.add_argument("coin", type=str, choices=CURRENCY)
    parsed_args = parser.parse_args()
    print(parsed_args)