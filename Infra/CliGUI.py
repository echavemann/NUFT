from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import CLI

class CLI_GUI(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.9)
        self.window.pos_hint = {"center_x" : 0.5, "center_y": 0.5}

        self.greeting = Label(
            text="Hello World",
            font_size= 100,
            color='#00FFCE'
            )
        self.window.add_widget(self.greeting)


        self.user = TextInput(
            multiline=False,
            padding_y = (20,20),
            size_hint = (1,0.5)
            )
        self.window.add_widget(self.user)


        self.button = Button(
            text="Run Command",
            size_hint = (1,0.5),
            bold = True,
            background_color = '#00FFCE'
            )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window
    
    def callback(self, instance):
        self.greeting.text = "Hello " + self.user.text + "!"


CLI_GUI().run()
























