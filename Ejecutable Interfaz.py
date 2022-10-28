from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from Base_de_datos.usuarios.Base_de_datosUsr import *
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen


# Tama;o de ventana:
Window.size = (850, 300)

class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args, **kwargs):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args, **kwargs)
        return super(ShowcaseScreen, self).add_widget(*args, **kwargs)
class LoginApp(MDApp):
    dialog = None

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.accent_palette = 'Indigo'

        self.screens = {}
        self.available_screens = sorted(['MainAdminScreen'])

        return Builder.load_file(filename ="Pantallas/login.kv")

    def login(self):
        user_identificacion = self.root.ids.user.text
        verificador_base = Filtrar("usuario", f"{user_identificacion}")
        user_password = self.root.ids.password.text

        if len(verificador_base) == 1:
            verificador_base = verificador_base[0]
            if verificador_base[5] == user_password:
                self.dialog = MDDialog(
                    title='Login',
                    text=f'Bienvenido, {verificador_base[1]}!',
                    # buttons = [
                    #     MDFlatButton(
                    #         text = "OK", text_color = self.theme_cls.accent_color,
                    #         on_release = self.close
                    #     ),
                    # ],
                )
            self.dialog.open()
        else:
            self.dialog = MDDialog(
                title='Login',
                text=f'Usuario o contraseña inexistentes.',
                # buttons = [
                #     MDFlatButton(
                #         text = "OK", text_color = self.theme_cls.accent_color,
                #             on_release = self.close
                #         ),
                #     ],
            )
            self.dialog.open()

    def close(self):
        self.dialog.dismiss()


LoginApp().run()