from kivy.uix.screenmanager import Screen
from kivy_garden.graph import MeshLinePlot
from kivy.clock import Clock
import random


class RealTimeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot = MeshLinePlot(color=[0, 1, 0, 1])  # Verde para la gráfica
        self.measurement_active = True
        Clock.schedule_once(self.initialize_graph, 0)  # Inicializar después de cargar la pantalla
        Clock.schedule_interval(self.update_data, 1)  # Actualizar cada segundo

    def initialize_graph(self, dt):
        """Agregar el gráfico al inicializar."""
        if "graph" in self.ids:
            self.ids.graph.add_plot(self.plot)
        else:
            raise AttributeError("El ID 'graph' no está definido en el archivo KV.")

    def start_measurement(self):
        self.measurement_active = True

    def stop_measurement(self):
        self.measurement_active = False

    def activate_pump(self):
        print("Bomba activada manualmente")

    def deactivate_pump(self):
        print("Bomba desactivada manualmente")

    def update_data(self, dt):
        """Actualiza los datos simulados."""
        if self.measurement_active:
            # Simular datos para humedad y temperatura
            new_humidity = random.randint(20, 80)
            new_temperature = random.randint(15, 35)

            # Actualizar la gráfica
            self.plot.points.append((len(self.plot.points), new_humidity))
            if len(self.plot.points) > 100:
                self.plot.points = self.plot.points[-100:]

            # Actualizar etiquetas de texto
            self.ids.humidity_label.text = f"Humedad: {new_humidity}%"
            self.ids.temperature_label.text = f"Temperatura: {new_temperature}°C"

            # Actualizar los GaugeWidget
            if "humidity_gauge" in self.ids:
                self.ids.humidity_gauge.value = new_humidity  # Actualizar el valor del GaugeWidget de humedad
            else:
                print("El ID 'humidity_gauge' no está definido en el archivo KV.")

            if "temperature_gauge" in self.ids:
                self.ids.temperature_gauge.value = new_temperature  # Actualizar el valor del GaugeWidget de temperatura
            else:
                print("El ID 'temperature_gauge' no está definido en el archivo KV.")

            # Simular el nivel del tanque de agua
            water_level = random.randint(10, 90)
            self.ids.water_level.value = water_level
            self.ids.water_label.text = f"Nivel del tanque: {water_level}%"

            #Pybluez o bleak para envío de datos por BLE
