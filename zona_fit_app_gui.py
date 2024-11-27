import tkinter as tk
from tkinter import ttk, messagebox

from zona_fit_db.cliente import Cliente
from zona_fit_db.cliente_dao import ClienteDAO


class App(tk.Tk):
    COLOR_VENTANA = '#1d2d44'

    def __init__(self):
        super().__init__()
        self.id_cliente = None
        self.configurar_ventana()
        self.configurar_grid()
        self.mostrar_titulo()
        self.mostrar_formulario()
        self.cargar_tabla()
        self.mostrar_botones()

    # Metodos de configuracion =========================================================================================
    def configurar_ventana(self):
        self.geometry('700x500')
        self.title('Zona Fit App')
        self.configure(background=self.COLOR_VENTANA)
        # Aplicamos estilos
        self.estilos = ttk.Style()
        self.estilos.theme_use('clam')  # Preparamos los estilos para el modo oscuro
        self.estilos.configure(self,
                                background=self.COLOR_VENTANA,
                                foreground='white',  # Color del texto
                                fieldbackground='black'  # Color de fondo de los componentes
                                )

    def configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def mostrar_titulo(self):
        titulo = ttk.Label(self, text='Zona Fit (GYM)', font=('Arial', 20),
                            background=self.COLOR_VENTANA,
                            foreground='white')
        titulo.grid(row=0, column=0, columnspan=2, pady=30)

    def mostrar_formulario(self):
        self.frame_formulario = ttk.Frame(self)

        # Nombre
        nombre_l = ttk.Label(self.frame_formulario, text='Nombre: ')
        nombre_l.grid(row=0, column=0, sticky=tk.W, padx=5, pady=30)
        self.nombre_t = ttk.Entry(self.frame_formulario)
        self.nombre_t.grid(row=0, column=1, padx=5, pady=30)

        # Apellido
        apellido_l = ttk.Label(self.frame_formulario, text='Apellido: ')
        apellido_l.grid(row=1, column=0, sticky=tk.W, padx=5, pady=30)
        self.apellido_t = ttk.Entry(self.frame_formulario)
        self.apellido_t.grid(row=1, column=1, padx=5, pady=30)

        # Membresia
        membresia_l = ttk.Label(self.frame_formulario, text='Membresía: ')
        membresia_l.grid(row=2, column=0, sticky=tk.W, padx=5, pady=30)
        self.membresia_t = ttk.Entry(self.frame_formulario)
        self.membresia_t.grid(row=2, column=1, padx=5, pady=30)

        # Publicar el frame del formulario
        self.frame_formulario.grid(row=1, column=0)

    def cargar_tabla(self):
        # Creamos un frame para mostrar la tabla
        self.frame_tabla = ttk.Frame(self)
        # Definimos los estilos de la tabla
        self.estilos.configure('Treeview', background='black',
                                foreground='white',
                                fieldbackground='black',
                                rowheight=30)  # Altura de las filas en px

        # Definimos las columanas
        columnas = ('Id', 'Nombre', 'Apellido', 'Membresia')

        # Creamos el objeto tabla
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show='headings')

        # Agregar los cabezales de las columnas
        self.tabla.heading('Id', text='Id', anchor=tk.CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tabla.heading('Apellido', text='Apellido', anchor=tk.W)
        self.tabla.heading('Membresia', text='Membresía', anchor=tk.W)

        # Definir las columnas (Registros)
        self.tabla.column('Id', width=50, anchor=tk.CENTER)
        self.tabla.column('Nombre', width=100, anchor=tk.W)
        self.tabla.column('Apellido', width=100, anchor=tk.W)
        self.tabla.column('Membresia', width=100, anchor=tk.W)

        # Cargar los clientes desde la base de datos
        clientes = ClienteDAO.seleccionar()
        for cliente in clientes:
            self.tabla.insert(parent='', index=tk.END,
                                values=(cliente.id, cliente.nombre, cliente.apellido, cliente.membresia))

        # Agregamos el scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)  # Establecer la relacion entre la tabla y el scrollbar
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Asociar el evento SELECT a la tabla
        self.tabla.bind('<<TreeviewSelect>>', self.cargar_cliente)

        # Publicamos la tabla
        self.tabla.grid(row=0, column=0)

        # Mostramos el frame de tabla
        self.frame_tabla.grid(row=1, column=1, padx=20)

    def mostrar_botones(self):
        self.frame_botones = ttk.Frame(self)

        # Creamos los botones ------------------------------------------------------------------------------------------
        # Agregar
        agregar_b = ttk.Button(self.frame_botones, text='Guardar', command=self.validar_cliente)
        agregar_b.grid(row=0, column=0, padx=30)

        # Eliminar
        eliminar_b = ttk.Button(self.frame_botones, text='Eliminar', command=self.eliminar_cliente)
        eliminar_b.grid(row=0, column=2, padx=30)

        # limpiar
        limpiar_b = ttk.Button(self.frame_botones, text='Limpiar', command=self.limpiar_datos)
        limpiar_b.grid(row=0, column=1, padx=30)

        # Estilos de los botones ---------------------------------------------------------------------------------------
        self.estilos.configure('TButton', background='#005f73')
        self.estilos.map('TButton',
                            background=[('active', '#0a9396')],
                            foreground=[('active', 'white')])

        # Publicar el frame de los botones -----------------------------------------------------------------------------
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=20)

    # Metodos de validacion ============================================================================================
    def validar_cliente(self):
        # Validar campos
        if self.nombre_t.get() and self.apellido_t.get() and self.membresia_t.get():
            if self.validar_membresia():
                self.guardar_cliente()
            else:
                messagebox.showerror('Error', 'El valor de membresia NO es numerico')
                self.membresia_t.delete(0, tk.END)
                self.membresia_t.focus_set()  # Enfocar el cursor en el campo membresia
        else:
            messagebox.showerror('Error', 'Todos los campos son requeridos')
            self.nombre_t.focus_set()  # Enfocar el cursor en el campo nombre

    def validar_membresia(self):
        try:
            int(self.membresia_t.get())
            return True
        except:
            return False

    # Metodos de actualizacion =========================================================================================
    def recargar_datos(self):
        # Volver a cargar los datos de la tabla
        self.cargar_tabla()
        # Limpiar los campos del formulario
        self.limpiar_datos()

    def limpiar_formulario(self):
        self.nombre_t.delete(0, tk.END)
        self.apellido_t.delete(0, tk.END)
        self.membresia_t.delete(0, tk.END)
        self.nombre_t.focus_set()

    def cargar_cliente(self, event):
        elemento_seleccionado = self.tabla.selection()[0]
        elemento = self.tabla.item(elemento_seleccionado)
        cliente_tupla = elemento['values']  # Recuperamos los valores de la tupla

        # Recuperar cada valor del cliente
        self.id_cliente = cliente_tupla[0]
        nombre = cliente_tupla[1]
        apellido = cliente_tupla[2]
        membresia = cliente_tupla[3]

        # Limpiar el formulario y Mostrar los datos en el formulario
        self.limpiar_formulario()
        self.nombre_t.insert(0, nombre)
        self.apellido_t.insert(0, apellido)
        self.membresia_t.insert(0, membresia)

    # Metodos de operacion =============================================================================================
    def guardar_cliente(self):
        # Recuperrar los datos del formulario
        nombre = self.nombre_t.get()
        apellido = self.apellido_t.get()
        membresia = int(self.membresia_t.get())

        # Validamos el valor del self.id_cliente
        if self.id_cliente is None:
            # Crear el objeto cliente
            cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)

            # Insertar el cliente en la base de datos
            ClienteDAO.insertar(cliente)
            messagebox.showinfo('Cliente', 'Cliente guardado correctamente')
        else:
            # Actiualizar un registro
            cliente = Cliente(self.id_cliente, nombre=nombre, apellido=apellido, membresia=membresia)
            ClienteDAO.actualizar(cliente)
            messagebox.showinfo('Cliente', 'Cliente actualizado correctamente')

        # vovlemos a mostrar los datos y limpiamos el formulario
        self.recargar_datos()

    def eliminar_cliente(self):
        if self.id_cliente is None:
            messagebox.showerror('Error', 'Seleccione un cliente')
        else:
            cliente = Cliente(self.id_cliente)
            ClienteDAO.eliminar(cliente)
            messagebox.showinfo('Cliente', 'Cliente eliminado correctamente')
            self.recargar_datos()

    def limpiar_datos(self):
        self.limpiar_formulario()
        self.id_cliente = None

    # a

if __name__ == '__main__':
    app = App()
    app.mainloop()