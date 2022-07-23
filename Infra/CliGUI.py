import dearpygui.dearpygui as dpg
import CLI

# REQUIRED
dpg.create_context()
dpg.create_viewport(title="NUFT Command Line Interface", width=800, height=600)

def button_callback(sender, app_data, user_data):
    # print(f"sender is: {sender}")
    # print(f"app_data is: {app_data}")
    # print(f"user_data is: {user_data}"
    CLI.run(dpg.get_value("cmd"))
    dpg.set_value("input", "")

with dpg.value_registry():
    dpg.add_string_value(default_value="", tag="cmd")

with dpg.window(label="NUFT CLI", tag="Primary Window"):
    dpg.add_text("Type command here")
    dpg.add_input_text(label="Command", default_value="", source="cmd", tag="input")
    dpg.add_button(label="run", callback=button_callback, tag="btn")

with dpg.window(label="Tutorial", pos=(50,50)):
    pass

dpg.set_primary_window("Primary Window", True)

CLI.run("stop")
# REQUIRED 
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()





