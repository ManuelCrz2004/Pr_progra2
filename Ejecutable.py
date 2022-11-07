'''
Este archivo tiene como finalidad ser el menú principal para el usuario. 
Será el archivo que enlace todos los documentos, módulos y clases, por este motivo se llama Ejecutable.py 
    Se busca que el usuario pueda inicialmente crear usuarios dentro de la base de datos creada para el programa.
'''

#Se importan los modulos de las subcarpetas correspondientes

from warnings import filters
from Base_de_datos.inventario.Base_de_datosInv import *
from Base_de_datos.inventario.ProductosInv import *
from Base_de_datos.usuarios.Usuarios import *
from Base_de_datos.usuarios.Base_de_datosUsr import *
import keyboard

#El objetivo de esta funcion es que el usuario administrador pueda crear nuevos intgrantes en la organizacion
def CrearUsuario():
    import random #Se usa random para que genere un id de 3 digitos aleatorios que seran asignados al nuevo usuario
    
    nombre = input("> Ingrese el nombre: ")
    rol = input("> Ingrese el rol que va a desempeñar: ")
    confirmacion_contraseña = False
    
    while confirmacion_contraseña == False: #Aqui se confirma que el usuario este escribiendo corectamente la contraseaña. En caso de no hacerlo, implicará que las contraseñas no coinciden
        contraseña = input("> Ingrese su contraseña: ")
        confirmar_contraseña = input("> Confirme su contraseña: ")
        
        if contraseña == confirmar_contraseña:
            confirmacion_contraseña = True
        else:
            print("Las contraseñas no coinciden")
            
    id_nuevo = random.randint(100, 999)
    id_nuevo = str(id_nuevo)
    
    usuario = Usuario(nombre, rol, contraseña)
    
    roles = ["ADMINISTRADOR", "SUPERVISOR", "CAJERO", "INVITADO"]
    #El condicional funciona dependiendo de la primera letra que sea escrita por el usuario. Dependiendo de la respuesta, se crea admin, cajero, invitado o supervisor
    if usuario.rol == roles[0]:
        id_definitivo = "A" + id_nuevo
    elif usuario.rol == roles[1]:
        id_definitivo = "S" + id_nuevo
    elif usuario.rol == roles[2]:
        id_definitivo = "C" + id_nuevo
    elif usuario.rol == roles[3]:
        id_definitivo = "I" + id_nuevo
    else:
        print("No se cumplen las condiciones para crear un id")
        
    #El nuevo usuario es vacío y tendrá las tres primeras letras del rol asignado junto a lso tres digitos que le identifican.
    usr = ""
    for letra in usuario.rol:
        if len(usr) != 3:
            usr += letra
        else:
            pass 
    usr = usr.lower()   
    usr += "_" + id_nuevo
    
    usuario = Usuario(nombre, rol, contraseña, usr, id_definitivo)
    
    print(f"El usuario creado es el siguiente: ") #Se confirma en una tupla el usuario recien creado que será almacenado en la base de datos.
    print(usuario)
    
    conf = input("Desea continuar con el Usuario creado? [S/N]\n> ")
    
    if conf.upper() == "S":
        InsertarUsuario(usuario) #Si se desea continuar el procedimiento, el usuario será almacenado en la base de datos. De lo contrario volverá al menú inicial de administrador
        print("Usuario agregado con exito")
    elif conf.upper() == "N":
        CrearUsuario()

def EliminarUsr(): #Funcion que pide al admin el nombre de usuaio que se desea eliminar. En caso de confirmar los cambios, la base de datos será actualizada.
    usuario_el = input("Ingrese el usuario que desea eliminar?\n > ")
    confirmacion = input(f"Esta seguro que desea eliminar el usuario {usuario_el}? [S/N]\n> ")
    if confirmacion.upper() == "S":
        print("Si confirma")
        EliminarUsuario("usuario", usuario_el)
        print("El usuario fue eliminado de la organización.")
    elif confirmacion.upper() == "N":
        EliminarUsr()
    else:
        print("No se entendio el valor ingresado")
            
#Bienvenida al usuario y preguntamos primero si es alguien registrado, para mayor privacidad del establecimiento.
def InicioBienvenida():
    print("Hola! Bienvenid@ a nuestro programa. \n El objetivo es optimizar manejo de contabilidad una empresa que maneje inventario y flujo de caja.")
    user_validation = input("Es usted un usuario registrado? \n [S/N]:")
    
    if user_validation.upper() == "S":
        Validacion()
    else:
        print("Lo siento, No cuentas con los permisos para acceder")
        InicioBienvenida()

def Validacion():
       
    user_identificacion = input("Por favor, digite su usario: \n")
    verificador_base = Filtrar("usuario", f"{user_identificacion}")
    
    if len(verificador_base) == 0:
        print("No se encuentra ningun usuario con ese valor. ")
        Validacion()
    elif len(verificador_base) == 1:
        #print(verificador_base) para ver la contraseña del usuario y confirmar que existe la cuenta
        user_password = input("Digite su contraseña: \n")
        verificador_base = verificador_base[0]
        if verificador_base[5] == user_password:
            print(f"Bienvenido {verificador_base[1]}")
            id_usr = verificador_base[3]
            VerificacionRol(id_usr)
        else:
            print("Valores para contraseña incorrectos")
    elif len(verificador_base) > 1:
        print("Comuniquese con un administrador para revisar su caso")
    else:
        print("Su petición no fue entendida")

def VerificacionRol(id):
    inicial_id = id[0]
    
    if inicial_id == "A":
        administrador()
    elif inicial_id == "C":
        cajero()
    elif inicial_id == "S":
        supervisor()

def Facturar():
    productos = []
    while True:
        print("Ingrese el codigo o nombre del producto")
        prod = input("> ")
        try:
            keyboard.add_hotkey("ctrl+esc", lambda lista: Cobrar(lista) )
        except:
            continue
        filtro1 = FiltrarInv("producto", prod)
        #### POSIBLE FILTRO DE CODIGO ################################
        
        if len(filtro1) == 0:
            print("No existe este elemento")
        elif len(filtro1) == 1:
            print(filtro1)
            unidades = input("> Ingrese las unidades a facturar\n> ")
            cantidad = filtro1[0]
            cantidad_total = cantidad[3]
            if int(unidades) > int(cantidad_total):
                print("Se esta exediendo el limite del inventario")
            else:
                cantidad_n = int(cantidad_total) - int(unidades)
                unidades_f = -int(unidades)
                ActualizarCantidad(prod, unidades_f)
                productos.append((prod, unidades))
        elif len(filtro1) > 1:
            print("Hay mas de un elemento, cual desea seleccionar")
            contador = 1
            for i in unidades:
                nombre = i[3]
                mensaje = str(contador) + "." + nombre
                print(mensaje)
                contador += 1
            selector = input("> ")
            
            if selector in range(len(unidades)):
                while True:
                    if selector == contador and contador != 0:
                        unidades = input("> Ingrese las unidades a facturar\n> ")
                        cantidad = filtro1[0]
                        cantidad_total = cantidad[3]
                        if int(unidades) > int(cantidad_total):
                            print("Se esta exediendo el limite del inventario")
                        else:
                            cantidad_n = int(cantidad_total) - int(unidades)
                            unidades_f = -int(unidades)
                            ActualizarCantidad(prod, unidades_f)
                            productos.append((prod, unidades))
                            break
                    else:
                        contador -= 1

def Cobrar(lista):
    total_cobrar = 0
    for i in lista:
        nombre = i[0]
        cantidad = i[1]
        
            

def ModificadorInventario():
    des = input("Aqui puede modificar el inventario.\n1) Añadir producto\n2) Borrar producto\n3) Cambiar Precio")
    
    if des == "1":
        print("Agregar un elemento al inventario")
        nom = input("Ingrese el nombre del producto:")
        nom = nom.upper()
        filtro_nombre = FiltrarInv("producto", nom)
        
        if len(filtro_nombre) != 0:
            print("Su producto ya se encuentra en el inventario, este se sumara con el presente.")
            cant = int(input("Ingrese la cantidad a añadir: "))
            ActualizarCantidad(nom, cant)
            print("Producto añadido y base actualizada") 
        elif len(filtro_nombre) == 0:
            print("Se va a añadir un producto nuevo")
            div = input("A que division pertenece?")
            canti = input("Ingrese la cantidad del producto: ")
            price = input("Ingrese el precio unitario")
            producto = Productos(nom, div, price, canti)
            InsertarProducto(producto)
    elif des == "2":
        print("Eliminar un elemento del inventario")
        nom = input("Ingrese el nombre del producto. ")
        nom = nom.upper()
        conf = input(f"Esta seguro que desea eliminar {nom} [S/N]")
        conf = conf.upper()
        
        if conf == "S":
            EliminarProducto(nom)
            print("Producto Eliminado")
        elif conf == "N":
            administrador()
        else:
            print("Tu respuesta no ha sido entendida.")
            ModificadorInventario()
    elif des == "3":
        print("Se Cambiara el precio de un producto")
        nom = input("Ingrese el nombre del producto: ")
        prec = int(input("Ingrese el nuevo precio: "))
        nom.upper()
        ActualizarPrecio(nom, prec)
        print("Precio actualizado")
                    
def administrador ():
    eleccion = int(input("El menu de acciones es el siguiente: \n 1: Crear Usuario. \n 2: Remover usuario.\n 3: Acciones inventario \n 4: Imprimir facturas \n 5: Mostar modo cajero \n 6: Menu cajero \n"))
            
    if eleccion == 1:
            print("Aqui puede crear nuevos usarios en a la organizacion.")
            CrearUsuario() #Se comunica con el archivo Usuarios para que pueda usar el método crear usuarios implementado en dicha clase.

    elif eleccion == 2:
            print("Aqui puede remover usuario de la base de datos") ##Se comunica con el archivo Usuarios para que pueda usar el método crear usuarios implementado en dicha clase.
            EliminarUsr() #Al ser una lista, se implementa de la manera .pop() para remover un usuario.
            
    elif eleccion == 3:
        ModificadorInventario()
                    
    elif eleccion == 4: #Como el módulo 4 no se ha implementado todavía, al momento del programa notificar un error, es mejor que se le notifique al usuario que se está trabajando en ello.
        try:
            print("Pronto disponible.")
        except:
            print("Pronto podra imprimir facturacion de los elementos vendidos")
    elif eleccion == 5: 
            try:
                Base_de_datosUsr(menu_ventas) #Pendiente por crear el menu ventas
            except:
                print("Oops! Este modulo pronto estara disponible")
    elif eleccion == 6:
        cajero() #En este método, el programa se comunicará con Usuario y el método Cambiar Contraseña
    else:
        return "Contacte a su administrador para que le pueda crear su usuario."        

def cajero():
        print("Bienvenido de vuelta")
        cajero_eleccion = int(input("Presione 1 para empezar a facturar. \n Presione 2 para mirar el inventario actual."))
        if cajero_eleccion == 1:
            Facturar()
        elif cajero_eleccion == 2:
            print("Pronto disponible.")
        else:
            return 'Escoja una opcion valida'

def supervisor(credenciales):
    if credenciales == ["SUPERVISOR", 1234]:
        print("Bienvenido de vuelta, ")
        supervisor_eleccion = int(input("El menu de acciones es el siguiente: \n 1: Ver o editar inventario \n 2: Imprimir facturas \n 3: Mostar modo cajero \n 6: Menu cajero"))
        if supervisor_eleccion == 1:
            sub_opcion = int(input("Presione 1 si desea unicamente ver el inventario. \n Presione 2 si desea editar el inventario actual."))
            if sub_opcion == 1:
                print("Pronto disponible.")
            elif sub_opcion == 2:
                print("Agregara un nuevo elemento?")
                if sub_opcion.upper() == "S":
                    print("Pronto disponible.") #Aqui se llama a la funcion Base de datos para agregar nuevos elementos a la lista
                else:
                    print("Pronto disponible.")
            elif supervisor_eleccion == 2: 
                try:
                    print("Pronto disponible.")
                except:
                    print("Pronto podra imprimir facturacion de los elementos vendidos")
            elif supervisor_eleccion == 3: 
                try:
                    Base_de_datosUsr(menu_ventas) #Pendiente por crear el menu ventas
                except:
                    print("Oops! Este modulo pronto estara disponible")
            elif credenciales == ['INVITADO', 1234]:
                print("Como invitado usted puede unicamente ver el inventario del establecimiento.")
                return print("Pronto disponible.")
    else: 
        return "Contacte a su administrador para que le pueda crear su usuario" 

#Se llama a la funcion para validar su funcionamiento
InicioBienvenida()