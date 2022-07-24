# import dearpygui.dearpygui as dpg
# import CLI

# # REQUIRED
# dpg.create_context()
# dpg.create_viewport(title="NUFT Command Line Interface", width=800, height=600)

# def button_callback(sender, app_data, user_data):
#     # print(f"sender is: {sender}")
#     # print(f"app_data is: {app_data}")
#     # print(f"user_data is: {user_data}"
#     CLI.run(dpg.get_value("cmd"))
#     dpg.set_value("input", "")

# with dpg.value_registry():
#     dpg.add_string_value(default_value="", tag="cmd")

# with dpg.window(label="NUFT CLI", tag="Primary Window"):
#     dpg.add_text("Type command here")
#     dpg.add_input_text(label="Command", default_value="", source="cmd", tag="input")
#     dpg.add_button(label="run", callback=button_callback, tag="btn")

# with dpg.window(label="Tutorial", pos=(50,50)):
#     pass

# dpg.set_primary_window("Primary Window", True)

# CLI.run("stop")
# # REQUIRED 
# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()

# """
# * Pizza delivery prompt example
# * run example by writing `python example/pizza.py` in your console
# """
# from __future__ import print_function, unicode_literals

# import regex
# from pprint import pprint

# from prompt_toolkit.validation import Validator, ValidationError

# from PyInquirer import prompt

# from examples import custom_style_3


# class PhoneNumberValidator(Validator):
#     def validate(self, document):
#         ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
#         if not ok:
#             raise ValidationError(
#                 message='Please enter a valid phone number',
#                 cursor_position=len(document.text))  # Move cursor to end


# class NumberValidator(Validator):
#     def validate(self, document):
#         try:
#             int(document.text)
#         except ValueError:
#             raise ValidationError(
#                 message='Please enter a number',
#                 cursor_position=len(document.text))  # Move cursor to end


# print('Hi, welcome to Python Pizza')

# questions = [
#     {
#         'type': 'confirm',
#         'name': 'toBeDelivered',
#         'message': 'Is this for delivery?',
#         'default': False
#     },
#     {
#         'type': 'input',
#         'name': 'phone',
#         'message': 'What\'s your phone number?',
#         'validate': PhoneNumberValidator
#     },
#     {
#         'type': 'list',
#         'name': 'size',
#         'message': 'What size do you need?',
#         'choices': ['Large', 'Medium', 'Small'],
#         'filter': lambda val: val.lower()
#     },
#     {
#         'type': 'input',
#         'name': 'quantity',
#         'message': 'How many do you need?',
#         'validate': NumberValidator,
#         'filter': lambda val: int(val)
#     },
#     {
#         'type': 'expand',
#         'name': 'toppings',
#         'message': 'What about the toppings?',
#         'choices': [
#             {
#                 'key': 'p',
#                 'name': 'Pepperoni and cheese',
#                 'value': 'PepperoniCheese'
#             },
#             {
#                 'key': 'a',
#                 'name': 'All dressed',
#                 'value': 'alldressed'
#             },
#             {
#                 'key': 'w',
#                 'name': 'Hawaiian',
#                 'value': 'hawaiian'
#             }
#         ]
#     },
#     {
#         'type': 'rawlist',
#         'name': 'beverage',
#         'message': 'You also get a free 2L beverage',
#         'choices': ['Pepsi', '7up', 'Coke']
#     },
#     {
#         'type': 'input',
#         'name': 'comments',
#         'message': 'Any comments on your purchase experience?',
#         'default': 'Nope, all good!'
#     },
#     {
#         'type': 'list',
#         'name': 'prize',
#         'message': 'For leaving a comment, you get a freebie',
#         'choices': ['cake', 'fries'],
#         'when': lambda answers: answers['comments'] != 'Nope, all good!'
#     }
# ]

# answers = prompt(questions, style=custom_style_3)
# print('Order receipt:')
# pprint(answers)


import sys
 
from tkinter import *
 
def TimesTable():
    print("\n")
    result = "Result"
    for x in range(1,13):
        m = int(EnterTable.get())
        print('\t\t', (x), ' x ',(m), ' = ', (x * m),)
        result = result + '\t\t' + str(x) + ' x ' + str(m)+  ' = ' + str(x * m) + "\n"
    result=Label(Multiply, text=result, justify='left').grid(row=9, column=6)
 
 
Multiply = Tk()
Multiply.geometry('250x500+700+200')
Multiply.title('Multiplication Table')
 
EnterTable = StringVar()
 
label1=Label(Multiply, text='Multiplication Times Table', font=30, fg='Black').grid(row=1, column=6)
label1=Label(Multiply,text='                                         ').grid(row=2,column=6)
entry5=Entry(Multiply, textvariable=EnterTable, justify='center').grid(row=3, column=6)
label1=Label(Multiply,text='                                         ').grid(row=4,column=6)            
 
button1=Button(Multiply, text='Times Table', command=TimesTable).grid(row=5,column=6)
label1=Label(Multiply,text='                                         ').grid(row=6,column=6)        
QUIT=Button(Multiply,text='Quit', fg='Red', command=Multiply.destroy).grid(row=7,column=6)
label1=Label(Multiply,text='                                         ').grid(row=8,column=6)        
result=Label(Multiply, text="Show result by insert a value", justify='left').grid(row=9, column=6)
label1=Label(Multiply,text='                                         ').grid(row=10,column=6)        
 
 
Multiply.mainloop()
