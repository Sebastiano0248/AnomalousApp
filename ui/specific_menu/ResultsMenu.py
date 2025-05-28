from ui.constants import Styles
from anomalouslib.data.DatasetGenerator import DatasetGenerator
from ui.Menu import Menu
from anomalouslib.utils.load_save_like import save_to_pickle

import json
import os

class ResultsMenu(Menu):
    def __init__(self, back_menu):
        super().__init__()
        
        # Paths
        self.config_dataset_generation = self.load_param("path", "cache>dataset_generation")
        self.data_dir = self.load_param("path", "dataset>undefined")
        
        # Cache
        self.default_dataset_config = self._load_default_dataset_config()

        # Variables globals
        self.back_menu = back_menu


    def _load_default_dataset_config(self):
        try:
            with open(self.config_dataset_generation) as f:
                return json.load(f)
        except:
            print("No s'ha pogut carregar la configuració. S'està creant una nova configuració per defecte.")
            return {"num_particules": 5, "num_passos": 1000, "random_params": 0}

    def show_generation_menu(self):
        self.clear_frame()
        self.app.title("Generar Dataset")

        self.ui.title("⚙️ Tipus de Trajectòria")

        config_frame = self.ui.frame(width=300, height=100)

        self.ui.title(
            "Configuració actual:",
            parent=config_frame,
            style={"font": ("Arial", 16, "bold"), "anchor": "w", "width": 100},
        ).pack(pady=(5, 0), padx=10, anchor="w")

        self.ui.title(
            text=(
                f"• Partícules: {self.default_dataset_config['num_particules']}\n"
                f"• Passos: {self.default_dataset_config['num_passos']}\n"
                f"• Paràmetres aleatoris: {'Sí' if self.default_dataset_config.get('random_params', False) else 'No'}"
            ),
            parent=config_frame,
            style={"font": ("Arial", 14), "anchor": "w", "justify": "left", "width": 100},
        ).pack(pady=(0, 5), padx=20, anchor="w")
        
        # Botó de configuració
        self.ui.button(
            "⚙️ Configurar paràmetres",
            self.show_config_menu
        )

        # Tipos de trayectorias
        trajectories = [
            ("🚶 Random Walk", "generate_RandomWalk"),
            ("📈 Brownian Motion", "generate_BrownianMotion"),
            ("⏱️ CTRW", "generate_ContinuousTimeRandomWalk"),
            ("📉 FBM", "generate_FractionalBrownianMotion"),
            ("🌀 Lévy Walks", "generate_LevyWalks"),
            ("🔄 ATTM", "generate_AnnealedTransitTimeModel"),
            ("📏 SBM", "generate_ScaledBrownianMotion")
        ]
        
        for text, method in trajectories:
            self.ui.button(
                text=text, pady=5,
                command=lambda m=method: self._generate_dataset(m),
            )
        
        self.ui.back_button(self.back_menu)

    def show_config_menu(self):
        self.clear_frame()
        self.app.title("Configuració")
        
        self.ui.title("⚙️ Configuració de Paràmetres", pady=20)

        self.ui.title(
            text="Nombre de partícules:",
            style=Styles.subtitle_style,
            pady=10
        )
        self.num_particules = self.ui.input_box(
            self.default_dataset_config["num_particules"]
        )

        self.ui.title(
            text="Nombre de passos:",
            style=Styles.subtitle_style,
            pady=10
        )
        self.num_passos = self.ui.input_box(
            self.default_dataset_config["num_passos"]
        )

        self.ui.title(
            text="Paràmetres aleatoris:",
            style=Styles.subtitle_style,
            pady=10
        )

        _, self.random_params = self.ui.check_box(
            self.default_dataset_config["random_params"]
        )
        
        self.ui.button(
            "💾 Guardar Configuració",
            self._save_config,
            pady=15
        )
        
        self.ui.back_button(self.show_generation_menu)

    def _save_config(self):
        try:
            # Actualitzar la variable de configuració
            self.default_dataset_config["num_particules"] = int(self.num_particules.get())
            self.default_dataset_config["num_passos"] = int(self.num_passos.get())
            self.default_dataset_config["random_params"] = int(self.random_params.get())

            config = {
                "num_particules": int(self.num_particules.get()),
                "num_passos": int(self.num_passos.get()),
                "random_params": int(self.random_params.get())
            }
            os.makedirs("config", exist_ok=True)
            with open(self.config_dataset_generation, "w") as f:
                json.dump(config, f)
            self.show_generation_menu()
        except ValueError:
            self.ui.title(
                text=f"⛔ Valors no vàlids!",
                style=Styles.subtitle_style,
                pady=10
            )
        
    def _generate_dataset(self, method_name):
        generator = DatasetGenerator(self.default_dataset_config["num_particules"])   
        try:
            method = getattr(generator, method_name)
            dataset = method(
                num_passos = self.default_dataset_config["num_passos"],
                random_params = self.default_dataset_config["random_params"]
            )
            self.show_save_menu(
                "dataset",
                lambda name: save_to_pickle(dataset, self.data_dir, name),
                self.show_generation_menu
            )
        except Exception as e:
            self.ui.title(
                text=f"⛔ Error: {str(e)}",
                style=Styles.subtitle_style,
                pady=10
            )