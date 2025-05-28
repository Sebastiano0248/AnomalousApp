from ui.Menu import Menu
from ui.specific_menu.GenerationMenu import GenerationMenu
from ui.specific_menu.ModelMenu import ModelMenu


class MainMenu(Menu):
    def __init__(self):
        super().__init__()

        # objectes necessaris
        self.gm = GenerationMenu(self.show_main_menu)
        self.mm = ModelMenu(self.show_main_menu)

        self.show_main_menu()

        self.app.mainloop()

    def show_main_menu(self):
        self.clear_frame()
        self.app.title("Menú Principal")

        self.ui.title("🌟 Menú Principal 🌟")

        self.ui.button(
            "✨ Generar dataset",
            self.gm.show_generation_menu
        )
        self.ui.button(
            "🚀 Interpretar dataset",
            self.mm.show_model_menu
        )

        self.ui.button("❌ Sortir", self.app.quit)

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
    
