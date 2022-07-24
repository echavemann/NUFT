from kivy.app import App 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
import CLI

class CLI_GUI(App):
    def build(self):
        # Window Settings
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.9, 0.9)
        self.window.pos_hint = {"center_x" : 0.5, "center_y": 0.5}

        # Main Label
        self.greeting = Label(
            text="Hello World",
            font_size= 100,
            color='#00FFCE'
            )
        self.window.add_widget(self.greeting)

        # Text Input Box
        self.user = TextInput(
            multiline=False,
            padding_y = (20,20),
            size_hint = (1,0.5)
            )
        self.window.add_widget(self.user)

        # create a dropdown with 10 buttons
        self.dropdown = DropDown()
        for index in range(10):
        
            # Adding button in drop down list
            btn = Button(text ='Value % d' % index, size_hint_y = None, height = 40)
        
            # binding the button to show the text when selected
            btn.bind(on_release = lambda btn: self.dropdown.select(btn.text))
        
            # then add the button inside the dropdown
            self.dropdown.add_widget(btn)
        
        # create a big main button
        self.mainbutton = Button(text ='Hello', size_hint =(None, None), pos =(350, 300))
        
        # show the dropdown menu when the main button is released
        # note: all the bind() calls pass the instance of the caller
        # (here, the mainbutton instance) as the first argument of the callback
        # (here, dropdown.open.).
        self.mainbutton.bind(on_release = self.dropdown.open)
        
        # one last thing, listen for the selection in the
        # dropdown list and assign the data to the button text.
        self.dropdown.bind(on_select = lambda instance, x: setattr(self.mainbutton, 'text', x))
 
        # runtouchApp:
        # If you pass only a widget in runtouchApp(), a Window will
        # be created and your widget will be added to the window
        # as the root widget.
        runTouchApp(self.mainbutton)
        self.window.add_widget(self.mainbutton)

        # Button 
        self.button = Button(
            text="Run Command",
            size_hint = (1,0.5),
            bold = True,
            background_color = '#00FFCE'
            )
        # Linking button to callback function
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window
    
    # Callback function linked to button
    def callback(self, instance):
        self.greeting.text = "Hello " + self.user.text + "!"

# Running the App
CLI_GUI().run()