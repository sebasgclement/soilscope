from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import json

class HistoricalScreen(Screen):
    def on_enter(self):
        """Carga los datos desde el JSON y llena el carrusel de imágenes."""
        # Cargar datos desde el JSON
        with open("resources/data.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.cultivos = data["cultivos"]

        # Limpiar el carrusel de imágenes
        self.ids.carrusel_plantas.clear_widgets()

        # Ajustar altura del GridLayout en función del número de imágenes
        self.ids.carrusel_plantas.height = len(self.cultivos) * 110  # Altura suficiente

        # Agregar imágenes al carrusel como fondo de botones
        for cultivo in self.cultivos:
            btn = Button(
                size_hint_y=None, height=100,  
                background_normal=cultivo["imagen"],  # Fondo del botón con la imagen
                background_down=cultivo["imagen"],  # Mantener la imagen al presionar
            )

            # Enlazar el botón con la función para mostrar detalles del cultivo correspondiente
            btn.bind(on_release=lambda instance, c=cultivo: self.mostrar_detalles(c))

            # Agregar el botón al carrusel
            self.ids.carrusel_plantas.add_widget(btn)

        # Mostrar detalles del primer cultivo
        if self.cultivos:
            self.mostrar_detalles(self.cultivos[0])

    def mostrar_detalles(self, cultivo):
        """Actualizar la imagen, la descripción y los valores del cultivo seleccionado."""
        self.ids.imagen_cultivo.source = cultivo["imagen"]
        self.ids.descripcion.text = cultivo["descripcion"]
        self.ids.temp_ambiente.text = f"Temp. Ambiente: {cultivo['temp_ambiente_max']} - {cultivo['temp_ambiente_min']} °C"
        self.ids.humedad_ambiente.text = f"Humedad Ambiente: {cultivo['humedad_ambiente_max']} - {cultivo['humedad_ambiente_min']} %"
        self.ids.humedad_suelo.text = f"Humedad Suelo: {cultivo['humedad_suelo_max']} - {cultivo['humedad_suelo_min']} %"
