from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from collections import OrderedDict #Ordenar los datos en forma de tabla
from pymongo import MongoClient
from utils.datatable import Datatable
class AdminWindow (BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #print(self.get_product())
        content = self.ids.scrn_content
        users = self.get_users()
        userstable = Datatable(table= users)
        content.add_widget(userstable)

        #Display Products
        product_scrn = self.ids.scrn_product_content
        products = self.get_product()
        prod_table = Datatable(table=products)
        product_scrn.add_widget(prod_table)

#----------------------------------------------------------------------------#
#Conexion con la base de datos MongoClient

    def get_users(self):
        client = MongoClient() #Conexion con la base de datos

        db = client.silverpos
        users = db.users
        _users = OrderedDict()
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['user_names'] = {}
        _users['passwords'] = {}
        _users['designation'] = {}
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designation = []
        for user in users.find():
            first_names.append(user['firs_name']) #nombre del usuario
            last_names.append(user['last_name']) #apellido del usuario
            user_names.append(user['user_name']) #nombre de usuario
            pwd = user['passwords']
            if len(pwd) > 10:
                pwd = pwd [:10] + '...'
            passwords.append(pwd) #contraseña a guardar
            designation.append(user['designation']) #El rol a asignar

        users_length = len(first_names) #la longitud del nombre de usuario será igual a la longitud de su primer nombre
        idx = 0 #el indice o cantidad de usuarios comienza en 0
        while idx < users_length:
            _users['first_names'][idx] = first_names[idx]
            _users['password_names'][idx] = first_names[idx]
            _users['user_names'][idx] = first_names[idx]
            _users['password'][idx] = first_names[idx]
            _users['designation'][idx] = first_names[idx]

            idx += 1

        return(_users)
#----------------------------------------------------------------------------#
    def get_product(self):
        client = MongoClient() #Conexion con la base de datos

        db = client.silverpos
        products = db.stocks
        _stocks = OrderedDict()
        _stocks['product_code'] = {},
        _stocks['product_name'] = {},
        _stocks['product_weight'] = {},
        _stocks['in_stock'] = {},
        _stocks['sold'] = {},
        _stocks['order'] = {},
        _stocks['last_purchase'] = {}


        product_code = []
        product_name = []
        product_weight = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []
        for product in products.find():
            product_code.append(product['firs_name']) #nombre del usuario
            name = product['last_name']
            if len(name) > 10:
                name = name[:10] + '...'
            product_name.append(name) #apellido del usuario
            product_weight.append(product['user_name']) #nombre de usuario
            in_stock.append(product['in_stock']) #contraseña a guardar
            sold.append(product['sold']) #El rol a asignar
            order.append(product['order'])
            last_purchase.append((product['last_purchase']))

        products_length = len(product_code) #la longitud del nombre de usuario será igual a la longitud de su primer nombre
        idx = 0 #el indice o cantidad de usuarios comienza en 0
        while idx < products_length:
            _stocks['product_code'][idx] = product_code[idx]
            _stocks['product_name'][idx] = product_name[idx]
            _stocks['product_weight'][idx] = product_weight[idx]
            _stocks['in_stock'][idx] = in_stock[idx]
            _stocks['sold'][idx] = sold[idx]
            _stocks['order'][idx] = order[idx]
            _stocks['last_purchase'][idx] = last_purchase[idx]

            idx += 1

        return _stocks

    def change_screen(self,instance):
        if instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'scrn_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'




class AdminApp(App):
    def build(self):

        return AdminWindow()

if __name__ == '__main__':
    AdminApp().run()

