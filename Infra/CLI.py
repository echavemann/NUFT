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
        "run" : "Run"}
        self.parser = argparse.ArgumentParser(description="NUFT Command Line Interface")
        self.argString = argString
    
    # Add arguments such as positional or flag args here 
    def parse(self):
        #Example run command 
        self.parser.add_argument("cmd", type=str, choices=self.commands, help="Type a cmd from the list of available commands")

        parsed_args = self.parser.parse_args(shlex.split(self.argString))
        return parsed_args

    # Determines the parsed command and runs the appropriate funciton 
    def execute_command(self):
        if (self.parse().cmd == "run"):
            Coinbase_Websocket.run()
            
def run(str):
    cli = CLI(str)
    cli.execute_command()
    