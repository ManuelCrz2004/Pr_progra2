'''
Este archivo tiene como finalidad ser el que establezca el menú principal para el usuario, es decir, que abra la pantalla de signin.
Por eso es el ejecutable para la interfaz gráfica.
'''
#Se importan los modulos de las subcarpetas correspondientes
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from admin.admin import Ventana_Administrador
from inicio.inicio import VentanaInicio
from cajero.cajero import OperatorWindow

class VentanaEjecutable(BoxLayout):
    #Representa la ventana que abre el programa en el menú principal, esta se hereda de la clase BoxLayout que proviene de la librería Kivy
    #Se asignan las variables de clase, de acuerdo a las ventanas de los menus de cada rol
    admin_widget = Ventana_Administrador()
    signin_widget = VentanaInicio()
    operator_widget = OperatorWindow()
   #el método __init__ se constuye mediante herencia alterada
   #Args método constructor:
   #**kwargs: Es un párametro que permite pasar argumentos cuya longitud varía
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Por cada uno de los screens se le agregan las variables de clase como widgets para construir las ventanas de cada menu
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)

class MainApp(App):
    #Representa la construcción de todas las ventanas
    def build(self):
        #Este  método retorna la ventana ejecutable
        return VentanaEjecutable()
#Aqui se puede correr el programa
if __name__=='__main__':
    MainApp().run()