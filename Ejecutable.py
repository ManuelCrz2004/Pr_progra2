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


#El objetivo de esta funcion es que el usuario administrador pueda crear nuevos intgrantes en la organizacion

# El objetivo de esta funcion es que el usuario administrador pueda crear nuevos intgrantes en la organizacion
def CrearUsuario():
    import random  # Se usa random para que genere un id de 3 digitos aleatorios que seran asignados al nuevo usuario

    nombre = input("> Ingrese el nombre: ")
    rol = input("> Ingrese el rol que va a desempeñar: ")
    confirmacion_contraseña = False

    while confirmacion_contraseña == False:  # Aqui se confirma que el usuario este escribiendo corectamente la contraseaña. En caso de no hacerlo, implicará que las contraseñas no coinciden
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
    # El condicional funciona dependiendo de la primera letra que sea escrita por el usuario. Dependiendo de la respuesta, se crea admin, cajero, invitado o supervisor
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

    # El nuevo usuario es vacío y tendrá las tres primeras letras del rol asignado junto a lso tres digitos que le identifican.
    usr = ""
    for letra in usuario.rol:
        if len(usr) != 3:
            usr += letra
        else:
            pass
    usr = usr.lower()
    usr += "_" + id_nuevo

    usuario = Usuario(nombre, rol, contraseña, usr, id_definitivo)

    print(
        f"El usuario creado es el siguiente: ")  # Se confirma en una tupla el usuario recien creado que será almacenado en la base de datos.
    print(usuario)

    conf = input("Desea continuar con el Usuario creado? [S/N]\n> ")

    if conf.upper() == "S":
        InsertarUsuario(
            usuario)  # Si se desea continuar el procedimiento, el usuario será almacenado en la base de datos. De lo contrario volverá al menú inicial de administrador
        print("Usuario agregado con exito")
    elif conf.upper() == "N":
        CrearUsuario()


def EliminarUsr():  # Funcion recursiva que pide al admin el nombre de usuaio que se desea eliminar. En caso de confirmar los cambios, la base de datos será actualizada.
    usuario_el = input("Ingrese el usuario que desea eliminar?\n > ")
    confirmacion = input(
        f"Esta seguro que desea eliminar el usuario {usuario_el}? [S/N]\n> ")  # Esta variable guarda un "S" (que corresponde a que si se quiere eliminar) o "N" (que indica que no se quiere eliminar definitivamente)
    if confirmacion.upper() == "S":  # Para que no haya errores en la sintaxis del usuario, se convierte el string en mayúscula
        print("Si confirma")
        EliminarUsuario("usuario",
                        usuario_el)  # Se invoca esta función del módulo Usuarios con sus respectivos argumentos
        print("El usuario fue eliminado de la organización.")
    elif confirmacion.upper() == "N":
        EliminarUsr()  # Se vuelve a invocar la función
    else:
        print("No se entendio el valor ingresado")


# Función recursiva que da la bienvenida al usuario y preguntamos primero si es alguien registrado, para mayor privacidad del establecimiento.
def InicioBienvenida():
    print(
        "Hola! Bienvenid@ a nuestro programa. \n El objetivo es optimizar manejo de contabilidad una empresa que maneje inventario y flujo de caja.")
    user_validation = input(
        "Es usted un usuario registrado? \n [S/N]:")  # Para validar y dar ingreso a el programa, se confirma si el usuario esta registrado

    if user_validation.upper() == "S":
        Validacion()  # Se invoca la función validación para validar las credenciales que el usuario ingrese.
    else:
        print("Lo siento, No cuentas con los permisos para acceder")
        InicioBienvenida()  # Vuelve a mostrarle el menú de bienvenida al usuario


# Función que que pide digitar el nombre de usuario y verifica si ya existe. De acuerdo a eso, se pide que se inserte la contraseña y verifica si es válida.
def Validacion():
    user_identificacion = input("Por favor, digite su usario: \n")
    verificador_base = Filtrar("usuario",
                               f"{user_identificacion}")  # Invoca la función Filtrar del módulo Base_de_datosUsr para poder ver si existe un usuario que concuerde en la base de datos.

    if len(verificador_base) == 0:  # Si la longitud es 0, quiere decir que no hay ningun usuario llamado asi que exista
        print("No se encuentra ningun usuario con ese valor. ")
        Validacion()  # Vuelve a mostrar este menú
    elif len(verificador_base) == 1:
        # print(verificador_base) para ver la contraseña del usuario y confirmar que existe la cuenta
        user_password = input("Digite su contraseña: \n")
        verificador_base = verificador_base[0]
        if verificador_base[
            5] == user_password:  # Ya que verificador base es una tupla, el índice 5 de este corresponderia a la contraseña y el condicional se usa para ver si coincide con la que el usuario ingresó
            print(f"Bienvenido {verificador_base[1]}")  # El indice 1 de esta tupla es el nombre de usuario
            id_usr = verificador_base[3]  # El indice 3 de la tupla corresponde al id del usuario
            VerificacionRol(id_usr)  # Se pide que se verifique el rol del usuario con esta función
        else:
            print("Valores para contraseña incorrectos")
    elif len(verificador_base) > 1:
        print(
            "Comuniquese con un administrador para revisar su caso")  # Quiere decir que hay dos o más usuarios con el mismo nombre de usuario
    else:
        print("Su petición no fue entendida")


# Función que verifica con el uso de condicionales cual rol tiene el usuario de acuerdo con la letra inicial del id del usuario.
def VerificacionRol(id):
    inicial_id = id[0]  # El índice 0 del id corresponde a una letra mayúscula que indica el rol del usuario

    if inicial_id == "A":
        administrador()  # Se invoca la función administrador
    elif inicial_id == "C":
        cajero()  # Se invoca la función cajero
def Facturar():
    productos = []
    ''' 
        La variable productos es una lista vacía que se irá alimentando conforme a los porductos que sean seleccionados
        el usuario debe escirbir el nombre del producto que se encuentra actualmente en el inventario, para que sea
        cotejado en la base de datos.
        
    '''
    while True:
        print("Ingrese nombre del producto ('EXIT' para salit)")
        prod = input("> ")
        filtro1 = FiltrarInv("producto", prod)
        # En la variable filtro1 se almacena el input del usuario que será evaluada en la columna 0 de la base de datos
        # en caso de que el usuario esriba EXIT, se intrará al módulo Cobrar para imprimir la factura

        if len(filtro1) == 0:
            if prod == "EXIT":
                Cobrar(productos)
                break
            else:
                print("El producto no existe")

        elif len(filtro1) == 1:
            # Si el elemento a cobrar, se encuentra en la lista de la base de datos, se imprime la cantidad dispinible
            # también se imprime la categoría y el precio unitario, almacenados en una tupla.
            print(filtro1)
            unidades = input("> Ingrese las unidades a facturar\n> ")
            cantidad = filtro1[0]
            cantidad_total = cantidad[3]
            # En la base de datos, se toma en cuenta si la cantidad a llevar supera el límite actual de inventario
            if int(unidades) > int(cantidad_total):
                print("Se esta exediendo el limite del inventario")
            else:
                # Cantidad_n se refiere a la resta del inventario actual, con las unidades a cobrar. Es una resta posible
                # porque previamente se verificó que las uniades a llevar son menos que el inventario total

                cantidad_n = int(cantidad_total) - int(unidades)
                unidades_f = -int(unidades)
                ActualizarCantidad(prod, unidades_f) # Se alimenta la función Actualizar Cantidad con el producto que se cobró menos la cantidad que fue llevada
                productos.append((prod, unidades)) #Creación de una tupla que contiene el elemento a llevar y la cantidad de veces que debe ser restado de la db
        elif len(filtro1) > 1: #Si existen productos duplicados en la tabla, entonces el usuario tendrá que escoger a cuál cobrar
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
                            print("Se esta excediendo el limite del inventario")
                        else:
                            cantidad_n = int(cantidad_total) - int(unidades)
                            unidades_f = -int(unidades)
                            ActualizarCantidad(prod, unidades_f)
                            productos.append((prod, unidades))
                            break
                    else:
                        contador -= 1


def Cobrar(lista):
    # Se da como argumento una lista con los objetos de la clase Productos que se quieren cobrar
    total_cobrar = 0
    mensaje = "**** Compra total: ****\n"

    for i in lista:
        nombre = i[0]
        cantidad = int(i[1])
        prec = FiltrarInv("producto",
                          f"{nombre}")  # Se invoca la función FiltrarInv de módulo Base_de_datosUsr para buscar los datos del producto

        prec = prec[0]  # prec[0] corresponde a la tupla con la información del producto
        prec = int(prec[2])  # prec[2] corresponde al precio de ese producto
        prec_tot = prec * cantidad  # Se multiplica el precio por la cantidad para hayar el total que hay que pagar para ese producto
        total_cobrar += prec_tot  # Se le suma a la variable que guarda el total de cobrar

        msn = f"{nombre}  cant. {cantidad}\n.... tot. {prec_tot}\n"  # Se crea un mensaje con el nombre del producto, la cantidad de este y el precio que hay que pagar por ese producto
        mensaje += msn
    mensaje += f"Total: {total_cobrar} COP"  # Al final se suma un mensaje que contenga el total a cobrar
    mensaje += "\n***********************"

    print(mensaje)  # Imprime ese mensaje

    ingreso = int(input("Dinero recibido\n "))

    vueltas = ingreso - total_cobrar
    print(f"Tiene que dar - {vueltas}")


def ModificadorInventario():
    des = input("Aqui puede modificar el inventario.\n1) Añadir producto\n2) Borrar producto\n3) Cambiar Precio")

    if des == "1":
        print("Agregar un elemento al inventario")
        nom = input("Ingrese el nombre del producto:")
        nom = nom.upper()  # Se cambia a mayúsculas
        filtro_nombre = FiltrarInv("producto",
                                   nom)  # Se invoca la función Filtrar de módulo Base_de_datosUsr para verificar si el producto ya existe

        if len(filtro_nombre) != 0:
            print("Su producto ya se encuentra en el inventario, este se sumara con el presente.")
            cant = int(input("Ingrese la cantidad a añadir: "))
            ActualizarCantidad(nom,
                               cant)  # Se invoca la función ActualizarCantidad del módulo Base_de_datosInv para modificar la cantidad del producto ya existente en la base de datos.
            print("Producto añadido y base actualizada")
        elif len(filtro_nombre) == 0:
            print("Se va a añadir un producto nuevo")
            div = input("A que division pertenece?")
            canti = input("Ingrese la cantidad del producto: ")
            price = input("Ingrese el precio unitario")
            producto = Productos(nom, div, price,
                                 canti)  # Se crea un objeto de la clase Productos del módulo ProductosInv
            InsertarProducto(
                producto)  # Se invoca la función InsertaProducto del módulo Base_de_datosInv para añadir el objeto producto a la base de datos.
    elif des == "2":
        print("Eliminar un elemento del inventario")
        nom = input("Ingrese el nombre del producto. ")
        nom = nom.upper()
        conf = input(
            f"Esta seguro que desea eliminar {nom} [S/N]")  # Se confirma si el usuario esta seguro de eliminar el producto
        conf = conf.upper()

        if conf == "S":
            EliminarProducto(
                nom)  # Se invoca la función EliminarProducto del modulo Base_de_datosInv para remover el producto de la base de datos
            print("Producto Eliminado")
        elif conf == "N":
            administrador()  # Se invoca la función administrador para que el usuario pueda volver al menú principal del administrador
        else:
            print("Tu respuesta no ha sido entendida.")
            ModificadorInventario()  # Se vuelve a invocar esta función paara que el usuario pueda retornar al menú de modificar inventario
    elif des == "3":
        print("Se Cambiara el precio de un producto")
        nom = input("Ingrese el nombre del producto: ")
        prec = int(input("Ingrese el nuevo precio: "))
        nom.upper()
        ActualizarPrecio(nom,
                         prec)  # Se invoca la función ActualizarPrecio del módulo Base_de_datosInv para modificar el precio del producto ya existente en la base de datos.
        print("Precio actualizado")


def administrador():
    eleccion = int(input(
        "El menu de acciones es el siguiente: \n 1: Crear Usuario. \n 2: Remover usuario.\n 3: Acciones inventario \n 4: Imprimir facturas \n 5: Mostar modo cajero \n 6: Menu cajero \n"))

    if eleccion == 1:
        print("Aqui puede crear nuevos usarios en a la organizacion.")
        CrearUsuario()  # Se comunica con el archivo Usuarios para que pueda usar el método crear usuarios implementado en dicha clase.

    elif eleccion == 2:
        print(
            "Aqui puede remover usuario de la base de datos")  ##Se comunica con el archivo Usuarios para que pueda usar el método crear usuarios implementado en dicha clase.
        EliminarUsr()  # Al ser una lista, se implementa de la manera .pop() para remover un usuario.

    elif eleccion == 3:
        while True:
            ModificadorInventario()
            OrdenarBaseInv()

            ####### Se esta retornando la base de datos en desorde, hay que buscar una solución para que esta pueda devolverse organizada y esta sea mas comoda para el usuario

            conf = input("> Desea Salir? [S/N]").upper()

            if conf == "S":
                break
            else:
                continue

    elif eleccion == 4:  # Como el módulo 4 no se ha implementado todavía, al momento del programa notificar un error, es mejor que se le notifique al usuario que se está trabajando en ello.
        try:
            print("Pronto disponible.")
        except:
            print("Pronto podra imprimir facturacion de los elementos vendidos")
    elif eleccion == 5:
        try:
            cajero()  # Pendiente por crear el menu ventas
        except:
            print("Oops! Este modulo pronto estara disponible")
    elif eleccion == 6:
        cajero()  # En este método, el programa se comunicará con Usuario y el método Cambiar Contraseña
    else:
        return "Contacte a su administrador para que le pueda crear su usuario."

def cajero():
        print("Bienvenido de vuelta")
        # Después que la consola imprime el mensaje bienvenido, se le pide al usuario que seleccione
        cajero_eleccion = int(input("Presione 1 para empezar a facturar. \n Presione 2 para mirar el inventario actual."))
        if cajero_eleccion == 1:
            Facturar()
        elif cajero_eleccion == 2:
            ImprimirBase()
        else:
            return 'Escoja una opcion valida'



#Se llama a la funcion para validar su funcionamiento
InicioBienvenida()