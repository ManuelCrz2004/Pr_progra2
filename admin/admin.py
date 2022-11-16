from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

from collections import OrderedDict
from pymongo import MongoClient
from utils.datatable import DataTable
from datetime import datetime

Builder.load_file('admin/admin.kv')


class Notificaciones(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7, .7)


class Ventana_Administrador(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db = client.facturacion
        self.users = db.users
        self.products = db.inventario
        self.notify = Notificaciones()

        codigo_del_producto = []
        nombre_producto = []
        spinvals = []

        for product in self.products.find():
            codigo_del_producto.append(product['product_code'])
            nombre = product['product_name']
            if len(nombre) > 30:
                nombre_largo = nombre[:30] + '...'
            nombre_producto.append(nombre)

        for x in range(len(codigo_del_producto)):
            line = ' | '.join([codigo_del_producto[x], nombre_producto[x]])
            spinvals.append(line)
        self.ids.target_product.values = spinvals

        content = self.ids.contenido_pantallas
        users = self.tabla_usuarios()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        # Display Products
        product_scrn = self.ids.scrn_product_contents
        products = self.almacenamiento_productos()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

    def agregar_campos_usr(self):
        target = self.ids.campos_operacion_usuario
        target.clear_widgets()
        campo_agregar_n = TextInput(hint_text='Nombre', multiline=False)
        campo_agergar_a = TextInput(hint_text='Apellido', multiline=False)
        campo_agregar_u = TextInput(hint_text='Usuario', multiline=False)
        campo_c = TextInput(hint_text='Contraseña', multiline=False)
        campo_roles = Spinner(text='Rol', values=['Cajero', 'Administrador'])
        campo_submit = Button(text='Agregar', size_hint_x=None, width=100,
                              on_release=lambda x: self.agregar_usr(campo_agregar_n.text, campo_agergar_a.text,
                                                                    campo_agregar_u.text, campo_c.text,
                                                                    campo_roles.text))

        target.add_widget(campo_agregar_n)
        target.add_widget(campo_agergar_a)
        target.add_widget(campo_agregar_u)
        target.add_widget(campo_c)
        target.add_widget(campo_roles)
        target.add_widget(campo_submit)

    def agregar_usr(self, nombre, apellido, user, pwd, rol):

        if nombre == '' or apellido == '' or user == '' or pwd == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Por Favor llene todos los campos[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.users.insert_one({'first_name': nombre, 'last_name': apellido,
                                   'user_name': user, 'password': pwd, 'designation': rol})
            content = self.ids.contenido_pantallas
            content.clear_widgets()

            users = self.tabla_usuarios()
            userstable = DataTable(table=users)
            content.add_widget(userstable)

    def actualizar_usr_campos(self):
        target = self.ids.campos_operacion_usuario
        target.clear_widgets()
        campo_actualizar_n = TextInput(hint_text='Nombre', multiline=False)
        campo_actualizar_a = TextInput(hint_text='Apellido', multiline=False)
        campo_actualizar_u = TextInput(hint_text='Usuario', multiline=False)
        campo_actualizar_pwd = TextInput(hint_text='Contraseña', multiline=False)
        campo_actualizar_rol = Spinner(text='Rol', values=['Cajero', 'Administrador'])
        update = Button(text='Actualizar', size_hint_x=None, width=100,
                        on_release=lambda x: self.actualizar_usr(campo_actualizar_n.text, campo_actualizar_a.text,
                                                                 campo_actualizar_u.text, campo_actualizar_pwd.text,
                                                                 campo_actualizar_rol.text))

        target.add_widget(campo_actualizar_n)
        target.add_widget(campo_actualizar_a)
        target.add_widget(campo_actualizar_u)
        target.add_widget(campo_actualizar_pwd)
        target.add_widget(campo_actualizar_rol)
        target.add_widget(update)

    def actualizar_usr(self, first, last, user, pwd, des):

        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            user = self.users.find_one({'user_name': user})
            if user == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Username[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 1)
            else:
                if first == '':
                    first = user['first_name']
                if last == '':
                    last = user['last_name']
                if pwd == '':
                    pwd = user['password']
                self.users.update_one({'user_name': user}, {
                    '$set': {'first_name': first, 'last_name': last, 'user_name': user, 'password': pwd,
                             'designation': des, 'date': datetime.now()}})
                content = self.ids.contenido_pantallas
                content.clear_widgets()

                users = self.tabla_usuarios()
                userstable = DataTable(table=users)
                content.add_widget(userstable)

    def tabla_usuarios(self):
        client = MongoClient()
        db = client.facturacion
        users = db.users
        _users = OrderedDict()
        _users['Nombres'] = {}
        _users['Apellidos'] = {}
        _users['Nombre de usuario'] = {}
        _users['Contraseñas'] = {}
        _users['Rol'] = {}

        Nombres = []
        Apellidos = []
        user_names = []
        passwords = []
        Rol = []

        for user in users.find():
            Nombres.append(user['first_name'])
            Apellidos.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd = user['password']
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            Rol.append(user['designation'])

        users_length = len(Nombres)
        idx = 0

        while idx < users_length:
            _users['Nombres'][idx] = Nombres[idx]
            _users['Apellidos'][idx] = Apellidos[idx]
            _users['Nombre de usuario'][idx] = user_names[idx]
            _users['Contraseñas'][idx] = passwords[idx]
            _users['Rol'][idx] = Rol[idx]

            idx += 1

        return _users

    def remover_usr_campo(self):
        target = self.ids.campos_operacion_usuario
        target.clear_widgets()
        input_remover_u = TextInput(hint_text='Usuario a remover')
        remover = Button(text='Remover', size_hint_x=None, width=100,
                         on_release=lambda x: self.remover_usr(input_remover_u.text))

        target.add_widget(input_remover_u)
        target.add_widget(remover)

    def agregar_producto(self, codigo, nombre, peso, inventario, venta, ordenado, comprado):

        if codigo == '' or nombre == '' or peso == '' or inventario == '' or ordenado == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Por favor llene los campos obligatorios[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.products.insert_one(
                {'product_code': codigo, 'product_name': nombre, 'product_weight': peso, 'in_stock': inventario,
                 'sold': venta, 'order': ordenado, 'last_purchase': comprado})
            content = self.ids.scrn_product_contents
            content.clear_widgets()

            prodz = self.almacenamiento_productos()
            stocktable = DataTable(table=prodz)
            content.add_widget(stocktable)

    def agregar_campos_producto(self):
        target = self.ids.campos_operacion_productos
        target.clear_widgets()

        campo_agregar_cod = TextInput(hint_text='Codigo Producto', multiline=False)
        campo_agregar_nprod = TextInput(hint_text='Nombre Porducto', multiline=False)
        campo_agregar_peso = TextInput(hint_text='Peso', multiline=False)
        campo_agregar_inv = TextInput(hint_text='Disponibilidad Inventario', multiline=False)
        campo_agregar_venta = TextInput(hint_text='Ventas', multiline=False)
        campo_agregar_ordenado = TextInput(hint_text='En Tránsito', multiline=False)
        campo_agregar_fechacompra = TextInput(hint_text='Fecha últ. compra', multiline=False)
        submit = Button(text='Agregrar', size_hint_x=None, width=100,
                        on_release=lambda x: self.agregar_producto(campo_agregar_cod.text, campo_agregar_nprod.text,
                                                                   campo_agregar_peso.text, campo_agregar_inv.text,
                                                                   campo_agregar_venta.text,
                                                                   campo_agregar_ordenado.text,
                                                                   campo_agregar_fechacompra.text))

        target.add_widget(campo_agregar_cod)
        target.add_widget(campo_agregar_nprod)
        target.add_widget(campo_agregar_peso)
        target.add_widget(campo_agregar_inv)
        target.add_widget(campo_agregar_venta)
        target.add_widget(campo_agregar_ordenado)
        target.add_widget(campo_agregar_fechacompra)
        target.add_widget(submit)

    def remover_usr(self, user):

        if user == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b] Por favor escriba el nombre de usuario a remover [/b][/color]',
                      markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            target_user = self.users.find_one({'user_name': user})
            if target_user == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Usuario inexistente[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 1)
            else:
                content = self.ids.contenido_pantallas
                content.clear_widgets()

                self.users.remove({'user_name': user})
                users = self.tabla_usuarios()
                userstable = DataTable(table=users)
                content.add_widget(userstable)

    def actualizar_productos_campo(self):
        target = self.ids.campos_operacion_productos
        target.clear_widgets()

        campo_cambio_codigo = TextInput(hint_text='Código del producto', multiline=False)
        campo_cambio_nombre = TextInput(hint_text='Nombre del producto', multiline=False)
        campo_cambio_peso = TextInput(hint_text='Peso (kg)', multiline=False)
        campo_cambio_inventario = TextInput(hint_text='Cantidad en inventario', multiline=False)
        campo_actualizar_ventas = TextInput(hint_text='Productos vendidos', multiline=False)
        campo_actualizar_transito = TextInput(hint_text='En tránsito', multiline=False)
        crud_purchase = TextInput(hint_text='Última compra', multiline=False)
        crud_submit = Button(text='Update', size_hint_x=None, width=100,
                             on_release=lambda x: self.actualizar_producto(campo_cambio_codigo.text,
                                                                           campo_cambio_nombre.text,
                                                                           campo_cambio_peso.text,
                                                                           campo_cambio_inventario.text,
                                                                           campo_actualizar_ventas.text,
                                                                           campo_actualizar_transito.text,
                                                                           crud_purchase.text))

        target.add_widget(campo_cambio_codigo)
        target.add_widget(campo_cambio_nombre)
        target.add_widget(campo_cambio_peso)
        target.add_widget(campo_cambio_inventario)
        target.add_widget(campo_actualizar_ventas)
        target.add_widget(campo_actualizar_transito)
        target.add_widget(crud_purchase)
        target.add_widget(crud_submit)

    def actualizar_producto(self, code, name, weight, stock, sold, order, purchase, product_weight=None):

        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Código requerido[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            target_code = self.products.find_one({'product_code': code})
            if target_code == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]El código no se encuentra[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 1)
            else:
                if name == '':
                    name = target_code['product_name']
                if product_weight == '':
                    product_weight = target_code['product_weight']
                if stock == '':
                    stock = target_code['in_stock']
                if sold == '':
                    sold = target_code['sold']
                if order == '':
                    order = target_code['order']
                if purchase == '':
                    purchase = target_code['last_purchase']
                content = self.ids.scrn_product_contents
                content.clear_widgets()

                self.products.update_one({'product_code': code}, {
                    '$set': {'product_code': code, 'product_name': name, 'product_weight': weight, 'in_stock': stock,
                             'sold': sold, 'order': order, 'last_purchase': purchase}})

                prodz = self.almacenamiento_productos()
                stocktable = DataTable(table=prodz)
                content.add_widget(stocktable)

    def remover_productos_campo(self):
        target = self.ids.campos_operacion_productos
        target.clear_widgets()
        input_codigo_remover = TextInput(hint_text='Código del producto')
        crud_submit = Button(text='Remover', size_hint_x=None, width=100,
                             on_release=lambda x: self.remover_producto(input_codigo_remover.text))

        target.add_widget(input_codigo_remover)
        target.add_widget(crud_submit)

    def remover_producto(self, codigo):
        if codigo == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Todos los campos obligatorios[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            target_code = self.products.find_one({'product_code': codigo})
            if target_code == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Código inválido[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 1)
            else:
                content = self.ids.scrn_product_contents
                content.clear_widgets()

                self.products.remove({'product_code': codigo})

                prodz = self.almacenamiento_productos()
                stocktable = DataTable(table=prodz)
                content.add_widget(stocktable)

    def almacenamiento_productos(self):
        client = MongoClient()
        db = client.facturacion
        products = db.inventario
        _stocks = OrderedDict()
        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_weight'] = {}
        _stocks['in_stock'] = {}
        _stocks['sold'] = {}
        _stocks['order'] = {}
        _stocks['last_purchase'] = {}

        codigo_producto = []
        nombre_producto = []
        product_weight = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []

        for product in products.find():
            codigo_producto.append(product['product_code'])
            name = product['product_name']
            if len(name) > 10:
                name = name[:10] + '...'
            nombre_producto.append(name)
            product_weight.append(product['product_weight'])
            in_stock.append(product['in_stock'])
            try:
                sold.append(product['sold'])
            except KeyError:
                sold.append('')
            try:
                order.append(product['order'])
            except KeyError:
                order.append('')
            try:
                last_purchase.append(product['last_purchase'])
            except KeyError:
                last_purchase.append('')

        products_length = len(codigo_producto)
        idx = 0

        while idx < products_length:
            _stocks['product_code'][idx] = codigo_producto[idx]
            _stocks['product_name'][idx] = nombre_producto[idx]
            _stocks['product_weight'][idx] = product_weight[idx]
            _stocks['in_stock'][idx] = in_stock[idx]
            _stocks['sold'][idx] = sold[idx]
            _stocks['order'][idx] = order[idx]
            _stocks['last_purchase'][idx] = last_purchase[idx]

            idx += 1

        return _stocks

    def logout(self):
        self.parent.parent.current = 'scrn_si'

    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def cambio_pantalla(self, instance):
        if instance.text == 'Administrar Inventario':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == 'Administrar Usuarios':
            self.ids.scrn_mngr.current = 'scrn_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'


class AdminApp(App):
    def build(self):
        return Ventana_Administrador()


if __name__ == '__main__':
    AdminApp().run()