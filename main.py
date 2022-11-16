from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from admin.admin import Ventana_Administrador
from inicio.inicio import VentanaInicio
from cajero.cajero import OperatorWindow

class VentanaEjecutable(BoxLayout):

    admin_widget = Ventana_Administrador()
    signin_widget = VentanaInicio()
    operator_widget = OperatorWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)

class MainApp(App):
    def build(self):

        return VentanaEjecutable()

if __name__=='__main__':
    MainApp().run()