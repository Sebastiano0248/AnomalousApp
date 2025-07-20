from ui.Menu import Menu
from anomalouslib.models.testing_utils import predict_continuous, predict_discrete
from anomalouslib.data.preprocessing import generate_regressor_tensors, generate_classification_tensors
from anomalouslib.utils.load_save_like import load_from_pickle, save_to_csv
from anomalouslib.models.model_handler import load_model
from ui.constants import Styles
from anomalouslib.analysis.DataAnalyzer import DataAnalyzer
from anomalouslib.analysis.ModelAnalyzer import ModelAnalyzer


import pandas as pd
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ModelMenu(Menu):
    def __init__(self, back_menu):
        super().__init__()

        # Variables globals
        self.back_menu = back_menu

        # Variables del model
        self.dataset = None
        self.model = None
        self.le = None

        # Paths
        self.data_dir = self.load_param("path", "dataset>undefined")
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
            lambda: self.show_plot(
                lambda: da.mostrar_trajectories(draw=False),
                lambda: self.show_statistical_analysis(dataset)
            ),
            pady=10
        )

        self.ui.button(
            "📉 Evolució Temporal",
            lambda: self.show_plot(
                lambda: da.mostrar_evolucio(draw=False),
                lambda: self.show_statistical_analysis(dataset)
            ),
            pady=10
        )

        self.ui.button(
            "📊 Histograma 3D",
            lambda: self.show_plot(
                lambda: da.mostrar_histograma(draw=False),
                lambda: self.show_statistical_analysis(dataset)
            ),
            pady=10
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
        if isinstance(model, tuple):
            self.model = model[0]
            self.le = model[1]
        else:
            self.model = model
            self.le = None
        params = list(self.dataset["attributes"].iloc[0].keys())
        self.trajectory_type = self.dataset["attributes"].iloc[0]["trajectory_type"]
        if len(params) > 1:
            self.clear_frame()
            self.app.title("Paràmetres del Model")
            self.ui.title("📊 Paràmetres del Model")

            self.ui.title(
                text="Selecciona el paràmetre a inferir",
                style=Styles.subtitle_style,
                pady=10
            )

            for param in params:
                self.ui.button(
                    param.capitalize(),
                    lambda p=param: self.select_analysis(self.model, p),
                    pady=10
                )
        else:
            self.param = params[0]
            self.select_analysis(model, self.param)
            return

        self.ui.back_button(lambda: self.show_model_list(self.dataset))

    def select_analysis(self, model, param, le=None):
        self.param = param

        ma = ModelAnalyzer(self.dataset)
        self.clear_frame()
        self.ui.title("📊 Anàlisi del Model")

        self.ui.button(
            "📈 Inferència",
            lambda: self.show_results(),
            pady=10
        )
        
        if self.le is not None:
            self.ui.button(
                "📊 Patrons de Trajectòria Discreta",
                lambda: self.show_plot(
                    lambda: ma.analyze_discrete_trajectory_patterns(self.model, self.param, self.le, draw=False),
                    lambda: self.select_analysis(self.model, self.param, self.le)
                ),
                pady=10
            )
        else:
            self.ui.button(
                "📊 Patrons de Trajectòria Contínua",
                lambda: self.show_plot(
                    lambda: ma.analyze_continuous_trajectory_patterns(self.model, self.param, draw=False),
                    lambda: self.select_analysis(self.model, self.param)
                ),
                pady=10
            )

        self.ui.back_button(lambda: self.show_model_list(self.dataset))
    
    def show_results(self):

        def predict_discrete_probabilities(model, X_input, y_input=None, le=None, num_samples=None, to_print=True):
            import torch
            """
            Predice clases discretas a partir de probabilidades.
            Añade columna 'real_type' con los valores de y_input (decodificados si le está presente).
            """
            if num_samples is not None:
                X_input = X_input[:num_samples]
            if y_input is not None:

                y_input = y_input[:num_samples]

            self.model.eval()
            with torch.no_grad():
                output = self.model(X_input)
                probabilities = output.cpu().numpy()
                predicted_indices = probabilities.argmax(axis=1)

            results = {}
            if le is not None:
                predicted_labels = le.inverse_transform(predicted_indices)
                results['Predicted Label'] = predicted_labels
            else:
                results['Predicted Label'] = predicted_indices

            # Añadir columna real_type
            if y_input is not None:
                if le is not None:
                    y_numpy = y_input.cpu().numpy()
                    predicted_class_indices = np.argmax(y_numpy, axis=1)
                    real_types = le.inverse_transform(predicted_class_indices)
                else:
                    real_types = y_input.cpu().numpy()
                results['real_type'] = real_types

            df = pd.DataFrame(results)

            if to_print:
                print("Predicciones:")
                for i, row in df.iterrows():
                    if 'real_type' in df.columns:
                        print(f"Ejemplo {i+1}: Predicho = {row['Predicted Label']}, Real = {row['real_type']}")
                    else:
                        print(f"Ejemplo {i+1}: Predicho = {row['Predicted Label']}")

            return df
        
        lentgh = len(self.dataset)
        if self.le is not None:
            x, y = generate_classification_tensors(self.dataset, self.param, self.le)
            results = predict_discrete_probabilities(self.model, x, y, self.le, to_print=False)
        else:
            x, y = generate_regressor_tensors(self.dataset, self.trajectory_type, self.param)
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
        else:
            results_to_show = results

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
                    lambda: self.show_results()
                ),
            pady=10
        )

        self.ui.back_button(lambda: self.select_analysis(self.model, self.param, self.le))