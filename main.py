from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from realtime_screen import RealTimeScreen
from historical_screen import HistoricalScreen
from gauge_widget import GaugeWidget

# Cargar el archivo KV
Builder.load_file("soilscope.kv")

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        print("Cargando pantallas...")
        sm.add_widget(RealTimeScreen(name="real_time"))
        sm.add_widget(HistoricalScreen(name="historical"))
        return sm

if __name__ == "__main__":
    MainApp().run()
