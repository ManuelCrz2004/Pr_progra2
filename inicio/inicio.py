'''
Este archivo tiene como finalidad ser el que construya la ventana que le permita
al usuario hacer el proceso de sign in, es decir, poder ingresar sus credenciales y acceder al programa.
'''

# Se importan los modulos de las subcarpetas correspondientes de la librería Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
# Se importan el módulo correspondiente de la librería pymongo
from pymongo import MongoClient

# Se usa la función Builder de la librería Kivy para invocar el archivo de kivy que contiene el código con el diseño
# de la ventana de inicio
Builder.load_file('inicio/inicio.kv')


class VentanaInicio(BoxLayout):
    # Representa la ventana que le permita al usuario hacer el proceso de sign in, esta se hereda de la clase
    # BoxLayout que proviene de la librería Kivy

    def __init__(self, **kwargs):
        # el método __init__ se construye mediante herencia alterada
        # Args método constructor:
        # **kwargs: Es un párametro que permite pasar argumentos cuya longitud varía
        super().__init__(**kwargs)

    def validacion_usuario(self):
        # Este método tiene como fin crear el proceso donde el usuario pueda ingresar sus credenciales y que estas se
        # puedan validar.

        # Lo que retorna es condicionado por las credenciales que el usuario ingrese, las opciones que puede retornar
        # son:(mas adelante se explicará esto a fondo) 1. Un campo que contenga el mensaje de "Usuario o contraseña
        # inválidos". 2. Cambie a la ventana del modo administrador. 3. Cambie a la ventana del modo cajero.

        client = MongoClient()  # client es una variable que construye un objeto de la clase MongoClient de la
        # librería pymongo
        db = client.facturacion  # db será la variable que invoca el párametro facturación del objeto client
        users = db.users  # users es la variable que guardará la base de datos de los usuarios

        # A continuación, se construiran variables que contienen los campos donde se ingresa la información de las
        # credenciales del usuario
        user = self.ids.username_field  # Campo donde se ingresa el nombre de usuario
        pwd = self.ids.pwd_field  # Campo donde se ingresa la contraseña del usuario
        # Esta variable es el campo que contenga el mensaje si las credenciales se invalidan
        info = self.ids.info

        # En acto seguido, se crean variables que guardan el texto que contiene los campos de nombre de usuario y
        # contraseña
        uname = user.text
        passw = pwd.text

        # Se declaran los textos de los campos de nombre de usuario y contraseña como strings vacíos para que no
        # hayan valores preestablecidos en estos campos.
        user.text = ''
        pwd.text = ''

        # Se crean condicionales para saber que opción debe retornar este método de acuerdo a las credenciales
        # ingresadas por el usuario

        # El primer condicional examina si los campos estan vacíos o no
        if uname == '' or passw == '':
            info.text = '[color=#FF0000]Por favor complete todos los campos[/color]'  # Si estan vacíos, aparecerá el
            # campo text con el siguiente mensaje
        else:
            user = users.find_one({
                'user_name': uname})  # Si no estan vacíos, se crea una variable donde se
            # invocará el método find_one que busca dentro de los datos guardados en users el diccionario con clave
            # user_name y el valor ingresado en el campo de nombre de usuario

            # A partir del primer condicional, se establece el siguiente que mira si el nombre de usuario existe en
            # la base datos
            if user == None:  # Esto quiere decir que no existe en la base de datos
                info.text = '[color=#FF0000]Usuario o contraseña inválidos[/color]'  # Si no esta el nombre de
                # usuario en la base de datos, aparecerá el campo text con el siguiente mensaje
            else:
                # Se crea otro condicional que examina si la contraseña insertada corresponde con el nombre de
                # usuario dado.
                if passw == user['password']:  # Es decor si el texto insertado en el campo de la contraseña coincida
                    # con el valor
                    # que este con la clave password del nombre de usuario

                    des = user[
                        'designation']  # Se guarda en una variable el valor que corresponde a la clave designation
                    # del nombre de usuario insertado, es decir, el rol del usuario
                    info.text = ''  # No se imprime ningun mensaje en este campo
                    # En la siguiente linea, se invocan tres métodos de la clase heredada BoxLayout, estas se separan
                    # mediante un "\". El conjunto de estas indican cual ventana tiene que ser mostrada. Nota:El
                    # orden para leer esta linea es de derecha a izquierda 1).ids.loggedin_user es una variable input
                    # presente en inicio.kv que guarda la información acerca del procedimiento del proceso signin del
                    # usuario 2).ids.scrn_op.children[0] invoca la clase de kivy Children para que tome la pantalla
                    # scrn_op como secundaria. Se le pone indice 0 porque scrn_op solo contiene una pantalla. La
                    # información de la variable anterior se entrega a esta pantalla. 3)self.parent.parent.parent: La
                    # función recursiva parent indica que la pantalla inicial se encuentra en el archivo "inicio.kv".
                    # Como en este método se invocan tres pantallas (inicio, admin y cajero), se invoca este método
                    # tres veces.

                    self.parent.parent.parent \
                        .ids.scrn_op.children[0] \
                        .ids.loggedin_user.text = uname

                    # Teniendo en cuenta que la contraseña coincida con el nombre de usuario, se crea el condicional
                    # según el rol del usuario
                    if des == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'  # Si el rol del usuario es administrador,
                        # se ingresa a la ventana del administrador
                    else:
                        self.parent.parent.current = 'scrn_op'  # Si el rol del usuario es cajero, se ingresa a la
                        # ventana del cajero

                else:
                    info.text = '[color=#FF0000]Usuario o contraseña inválidos[/color]'  # Si la contraseña no
                    # coincide con el nombre de usuario, aparecerá el campo text con el siguiente mensaje


class SigninApp(App):
    # Representa la construcción de la ventana de inicio, es decir, la de sign in
    def build(self):
        # Este tiene como proposito construir la ventana de inicio

        return VentanaInicio()  # retorna un objeto de la clase VentanaInicio


# Aqui se puede correr el programa
if __name__ == "__main__":
    sa = SigninApp()
    sa.run()
