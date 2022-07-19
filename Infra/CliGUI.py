import dearpygui.dearpygui as dpg
import CLI

dpg.create_context()
dpg.create_viewport(title="NUFT Command Line Interface", width=800, height=600)

with dpg.window(label="NUFT CLI", tag="Primary Window"):
    dpg.add_text("Sample")
    dpg.add_button(label="save")
    dpg.add_input_text(label="Command", default_value="Type Here")
    
with dpg.window(label="Window2"):
    dpg.add_text("Sample")
    dpg.add_button(label="save")
    dpg.add_input_text(label="Command", default_value="Type Here")

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()



