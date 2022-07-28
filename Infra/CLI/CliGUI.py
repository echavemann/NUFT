from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import CLI
import os

class CLI_GUI(App):
    def build(self):
        # Window Settings
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.9)
        self.window.pos_hint = {"center_x" : 0.5, "center_y": 0.5}

        # Main Label
        self.main_label = Label(
            text="NUFT CLI",
            font_size= 100,
            color='#00FFCE'
            )

        # Sub Label
        self.sub_label = Label(
            text="Available Commands: start, stop, query, backtest, systat, excstat, train",
            font_size= 25,
            color='#00FFCE'
            )
        
        # Text Input Box
        self.user = TextInput(
            multiline=False,
            padding_y = (20,20),
            size_hint = (1,0.5)
            )

        # Button 
        self.button = Button(
            text="Run Command",
            size_hint = (0.3,0.3),
            bold = True,
            background_color = '#00FFCE'
            )
        # Linking button to callback function
        self.button.bind(on_press=self.callback)
        

        self.window.add_widget(self.main_label)
        self.window.add_widget(self.sub_label)
        self.window.add_widget(self.user)
        self.window.add_widget(self.button)
        return self.window
    
    # Callback function linked to button
    def callback(self, instance):
        self.main_label.text = self.user.text + " executed!"

        if(self.user.text=="start"):
            os.system("python3 Infra/CLI.py start")
        elif(self.user.text=="stop"):
            os.system("python3 Infra/CLI.py stop")
    
# Running the App
CLI_GUI().run()