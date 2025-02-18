from kivy.uix.screenmanager import Screen
from kivy_garden.graph import MeshLinePlot
from kivy.clock import Clock, mainthread
import asyncio
import bluetooth

# Dirección MAC del ESP32 y puerto RFCOMM
BT_DEVICE_ADDRESS = "30:c6:f7:42:ed:98"  # Reemplazar con la dirección MAC real
BT_PORT = 1

class RealTimeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Definir dos gráficos para visualizar los datos de los dos sensores de humedad
        self.plot_humidity1 = MeshLinePlot(color=[0, 1, 0, 1])  # Verde para Humedad 1
        self.plot_humidity2 = MeshLinePlot(color=[0, 0, 1, 1])  # Azul para Humedad 2
        self.measurement_active = True
        self.bt_socket = None  # Socket para Bluetooth clásico
        self.loop = asyncio.get_event_loop()
        Clock.schedule_once(self.initialize_graph, 0)
        Clock.schedule_interval(self.update_graph, 1)
        self.loop.create_task(self.connect_bt())

    def initialize_graph(self, dt):
        if "graph" in self.ids:
            self.ids.graph.add_plot(self.plot_humidity1)
            self.ids.graph.add_plot(self.plot_humidity2)
        else:
            raise AttributeError("El ID 'graph' no está definido en el archivo KV.")

    async def connect_bt(self):
        try:
            self.bt_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.bt_socket.connect((BT_DEVICE_ADDRESS, BT_PORT))
            print("Conectado al ESP32 vía Bluetooth Clásico")
            self.loop.create_task(self.bt_read_loop())
        except Exception as e:
            print(f"Error de conexión Bluetooth: {e}")

    async def bt_read_loop(self):
        while True:
            try:
                # Leer datos de forma bloqueante en un hilo separado
                data = await self.loop.run_in_executor(None, self.bt_socket.recv, 1024)
                if data:
                    self.data_received(None, data)
            except Exception as e:
                print("Error en la lectura Bluetooth:", e)
            await asyncio.sleep(0.1)

    def data_received(self, sender, data):
        try:
            decoded_data = data.decode("utf-8")
            print(f"Datos recibidos: {decoded_data}")  # Para depuración
            parts = decoded_data.split(",")
            if len(parts) == 6:
                # Convertir cada parte al tipo adecuado:
                humedad1 = int(parts[0])
                humedad2 = int(parts[1])
                temperature = float(parts[2])
                humidity_air = float(parts[3])
                water_level = int(parts[4])
                relay_state = int(parts[5])
                self.update_interface(humedad1, humedad2, temperature, humidity_air, water_level, relay_state)
            else:
                print("Datos recibidos con formato incorrecto:", decoded_data)
        except Exception as e:
            print(f"Error al procesar datos Bluetooth: {e}")

    @mainthread
    def update_interface(self, humedad1, humedad2, temperature, humidity_air, water_level, relay_state):
        self.plot_humidity1.points.append((len(self.plot_humidity1.points), humedad1))
        self.plot_humidity2.points.append((len(self.plot_humidity2.points), humedad2))
        if len(self.plot_humidity1.points) > 100:
            self.plot_humidity1.points = self.plot_humidity1.points[-100:]
            self.plot_humidity2.points = self.plot_humidity2.points[-100:]
        self.ids.humidity1_label.text = f"Humedad 1: {humedad1}%"
        self.ids.humidity2_label.text = f"Humedad 2: {humedad2}%"
        self.ids.temperature_label.text = f"Temperatura: {temperature}°C"
        self.ids.humidity_air_label.text = f"Humedad aire: {humidity_air}%"
        self.ids.water_label.text = f"Nivel del tanque: {water_level}"
        self.ids.relay_label.text = "Bomba ACTIVADA" if relay_state else "Bomba APAGADA"
        self.ids.humidity1_gauge.value = humedad1
        self.ids.humidity2_gauge.value = humedad2
        self.ids.temperature_gauge.value = temperature
        self.ids.humidity_air_gauge.value = humidity_air
        self.ids.water_level.value = water_level

    def update_graph(self, dt):
        pass  # La actualización se realiza en update_interface cuando se reciben datos

    def start_measurement(self):
        self.measurement_active = True

    def stop_measurement(self):
        self.measurement_active = False

    def activate_pump(self):
        print("Bomba activada manualmente")

    def deactivate_pump(self):
        print("Bomba desactivada manualmente")
