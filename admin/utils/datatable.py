'''
Este archivo tiene como finalidad ser el que construya la tabla que organiza la información sobre los productos.
al usuario hacer el proceso de sign in, es decir, poder ingresar sus credenciales y acceder al programa.
'''

# Se importan los modulos de las subcarpetas correspondientes de la librería Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
# Se importan  el módulo correspondiente de la librería pymongo y la libreria collections
from pymongo import MongoClient
from collections import OrderedDict

# Se usa la función Builder de la librería Kivy para indicar el código con el diseño de la ventana de inicio (este
# presenta como un string)
Builder.load_string('''
<DataTable>: 
    id: main_win
    RecycleView:
        viewclass: 'CustLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')


class DataTable(BoxLayout):
    # Representa la tabla donde se disponen los datos que caracterizan a los productos

    def __init__(self, table='', **kwargs):
        # el método __init__ se construye mediante herencia alterada
        # Args método constructor:
        # **kwargs: Es un párametro que permite pasar argumentos cuya longitud varía
        # table (str): Es una cadena de caracteres vacia que va a permitir construir la tabla
        super().__init__(**kwargs)

        # products = self.get_products()
        products = table  # Variable que se le asigna el párametro table

        # A continuación, se van a construir en forma de variables, los elementos de la tabla
        # Títulos de las columnas
        col_titles = [k for k in
                      products.keys()]  # Los toma de las claves del diccionario donde estan la información de los
        # prductos, para ello se utiliza un ciclo for.
        # Número de filas
        rows_len = len(products[col_titles[
            0]])  # Se hace para averiguar cuantos filas hay que construir. Primero, se utiliza el valor que le
        # corresponde al indice 0 en la lista que guarda los nombres de las columnas, luego se asigna ese valor como
        # clave,y por ultimo, cuenta cuantos valores le corresponden a esa clave utilizando len.
        self.columns = len(col_titles)  # Se le asigna a self.columns, el número de títulos de columnas

        # En acto seguido, se construyen las columnas y las filas

        # Primero se crea una variable table_data que corresponde a una lista vacía y tiene como próposito guardar la
        # información de las filas y columnas
        table_data = []

        # Construcción de las columnas Se utiliza un ciclo for para recorrer todos los valores en la lista col_titles
        # que representan los títulos de las columnas
        for t in col_titles:
            # Se agregan los siguientes valores en forma de diccionario a la lista table_data La clave es un valor
            # str que corresponde a la caracteristica especifica de la columna y el valor que le corresponde
            # 1)"text":str(t)-- Representa al texto escrito en cada columna 2)"size_hint_y": None --Representa el
            # ancho, se le asigne a el valor None para que se pueda ajustar automaticamente según la proporción de la
            # pantalla 3)"height":50 -- Representa la altura, el valor int es la medida de la altura 4)"bcolor":(.06,
            # .45,.45,.1) -- Representa el color de la columna, el valor es una tupla que señala el color en código
            # RGBa
            table_data.append({'text': str(t), 'size_hint_y': None, 'height': 50, 'bcolor': (.06, .45, .45, 1)})

        # Construcción de las filas
        # Se utiliza un ciclo for con rango rows_len que representa el número de filas que se necesitan crear
        for r in range(rows_len):
            # Se utiliza otro ciclo for dentro para crear las filas por cada columna
            for t in col_titles:
                # Se agregan los siguientes valores en forma de diccionario a la lista table_data La clave es un
                # valor str que corresponde a la caracteristica especifica de la columna y el valor que le
                # corresponde 1)"text":str(products[t][r])-- Representa al texto escrito en cada columna,
                # se le asigna el valor que corresponde al indice del título de la columna correspondiente.
                # 2)"size_hint_y": None --Representa el ancho, se le asigne a el valor None para que se pueda ajustar
                # automaticamente según la proporción de la pantalla 3)"height":30 -- Representa la altura,
                # el valor int es la medida de la altura 4)"bcolor":(.06,.25,.25,.1) -- Representa el color de la
                # columna, el valor es una tupla que señala el color en código RGBa
                table_data.append(
                    {'text': str(products[t][r]), 'size_hint_y': None, 'height': 30, 'bcolor': (.06, .25, .25, 1)})

        # Se le asigna a estas variables creadas en el código de kivy, estos valores para que construyan las columnas
        # y la tabla
        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data

# Aqui se puede correr el programa, utilizando este código:
# class DataTableApp(App):
#     def build(self):

#         return DataTable()

# if __name__=='__main__':
#     DataTableApp().run()
