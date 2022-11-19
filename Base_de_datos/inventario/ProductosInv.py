"""Módulo ProductosInv

    Este módulo se encarga de crear objetos con la clase Productos y ejecutar algunos metodos a estos mismos.

    Los metodos que estan en la clase Usuario son:
        __init__
        __str__
        AñadirProducto
        RetirarProducto
        ModificarPrecio
        SumarIva
"""


class Productos:
    """Representa un Producto:

    Atributos:
        nombre (str): [Nombre del producto]
        division (str): [Tipo de producto]
        precio_unitario (int): [Precio de una unidad del producto]
        cantidad (int): [Cantidad de cada producto]
        iva (bool): [Corresponde si el valor tiene adicionado el iva]
        """

    def __init__(self, Nombre: str, division: str, precio_unidad: int, cantiadad: int = 0) -> object:
        """Inicializa en objeto de tipo Producto

        Args:
            Nombre (str): Distinguidor de objeto, es decir, el nombre del producto.
            division (str): El tipo de producto que es.
            precio_unidad (int): Valor de precio por unidad del producto
            cantiadad(int): Valor que da a conocer la cantidad del producto disponible -- su valor inicial por defecto es 0
        """
        self.nombre = Nombre.upper()
        self.division = division.upper()
        self.precio_unitario = precio_unidad
        self.cantidad = cantiadad
        self.iva = False

    def __str__(self) -> str:
        """Resume el objeto de la clase Producto con los datos principales

        Returns:
            str: Mensaje con el nombre, precio de unidad y cantidad del objeto de la clase Producto
        """
        mensaje = f"""PRODUCTO: {self.nombre}
PU: ${self.precio_unitario} - {self.cantidad} Unidades"""
        return mensaje

    def AñadirProducto(self, cantidad):
        """Suma un valor entero en el atributo cantidad del objeto Producto

        Args:
            cantidad (int): Valor que se va a sumar al atributo cantidad
        """

        self.cantidad += cantidad

    def RetirarProducto(self, cantidad):
        """Modifica el atributo cantidad del objeto Producto, restandole un valor entero

        Args:
        cantidad (int): Valor que se va a restar al atributo cantidad

        """
        self.cantidad -= cantidad

    def ModificarPrecio(self, precio_nuevo):
        """Cambia el atributo precio_unitario del objeto Usuario por un valor entero

        Args:
            precio_nuevo (int): Valor que se va a asignar al atributo precio_unitario

        """
        self.precio_unitario = precio_nuevo

    def SumarIva(self):
        """Suma al atributo precio_unitario del objeto Producto, el valor del impuesto Iva
        """
        impuesto = self.precio_unitario * 0.19  # 0.19 es el porcentaje del IVA
        self.precio_unitario += impuesto