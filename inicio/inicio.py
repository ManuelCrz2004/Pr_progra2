from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from pymongo import MongoClient

Builder.load_file('inicio/inicio.kv')

class VentanaInicio(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validacion_usuario(self):
        client = MongoClient()
        db = client.facturacion
        users = db.users

        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info

        uname = user.text
        passw = pwd.text

        user.text = ''
        pwd.text = ''

        if uname == '' or passw == '':
            info.text = '[color=#FF0000]Por favor complete todos los campos[/color]'
        else:
            user = users.find_one({'user_name':uname})

            if user == None:
                info.text = '[color=#FF0000]Usuario o contraseña inválidos[/color]'
            else:
                if passw == user['password']:
                    des = user['designation']
                    info.text = ''
                    self.parent.parent.parent\
                        .ids.scrn_op.children[0]\
                            .ids.loggedin_user.text = uname
                    if des == 'Administrator':
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.current = 'scrn_op'
                else:
                    info.text = '[color=#FF0000]Usuario o contraseña inválidos[/color]'


class SigninApp(App):
    def build(self):
        return VentanaInicio()

if __name__=="__main__":
    sa = SigninApp()
    sa.run()