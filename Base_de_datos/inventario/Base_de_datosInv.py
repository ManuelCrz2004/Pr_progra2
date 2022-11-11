from math import prod
from Base_de_datos.inventario.ProductosInv import *
import sqlite3

def CrearBaseInventario():
    conn = sqlite3.connect('Inventario.db')
    conn.commit()
    conn.close()
    
def CrearTablaInventario():
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS inventario (
        producto TEXT,
        division TEXT,
        precio_unitario INTEGER,
        cantidad INTEGER)""")
    conn.commit()
    conn.close()

def OrdenarBaseInv():
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    leer_ordenado = f"SELECT * FROM inventario ORDER BY division"
    cursor.execute(leer_ordenado)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()

def LeerBaseInv():
    OrdenarBaseInv()
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    leer = f"SELECT * FROM inventario"
    cursor.execute(leer)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos

def InsertarProducto(producto):
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    ejecutable = f"INSERT INTO inventario VALUES ('{producto.nombre}', '{producto.division}', '{producto.precio_unitario}', '{producto.cantidad}')" 
    cursor.execute(ejecutable)
    OrdenarBaseInv()
    conn.commit()   
    conn.close()

def EliminarProducto(nombre):
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    instr = f"DELETE FROM inventario WHERE producto == '{nombre}'"
    cursor.execute(instr)
    conn.commit()
    conn.close()
        
def ActualizarPrecio(producto, precio):
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    instr = FiltrarInv("producto", producto)
    instr = instr[0]
    nombr = instr[0]
    divis = instr[1]
    cant = instr[3]
    OrdenarBase()
    conn.commit()
    conn.close()
    prd = Productos(nombr, divis, precio, cant)
    EliminarProducto(producto)
    InsertarProducto(prd)
    
def ActualizarCantidad(producto, cant):
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    filtro = FiltrarInv("producto", producto)
    prd = filtro[0]
    nombre = prd[0]
    division = prd[1]
    precio = prd[2]
    cantidad = int(prd[3])
    cantidad += cant
    OrdenarBaseInv()
    conn.commit()
    conn.close()
    producto_final = Productos(nombre, division, precio, cantidad)
    EliminarProducto(producto)
    InsertarProducto(producto_final)

def RestarCantidad(producto, cant):
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    filtro = FiltrarInv("producto", producto)
    prd = filtro[0]
    nombre = prd[0]
    division = prd[1]
    precio = prd[2]
    cantidad = int(prd[3])
    cantidad -= cant
    OrdenarBase()
    conn.commit()
    conn.close()
    producto_final = Productos(nombre, division, precio, cantidad)
    EliminarProducto(producto)
    InsertarProducto(producto_final)

def FiltrarInv(argumento, filtro): 
    conn = sqlite3.connect('Inventario.db')
    cursor = conn.cursor()
    instruccion = f"SELECT * FROM inventario WHERE {argumento} == '{filtro}'"
    cursor.execute(instruccion)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos    

def ImprimirBase():
    base_datos = LeerBaseInv()
    contador = 1
    for i in base_datos:
        usr = Productos(i[0], i[1], i[2], i[3])
        msn = f"*************************\n*************************\n{contador}\n {usr} \n*************************\n"
        print(msn)
        contador += 1
