import tkinter as tk
from tkinter import messagebox

class Categoria:
    def __init__(self, nombre):
        self.nombre = nombre

    def mostrar_info(self):
        return f"Categoría: {self.nombre}"

class Producto:
    def __init__(self, nombre, precio, categoria):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria

    def mostrar_info(self):
        return f"Producto: {self.nombre}\nPrecio: ${self.precio:.2f}\nCategoría: {self.categoria.nombre}"

class Cliente:
    def __init__(self, nombre, apellido, id_cliente):
        self.nombre = nombre
        self.apellido = apellido
        self.id_cliente = id_cliente

    def mostrar_info(self):
        return f"Cliente: {self.nombre} {self.apellido} (ID: {self.id_cliente})"

class ItemOrden:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad

class Orden:
    def __init__(self, cliente):
        self.cliente = cliente
        self.items = []
        self.total = 0.0

    def agregar_item(self, item, cantidad):
        self.items.append((item, cantidad))

    def calcular_total(self):
        self.total = sum(item.calcular_subtotal() for item, cantidad in self.items)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Tienda")

        self.productos = []
        self.clientes = []
        self.ordenes = []
        self.categorias = []

        # Elementos de la interfaz
        self.label_nombre_producto = tk.Label(self, text="Nombre del producto:")
        self.label_nombre_producto.pack()
        self.entry_nombre_producto = tk.Entry(self)
        self.entry_nombre_producto.pack()

        self.label_precio_producto = tk.Label(self, text="Precio del producto:")
        self.label_precio_producto.pack()
        self.entry_precio_producto = tk.Entry(self)
        self.entry_precio_producto.pack()

        self.label_categoria_producto = tk.Label(self, text="Categoría del producto:")
        self.label_categoria_producto.pack()
        self.entry_categoria_producto = tk.Entry(self)
        self.entry_categoria_producto.pack()

        self.btn_registrar_producto = tk.Button(self, text="Registrar Producto", command=self.registrar_producto)
        self.btn_registrar_producto.pack()

        self.label_nombre_cliente = tk.Label(self, text="Nombre del cliente:")
        self.label_nombre_cliente.pack()
        self.entry_nombre_cliente = tk.Entry(self)
        self.entry_nombre_cliente.pack()

        self.label_apellido_cliente = tk.Label(self, text="Apellido del cliente:")
        self.label_apellido_cliente.pack()
        self.entry_apellido_cliente = tk.Entry(self)
        self.entry_apellido_cliente.pack()

        self.label_id_cliente = tk.Label(self, text="ID del cliente:")
        self.label_id_cliente.pack()
        self.entry_id_cliente = tk.Entry(self)
        self.entry_id_cliente.pack()

        self.btn_registrar_cliente = tk.Button(self, text="Registrar Cliente", command=self.registrar_cliente)
        self.btn_registrar_cliente.pack()

        self.label_producto_orden = tk.Label(self, text="Producto de la orden:")
        self.label_producto_orden.pack()
        self.entry_producto_orden = tk.Entry(self)
        self.entry_producto_orden.pack()

        self.label_cantidad_orden = tk.Label(self, text="Cantidad del producto:")
        self.label_cantidad_orden.pack()
        self.entry_cantidad_orden = tk.Entry(self)
        self.entry_cantidad_orden.pack()

        self.btn_agregar_item = tk.Button(self, text="Agregar Producto a Orden", command=self.agregar_producto_orden)
        self.btn_agregar_item.pack()

        self.label_info_orden = tk.Label(self, text="", wraplength=300, justify="left", pady=10)
        self.label_info_orden.pack()

        # Configuración de la posición de la ventana
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = screen_width - window_width - 50  # Ajusta aquí la distancia desde el lado derecho
        y_position = 50  # Ajusta aquí la distancia desde la parte superior
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    def registrar_producto(self):
        nombre = self.entry_nombre_producto.get()
        precio = float(self.entry_precio_producto.get())
        nombre_categoria = self.entry_categoria_producto.get()

        categoria = Categoria(nombre_categoria)
        producto = Producto(nombre, precio, categoria)
        self.productos.append(producto)

        info = producto.mostrar_info()
        self.label_info_orden.config(text=f"Producto registrado:\n{info}")

    def registrar_cliente(self):
        nombre = self.entry_nombre_cliente.get()
        apellido = self.entry_apellido_cliente.get()
        id_cliente = self.entry_id_cliente.get()

        cliente = Cliente(nombre, apellido, id_cliente)
        self.clientes.append(cliente)

        info = cliente.mostrar_info()
        self.label_info_orden.config(text=f"Cliente registrado:\n{info}")

    def agregar_producto_orden(self):
        nombre_producto = self.entry_producto_orden.get()
        cantidad = int(self.entry_cantidad_orden.get())

        # Buscar el producto por nombre
        producto_encontrado = None
        for producto in self.productos:
            if producto.nombre == nombre_producto:
                producto_encontrado = producto
                break

        if producto_encontrado:
            item_orden = ItemOrden(producto_encontrado, cantidad)
            orden_existente = False

            for orden in self.ordenes:
                if orden.cliente == self.clientes[-1]:  
                    orden.agregar_item(item_orden, cantidad)
                    orden_existente = True
                    break

            if not orden_existente:
                nueva_orden = Orden(self.clientes[-1])
                nueva_orden.agregar_item(item_orden, cantidad)
                self.ordenes.append(nueva_orden)

            # Calcular el total de la orden
            nueva_orden.calcular_total()

            info = f"Se agregó {cantidad} {producto_encontrado.nombre}(s) a la orden.\nTotal de la orden para {self.clientes[-1].nombre} {self.clientes[-1].apellido}: ${nueva_orden.total:.2f}"
            self.label_info_orden.config(text=info)

            # Mostrar mensaje emergente de éxito
            messagebox.showinfo("Éxito", "Producto agregado a la orden correctamente.")

        else:
            self.label_info_orden.config(text="Producto no encontrado.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
