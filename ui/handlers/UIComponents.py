from ui.constants import Styles
from ui.handlers.App import App

from CTkTable import *
import customtkinter


class UIComponents():
    def __init__(self):
        self.app = App()

    def title(self, text, father_frame=None, style=None, pady=20):
        style = style or Styles.title_style
        frame = father_frame or self.app.main_frame
        title = customtkinter.CTkLabel(frame, text=text, **style)
        title.pack(pady=pady)
        return title

    def button(self, text, command, father_frame=None, pady=10, style=None):
        style = style or Styles.btn_style
        frame = father_frame or self.app.main_frame
        button = customtkinter.CTkButton(frame, text=text, command=command, **style)
        button.pack(pady=pady)
        return button

    def input_box(self, default_value="", father_frame=None, input_style=None, pady=5):
        input_style = input_style or Styles.input_style
        frame = father_frame or self.app.main_frame
        entry = customtkinter.CTkEntry(frame, **input_style)
        entry.insert(0, str(default_value))
        entry.pack(pady=pady)
        return entry

    def check_box(self, default_value=False, text="Activar", father_frame=None, pady=5):
        frame = father_frame or self.app.main_frame
        var = customtkinter.BooleanVar(value=default_value)
        checkbox = customtkinter.CTkCheckBox(frame, text=text, variable=var)
        checkbox.pack(pady=pady)
        return var, checkbox

    def frame(self, father_frame=None, width=200, height=200, pady=10):
        frame = father_frame or self.app.main_frame
        frame_widget = customtkinter.CTkFrame(frame, width=width, height=height)
        frame_widget.pack(pady=pady)
        frame_widget.pack_propagate(False)
        return frame_widget

    def table_for_dataframe(self, dataframe, father_frame=None, pady=20):
        father_frame = father_frame or self.app.main_frame
        valores = [dataframe.columns.tolist()] + dataframe.values.tolist()
        tabla = CTkTable(master=father_frame, row=len(valores), column=len(valores[0]), values=valores)
        tabla.pack(expand=True, fill="both", padx=20, pady=pady)
        return tabla
    
    def back_button(self, back_menu):
        return self.button(
            text="🔙 Tornar",
            command=back_menu,
            pady=15,
            style=Styles.back_button_style
        )
