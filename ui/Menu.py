from ui.handlers.UIComponents import UIComponents
from ui.handlers.App import App
from ui.constants import Styles
from pathlib import Path
import yaml
import os

class Menu:
    def __init__(self):
        super().__init__()

        # Objectes necessaris
        self.app = App()
        self.ui = UIComponents()
    
    def clear_frame(self):
        for widget in self.app.main_frame.winfo_children():
            widget.destroy()

    def load_param(self, paramType: str, keys_str: str):
        yaml_path = Path(f"ui/config/{paramType}s.yaml")
        if not yaml_path.exists():
            print(f"Directorio actual: {Path.cwd()}")
            raise FileNotFoundError(f"El archivo {yaml_path} no existe.")

        try:
            with yaml_path.open('r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error al cargar el archivo YAML: {e}")

        keys = keys_str.split('>')
        for i, key in enumerate(keys):
            if not isinstance(data, dict):
                raise ValueError(f"El dato {data} no es un diccionario, no se puede seguir navegando.")
            
            if i == len(keys) - 1:
                return data.get(key, None)  # O cualquier otro comportamiento que desees
            else: data = data.get(key)
        return data

    # Load Menu
    def show_load_menu(self, value_type_name, extension, directory, load_method, go_to, back_menu):
        self.clear_frame()
        self.app.title(f"Carregar {value_type_name.title()}")

        self.ui.title(f"📂 Carregar {value_type_name.title()}")

        # Llistar arxius a la carpeta principal
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith(extension)]
        if files:
            self.ui.title(
                text=os.path.basename(directory) or directory,
                style=Styles.subtitle_style,
                pady=5
            )
            for idx, filename in enumerate(files, 1):
                self.ui.button(
                    text=f"{idx}. {filename}",
                    command=lambda f=filename: self._load_value(f, load_method, go_to),
                    style={"width": 300},
                    pady=5
                )

        # Llistar subcarpetes i els seus arxius
        subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            sub_files = [f for f in os.listdir(subdir_path) if os.path.isfile(os.path.join(subdir_path, f)) and f.endswith(extension)]
            if sub_files:
                frame = self.ui.frame()
                self.ui.title(
                    text=subdir,
                    style=Styles.subtitle_style,
                    pady=5,
                    parent=frame
                )
                for idx, filename in enumerate(sub_files, 1):
                    path = subdir + "/" + filename
                    self.ui.button(
                        text=f"{idx}. {filename}",
                        command=lambda f=path: self._load_value(f, load_method, go_to),
                        style={"width": 300},
                        pady=5,
                        parent=frame
                    )

        if not files and not subdirs:
            self.ui.title(
                text="No s'han trobat datasets",
                style=Styles.subtitle_style,
                pady=10
            )

        self.ui.back_button(back_menu)

    def _load_value(self, filename, load_method, go_to):
        try:
            value = load_method(filename)
            go_to(value)

        except Exception as e:
            self.ui.title(
                text=f"⛔ Error: {str(e)}",
                style=Styles.subtitle_style,
                pady=10
            )

    # Save Menu
    def show_save_menu(self, value_type_name, save_method, back_menu):
        self.clear_frame()
        self.app.title(f"Desar {value_type_name.title()}")

        self.ui.title(f"💾 Desar {value_type_name.title()}")

        self.ui.title(
            text = "Nom del fitxer:",
            style = Styles.subtitle_style,
            pady = 10
        )
        self.file_name = self.ui.input_box(value_type_name)

        self.ui.button(
            "💾 Desar",
            lambda: self._save_in_a_file(value_type_name, save_method, self.file_name.get()),
            pady=15
        )

        self.ui.back_button(back_menu)
    
    def _save_in_a_file(self, value_type_name, save_method, file_name):
        try:
            save_method(file_name)

            self.ui.title(
                text=f"✅ {value_type_name.title()} guardat!",
                style=Styles.subtitle_style,
                pady=10
            )
        except Exception as e:
            self.ui.title(
                text=f"⛔ Error: {str(e)}",
                style=Styles.subtitle_style,
                pady=10
            )

    # Show Plot
    def show_plot(self, plot_method, back_menu):
        self.clear_frame()
        self.app.title("Visualització")

        self.ui.title("📊 Visualització")

        try:
            plt, fig, _ = plot_method()
            self.ui.plot(fig)
            plt.close(fig)

            def open_plot():
                plt2, fig2, _ = plot_method()
                plt2.show()
                plt2.close(fig2)

            self.ui.button(
                "Obrir gràfica",
                open_plot,
                pady=15
            )
        except Exception as e:
            self.ui.title(
                text=f"⛔ Error: {str(e)}",
                style=Styles.subtitle_style,
                pady=10
            )

        def on_back():
            back_menu()
            plt.clf()
            plt.close('all')

        self.ui.back_button(on_back)