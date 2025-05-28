from ui.constants import Styles
from ui.handlers.App import App

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CTkTable import *
import customtkinter


class UIComponents():
    def __init__(self):
        self.app = App()

    def title(self, text, parent=None, style=None, pady=20):
        style = style or Styles.title_style
        frame = parent or self.app.main_frame
        title = customtkinter.CTkLabel(frame, text=text, **style)
        title.pack(pady=pady)
        return title

    def button(self, text, command, parent=None, pady=10, style=None):
        style = style or Styles.btn_style
        frame = parent or self.app.main_frame
        button = customtkinter.CTkButton(frame, text=text, command=command, **style)
        button.pack(pady=pady)
        return button

    def input_box(self, default_value="", parent=None, input_style=None, pady=5):
        input_style = input_style or Styles.input_style
        frame = parent or self.app.main_frame
        entry = customtkinter.CTkEntry(frame, **input_style)
        entry.insert(0, str(default_value))
        entry.pack(pady=pady)
        return entry

    def check_box(self, default_value=False, text="Activar", parent=None, pady=5):
        frame = parent or self.app.main_frame
        var = customtkinter.BooleanVar(value=default_value)
        checkbox = customtkinter.CTkCheckBox(frame, text=text, variable=var)
        checkbox.pack(pady=pady)
        return var, checkbox

    def frame(self, parent=None, width=200, height=200, pady=10):
        frame = parent or self.app.main_frame
        frame_widget = customtkinter.CTkFrame(frame, width=width, height=height)
        frame_widget.pack(pady=pady)
        frame_widget.pack_propagate(True)
        return frame_widget

    def table_for_dataframe(self, dataframe, parent=None, pady=20):
        parent = parent or self.app.main_frame
        valores = [dataframe.columns.tolist()] + dataframe.values.tolist()
        tabla = CTkTable(master=parent, row=len(valores), column=len(valores[0]), values=valores)
        tabla.pack(expand=True, fill="both", padx=20, pady=pady)
        return tabla
    
    def plot(self, figure, parent=None):
        parent = parent or self.app.main_frame
        canvas = FigureCanvasTkAgg(figure, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
    
    def back_button(self, back_menu):
        return self.button(
            text="🔙 Tornar",
            command=back_menu,
            pady=15,
            style=Styles.back_button_style
        )
