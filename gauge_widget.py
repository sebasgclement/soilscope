from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty


class GaugeWidget(Widget):
    value = NumericProperty(0)  # Valor actual del gauge (0-100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self.update_gauge)

    def update_gauge(self, *args):
        """Dibuja el gauge basado en el valor actual."""
        self.canvas.clear()
        with self.canvas:
            # Fondo del gauge (semicírculo base)
            Color(0.3, 0.3, 0.3)  # Gris oscuro
            Line(circle=(self.center_x, self.center_y, min(self.width, self.height) / 2 - 10, 0, 180), width=5)

            # Valor del gauge (parte llena)
            Color(0, 1, 0)  # Verde
            Line(circle=(self.center_x, self.center_y, min(self.width, self.height) / 2 - 10, 0, self.value * 1.8), width=10)

            # Texto del valor (si se necesita)
            # Podrías agregar más elementos visuales como etiquetas aquí.
