from ui.Menu import Menu
from anomalouslib.models.testing_utils import predict_continuous
from anomalouslib.data.preprocessing import generate_tensors
from anomalouslib.utils.load_save_like import load_from_pickle, save_to_csv
from anomalouslib.models.model_handler import load_model
from ui.constants import Styles
from anomalouslib.analysis.DataAnalyzer import DataAnalyzer


import pandas as pd

class ModelMenu(Menu):
    def __init__(self, back_menu):
        super().__init__()

        # Variables globals
        self.back_menu = back_menu

        # Paths
        self.data_dir = self.load_param("path", "dataset>generated")
        self.model_dir = self.load_param("path", "model")
        self.prediction = self.load_param("path", "result>prediction")

    def show_model_menu(self):
        self.show_dataset_list()
    
    def show_dataset_list(self):
        self.show_load_menu(
            "dataset", ".pkl",
            self.data_dir,
            lambda filename: load_from_pickle(self.data_dir, filename),
            self.show_analysis_menu,
            self.back_menu
        )

    def show_analysis_menu(self, dataset):
        self.clear_frame()
        self.app.title("Anàlisi del Dataset")

        self.ui.title("🔎 Anàlisi del Dataset")

        self.ui.button(
            "📊 Anàlisi Estadística",
            lambda: self.show_statistical_analysis(dataset),
            pady=10
        )
        self.ui.button(
            "🤖 Inferència amb Models",
            lambda: self.show_model_list(dataset),
            pady=10
        )

        self.ui.back_button(self.show_dataset_list)

    def show_statistical_analysis(self, dataset):
        self.clear_frame()
        self.app.title("Anàlisi")

        self.ui.title("📊 Opcions d'Anàlisi")
        da = DataAnalyzer(dataset)

        self.ui.button(
            "📈 Mostrar Trajectòries",
            lambda: da.mostrar_trajectories()
        )

        self.ui.button(
            "📉 Evolució Temporal",
            lambda: da.mostrar_evolucio()
        )

        self.ui.button(
            "📊 Histograma 3D",
            lambda: da.mostrar_histograma()
        )

        self.ui.back_button(lambda: self.show_analysis_menu(dataset))

    def show_model_list(self, dataset):
        self.dataset = dataset
        self.show_load_menu(
            "model", ".pth",
            self.model_dir,
            lambda filename: load_model(self.model_dir + filename),
            self.decide_param,
            lambda: self.show_analysis_menu(self.dataset)
        )

    def decide_param(self, model):
        self.model = model
        params = list(self.dataset["attributes"].iloc[0].keys())
        self.trajectory_type = self.dataset["attributes"].iloc[0]["trajectory_type"]
        if len(params) > 1:
            self.clear_frame()
            self.app.title("Paràmetres del Model")
            self.ui.title("📊 Paràmetres del Model")

            self.clear_frame()
            self.ui.title("📊 Paràmetres del Model")

            self.ui.title(
                text="Selecciona el paràmetre a inferir",
                style=Styles.subtitle_style,
                pady=10
            )

            for param in params:
                self.param = param
                self.ui.button(
                    self.param.capitalize(),
                    lambda: self.show_results(self.model),
                    pady=10
                )
        else:
            self.param = params[0]
            self.show_results(model)
            return

        self.ui.back_button(lambda: self.show_model_list(self.dataset))
    
    def show_results(self, model):
        self.model = model
        lentgh = len(self.dataset)
        x, y = generate_tensors(self.dataset, self.trajectory_type, self.param)
        results = predict_continuous(self.model, x, y, to_print=False)
        
        self.clear_frame()
        self.ui.title("📋 Resultats de la Inferència")
        if lentgh > 10:
            self.ui.title(
                text="Mostrant només les primeres 10 files",
                style=Styles.subtitle_style,
                pady=10
            )
            # Afegir una última fila amb punts suspensius a cada columna
            ellipsis_row = {col: "..." for col in results.columns}
            results_to_show = pd.concat([results.head(10), pd.DataFrame([ellipsis_row])], ignore_index=True)
        
        self.ui.table_for_dataframe(results_to_show, pady=20)

        self.ui.button(
            text="💾 Guardar Resultats",
            command=
                lambda: self.show_save_menu(
                    "resultat",
                    lambda filename: save_to_csv(
                        results,
                        self.prediction,
                        filename
                    ),
                    lambda: self.show_results(self.model)
                ),
            pady=10
        )

        self.ui.back_button(lambda: self.show_model_list(self.dataset))