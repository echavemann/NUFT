# Command Line Interface 
import argparse
import sys
import multiprocessing as mp
import concurrent.futures as cf
import Binance_Websocket as bc
import Kucoin_Websocket as ks
import Coinbase_Websocket as cb
import Kraken_Websocket as kr
import Gemini_Websocket as gm
import pandas as pd
import asyncio
from main_script import start

class CLI():

    def __init__(self):
        self.commands = {
        "run" : "Run"}
        self.parser = argparse.ArgumentParser(description="NUFT Command Line Interface")
        
    def parse(self):
        self.parser.add_argument("cmd", type=str, choices=self.commands)
        parsed_args = self.parser.parse_args()
        return parsed_args

    def run_command(self):
        if (self.parse().cmd == "run"):
            print("hi")
            #Coinbase_Websocket.run()
            

if __name__ == "__main__":
    cli = CLI()
    cli.run_command()