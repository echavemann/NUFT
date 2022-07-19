import dearpygui.dearpygui as dpg
import CLI

dpg.create_context()
dpg.create_viewport(title="NUFT Command Line Interface", width=800, height=600)

def button_callback(sender, app_data, user_data):
    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")

with dpg.window(label="Tutorial"):
    # user data and callback set when button is created
    dpg.add_button(label="Apply", callback=button_callback, user_data="Some Data")

    # user data and callback set any time after button has been created
    btn = dpg.add_button(label="Apply 2", )
    dpg.set_item_callback(btn, button_callback)
    dpg.set_item_user_data(btn, "Some Extra User Data")

with dpg.window(label="NUFT CLI", tag="Primary Window"):
    dpg.add_text("Type command here")
    dpg.add_input_text(label="Command", default_value="")
    dpg.add_button(label="run")
    

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()





