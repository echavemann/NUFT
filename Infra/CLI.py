# Command Line Interface 
import argparse
import sys
import Coinbase_Websocket
import shlex

# Command Line Interface Class 
class CLI():

    def __init__(self, argString):
        # Defines the list of commands available to the user
        self.commands = {
        "run" : "Run",
        #Starts all websockets, does not return control flow until all websockets are open. 
        "stop" : "Stop",
        #Stops all websockets, keeps connection open. 
        "backtest" : "Start Backtest", 
        #Takes in algorithm path, historical/realtime toggle, and start/end date if historical. Executes backtest. Returns control flow during backtest, but will autoprint result.  
        "systat" : "System Status",
        #Prints system status, operational and non-operational status of all websockets.
        "exchstat" : "Algo Status",
        #Prints performance of all algorithms.
        "query" : "Query memory",
        #Given query for backtesting report(s), returns backtesting report(s).
        "train" : "Passing Data ML Training"}
        #Given ML algorithm path, data query, finds data, trains model, returns control flow during train, but will autoprint result.
        self.parser = argparse.ArgumentParser(description="NUFT Command Line Interface")
        self.argString = argString
    
    # Add arguments such as positional or flag args here 
    def parse(self):
        #Main Command
        self.parser.add_argument("cmd", type=str, choices=self.commands, help="Type a cmd from the list of available commands")

        parsed_args = self.parser.parse_args(shlex.split(self.argString))
        return parsed_args

    # Determines the parsed command and runs the appropriate funciton 
    def execute_command(self):
        cmd = self.parse().cmd
        if (cmd == "run"):
            print("run")
        elif (cmd == "stop"):
            print("stop")
        elif (cmd == "backtest"):
            print("backtest")
        elif (cmd == "systat"):
            print("systat")
        elif (cmd == "exchstat"):
            print("exchstat")
        elif (cmd == "train"):
            print("train")

# Running the CLI, takes in an argString (To be input from GUI)           
def run(str):
    cli = CLI(str)
    cli.execute_command()

run("stop")