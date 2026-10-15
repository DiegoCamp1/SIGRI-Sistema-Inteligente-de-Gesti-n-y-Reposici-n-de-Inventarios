"""Menú y pantallas de SIGRI."""
import tkinter as tk
from tkinter import ttk, messagebox

from modelo.producto import Producto
from reportes.reporte_general import ReporteGeneral
from reportes.reporte_individual import ReporteIndividual
from modelo.excepciones import SKUDuplicadoError, ProductoNoEncontradoError


def convertir_cantidades(valores):
    """Convierte los cinco campos del formulario, sin aceptar decimales."""
    cantidades = []
    for campo, texto in valores:
        try:
            cantidades.append(int(texto.strip()))
        except (ValueError, AttributeError):
            raise ValueError(campo + " debe ser un número entero (por ejemplo, 10).") from None
    return cantidades


class InterfazSIGRI:
    CAMPOS = [
        ("sku", "SKU"), ("nombre", "Nombre del producto"),
        ("stock_inicial", "Stock inicial"), ("ventas", "Ventas del periodo"),
        ("mermas", "Mermas del periodo"), ("stock_minimo", "Stock mínimo"),
        ("stock_maximo", "Stock máximo"),
    ]

    def __init__(self, inventario, ventana=None):
        self.inventario = inventario
        self.ventana = ventana if ventana is not None else tk.Tk()
        self.ventana.title("SIGRI | Servimarsa Perú")
        self.ventana.geometry("1120x760")
        self.ventana.minsize(1000, 700)
        self.ventana.configure(bg="#f1f5f9")
        self.ventana.protocol("WM_DELETE_WINDOW", self.salir)
        self._configurar_estilos()
        self._construir_base()
        self.mostrar_menu()

    def _configurar_estilos(self):
        estilo = ttk.Style(self.ventana)
        estilo.theme_use("clam")
        estilo.configure("TFrame", background="#f1f5f9")
        estilo.configure("Card.TFrame", background="white")
        estilo.configure("TLabel", background="#f1f5f9", foreground="#24344b",
                         font=("Segoe UI", 10))
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 22, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 12, "bold"))
        estilo.configure("Card.TLabel", background="white")
        estilo.configure("Valor.TLabel", background="white", foreground="#075985",
                         font=("Segoe UI", 26, "bold"))
        estilo.configure("TButton", font=("Segoe UI", 10), padding=(12, 9))
        estilo.configure("Principal.TButton", background="#0369a1", foreground="white")
        estilo.map("Principal.TButton", background=[("active", "#075985")])
        estilo.configure("TEntry", padding=7, font=("Segoe UI", 11))
        estilo.configure("Treeview", rowheight=32, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=8)
        estilo.map("Treeview", background=[("selected", "#075985")],
                   foreground=[("selected", "white")])

    def _construir_base(self):
        self.ventana.columnconfigure(1, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        barra = tk.Frame(self.ventana, bg="#0f223b", width=235)
        barra.grid(row=0, column=0, sticky="nsew")
        barra.grid_propagate(False)
        tk.Label(barra, text="SIGRI", font=("Segoe UI", 27, "bold"),
                 fg="white", bg="#0f223b").pack(anchor="w", padx=22, pady=(28, 0))
        tk.Label(barra, text="Servimarsa Perú\nGestión y reposición", justify="left",
                 font=("Segoe UI", 11), fg="#afc9df", bg="#0f223b").pack(
                     anchor="w", padx=24, pady=(6, 28))
        opciones = [
            ("1  Registrar producto", self.mostrar_registro),
            ("2  Buscar producto", self.mostrar_busqueda),
            ("3  Listar inventario", self.mostrar_inventario),
            ("4  Productos críticos", self.mostrar_criticos),
            ("5  Resultado individual", self.mostrar_selector_individual),
            ("6  Reporte general", self.mostrar_general),
            ("7  Salir", self.salir),
        ]
        for texto, accion in opciones:
            tk.Button(barra, text=texto, command=accion, anchor="w", relief="flat",
                      bg="#17324f", fg="white", activebackground="#245479",
                      activeforeground="white", font=("Segoe UI", 10), cursor="hand2",
                      padx=12, pady=12).pack(fill="x", padx=14, pady=4)
        tk.Label(barra, text="Datos en memoria\nSe borran al cerrar la sesión.",
                 justify="left", wraplength=195, bg="#0f223b", fg="#afc9df",
                 font=("Segoe UI", 10)).pack(side="bottom", anchor="w", padx=22, pady=24)
        self.contenido = ttk.Frame(self.ventana, padding=24)
        self.contenido.grid(row=0, column=1, sticky="nsew")
        self.estado = tk.StringVar(master=self.ventana)
        ttk.Label(self.ventana, textvariable=self.estado, padding=(18, 8)).grid(
            row=1, column=0, columnspan=2, sticky="ew")

    # La navegación conserva el inventario de la sesión.
    def _vista(self, titulo, descripcion):
        for widget in self.contenido.winfo_children():
            widget.destroy()
        self.vista_actual = titulo
        cabecera = ttk.Frame(self.contenido)
        cabecera.pack(fill="x", pady=(0, 10))
        ttk.Label(cabecera, text=titulo, style="Titulo.TLabel").pack(side="left")
        ttk.Button(cabecera, text="Volver al menú", command=self.mostrar_menu).pack(side="right")
        ttk.Label(self.contenido, text=descripcion, wraplength=720).pack(
            anchor="w", pady=(0, 18))
        self.estado.set("Sesión activa · Productos registrados: " +
                        str(len(self.inventario.listar_productos())))

    def _tarjetas(self, datos):
        fila = ttk.Frame(self.contenido)
        fila.pack(fill="x", pady=(0, 16))
        for columna, (titulo, valor) in enumerate(datos):
            fila.columnconfigure(columna, weight=1, uniform="tarjetas")
            tarjeta = ttk.Frame(fila, style="Card.TFrame", padding=16)
            tarjeta.grid(row=0, column=columna, sticky="nsew", padx=(0, 10))
            ttk.Label(tarjeta, text=titulo, style="Card.TLabel").pack(anchor="w")
            ttk.Label(tarjeta, text=str(valor), style="Valor.TLabel").pack(anchor="w", pady=(5, 0))

    def mostrar_menu(self):
        self._vista("Control del inventario", "Registra productos y consulta las necesidades de reposición del periodo.")
        datos = self.inventario.generar_reporte(ReporteGeneral())
        self._tarjetas([("Productos", datos["total_productos"]),
                        ("Productos críticos", datos["productos_criticos"]),
                        ("Unidades por comprar", datos["total_compra"])])
        panel = ttk.Frame(self.contenido, style="Card.TFrame", padding=24)
        panel.pack(fill="x", pady=8)
        ttk.Label(panel, text="Comienza con un producto", style="Card.TLabel",
                  font=("Segoe UI", 15, "bold")).pack(anchor="w")
        ttk.Label(panel, text="Ingresa SKU, nombre, stock inicial, ventas, mermas y límites de stock.\n"
                  "Cada registro representa un producto en el mismo periodo de análisis.",
                  style="Card.TLabel", wraplength=660).pack(anchor="w", pady=14)
        ttk.Button(panel, text="Registrar producto", style="Principal.TButton",
                   command=self.mostrar_registro).pack(anchor="w")
        ttk.Label(self.contenido, text="¿Cómo se calcula?", style="Subtitulo.TLabel").pack(
            anchor="w", pady=(24, 10))
        ttk.Label(self.contenido, text="Stock actualizado = inicial − ventas − mermas.\n"
                  "Si el stock actualizado es menor o igual al mínimo, se solicita reposición\n"
                  "hasta alcanzar el máximo.", wraplength=710).pack(anchor="w")

    # Registro y validación de los datos del formulario chequeado 
    def mostrar_registro(self):
        self._vista("Registrar producto", "Completa todos los campos. Las cantidades son unidades enteras no negativas.")
        formulario = ttk.Frame(self.contenido, style="Card.TFrame", padding=22)
        formulario.pack(fill="x")
        formulario.columnconfigure(1, weight=1)
        self.entradas = {}
        for fila, (clave, etiqueta) in enumerate(self.CAMPOS):
            ttk.Label(formulario, text=etiqueta, style="Card.TLabel").grid(
                row=fila, column=0, sticky="w", padx=(0, 28), pady=7)
            entrada = ttk.Entry(formulario)
            entrada.grid(row=fila, column=1, sticky="ew", pady=7)
            entrada.bind("<Return>", lambda evento: self.registrar())
            self.entradas[clave] = entrada
        botones = ttk.Frame(self.contenido)
        botones.pack(fill="x", pady=18)
        ttk.Button(botones, text="Registrar y ver resultado", style="Principal.TButton",
                   command=self.registrar).pack(side="left")
        ttk.Button(botones, text="Limpiar formulario", command=self.limpiar_formulario).pack(side="left", padx=10)
        ttk.Label(self.contenido, text="Ventas + mermas no pueden superar el stock inicial.\n"
                  "El máximo debe ser mayor que el mínimo. El SKU no puede repetirse.",
                  wraplength=710).pack(anchor="w")
        self.entradas["sku"].focus_set()

    def limpiar_formulario(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        self.entradas["sku"].focus_set()

    def registrar(self):
        try:
            campos = []
            for clave, etiqueta in self.CAMPOS[2:]:
                campos.append((etiqueta, self.entradas[clave].get()))
            cantidades = convertir_cantidades(campos)
            producto = Producto(self.entradas["sku"].get(), self.entradas["nombre"].get(), *cantidades)
            self.inventario.registrar_producto(producto)
        except (ValueError, SKUDuplicadoError) as error:
            messagebox.showerror("Revisa los datos", str(error), parent=self.ventana)
            return  # El formulario conserva todas sus entradas.
        self.mostrar_individual(producto.sku)
        self.estado.set("Producto " + producto.sku + " registrado correctamente.")

    # Tabla compartida por inventario, búsqueda y productos críticos.
    def _crear_tabla(self):
        marco = ttk.Frame(self.contenido)
        marco.pack(fill="both", expand=True, pady=(0, 12))
        marco.columnconfigure(0, weight=1)
        marco.rowconfigure(0, weight=1)
        columnas = ("sku", "nombre", "stock", "estado", "compra")
        self.tabla = ttk.Treeview(marco, columns=columnas, show="headings", selectmode="browse")
        for clave, titulo, ancho in [
            ("sku", "SKU", 105), ("nombre", "Producto", 180),
            ("stock", "Stock actual", 90), ("estado", "Estado", 195),
            ("compra", "Por comprar", 100),
        ]:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, minwidth=ancho, stretch=clave == "nombre",
                              anchor="w" if clave in ("sku", "nombre", "estado") else "center")
        self.tabla.tag_configure("critico", background="#fff1e8", foreground="#9a3412")
        self.tabla.tag_configure("suficiente", background="#f0fdf4", foreground="#166534")
        self.tabla.grid(row=0, column=0, sticky="nsew")
        vertical = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal = ttk.Scrollbar(marco, orient="horizontal", command=self.tabla.xview)
        horizontal.grid(row=1, column=0, sticky="ew")
        self.tabla.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.tabla.bind("<Double-1>", lambda evento: self.ver_seleccionado())
        self.mensaje_tabla = tk.StringVar(master=self.ventana)
        ttk.Label(self.contenido, textvariable=self.mensaje_tabla).pack(anchor="w")
        ttk.Button(self.contenido, text="Ver resultado del seleccionado",
                   command=self.ver_seleccionado).pack(anchor="w", pady=12)

    def _llenar_tabla(self, productos, vacio):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)
        for producto in productos:
            critico = producto.requiere_reposicion()
            self.tabla.insert("", "end", values=(
                producto.sku, producto.nombre, producto.calcular_stock_actualizado(),
                "REQUIERE REPOSICIÓN" if critico else "STOCK SUFICIENTE",
                producto.calcular_unidades_por_comprar()),
                tags=("critico" if critico else "suficiente",))
        self.mensaje_tabla.set(str(len(productos)) + " producto(s). Selecciona uno para consultar su resultado."
                               if productos else vacio)

    def ver_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showinfo("Selecciona un producto", "Selecciona una fila de la tabla.", parent=self.ventana)
            return
        sku = self.tabla.item(seleccion[0], "values")[0]
        self.mostrar_individual(sku)

    def mostrar_inventario(self):
        self._vista("Inventario", "Consulta el stock calculado y las unidades por comprar de todos los productos.")
        self._crear_tabla()
        self._llenar_tabla(self.inventario.listar_productos(), "Todavía no hay productos. Registra el primero desde el menú.")

    def mostrar_criticos(self):
        self._vista("Productos críticos", "Productos cuyo stock actualizado es menor o igual al stock mínimo.")
        self._crear_tabla()
        mensaje = "No hay productos que requieran reposición."
        if not self.inventario.listar_productos():
            mensaje = "Todavía no hay productos registrados."
        self._llenar_tabla(self.inventario.listar_criticos(), mensaje)

    def mostrar_busqueda(self):
        self._vista("Buscar producto", "Busca un SKU exacto o una parte del nombre. Se ignoran mayúsculas y espacios externos.")
        controles = ttk.Frame(self.contenido)
        controles.pack(fill="x", pady=(0, 16))
        self.tipo_busqueda = tk.StringVar(master=self.ventana, value="sku")
        ttk.Radiobutton(controles, text="SKU", variable=self.tipo_busqueda, value="sku").pack(side="left")
        ttk.Radiobutton(controles, text="Nombre", variable=self.tipo_busqueda, value="nombre").pack(side="left", padx=12)
        self.criterio = ttk.Entry(controles)
        self.criterio.pack(side="left", fill="x", expand=True, padx=(0, 12))
        self.criterio.bind("<Return>", lambda evento: self.buscar())
        ttk.Button(controles, text="Buscar", style="Principal.TButton", command=self.buscar).pack(side="left")
        self._crear_tabla()
        self._llenar_tabla([], "Escribe un criterio y pulsa Buscar." if self.inventario.listar_productos()
                           else "Todavía no hay productos registrados.")
        self.criterio.focus_set()

    def buscar(self):
        try:
            productos = self.inventario.buscar_productos(self.criterio.get(), self.tipo_busqueda.get())
        except ValueError as error:
            messagebox.showerror("Revisa la búsqueda", str(error), parent=self.ventana)
            return
        self._llenar_tabla(productos, "No se encontraron productos con ese criterio.")

    def mostrar_selector_individual(self):
        self._vista("Resultado individual", "Selecciona un SKU para ver los datos, el cálculo y la reposición del producto.")
        productos = self.inventario.listar_productos()
        if not productos:
            ttk.Label(self.contenido, text="Todavía no hay productos registrados.").pack(anchor="w")
            ttk.Button(self.contenido, text="Registrar producto", command=self.mostrar_registro).pack(anchor="w", pady=15)
            return
        self.sku_individual = ttk.Combobox(self.contenido, state="readonly", values=[p.sku for p in productos])
        self.sku_individual.pack(anchor="w", pady=(0, 15))
        self.sku_individual.current(0)
        ttk.Button(self.contenido, text="Consultar resultado", style="Principal.TButton",
                   command=lambda: self.mostrar_individual(self.sku_individual.get())).pack(anchor="w")

    def mostrar_individual(self, sku):
        try:
            datos = self.inventario.generar_reporte(ReporteIndividual(sku))
        except (ValueError, ProductoNoEncontradoError) as error:
            messagebox.showerror("No se pudo consultar", str(error), parent=self.ventana)
            return
        self._vista("Resultado individual", "Información del producto y decisión automática de reposición.")
        panel = ttk.Frame(self.contenido, style="Card.TFrame", padding=22)
        panel.pack(fill="x")
        panel.columnconfigure(1, weight=1)
        for fila, (clave, etiqueta) in enumerate(self.CAMPOS):
            ttk.Label(panel, text=etiqueta, style="Card.TLabel").grid(row=fila, column=0, sticky="w", pady=5)
            if clave in ("sku", "nombre"):
                # Texto largo consultable con el cursor, sin aumentar la altura.
                entrada = ttk.Entry(panel)
                entrada.insert(0, str(datos[clave]))
                entrada.configure(state="readonly")
                entrada.grid(row=fila, column=1, sticky="ew", padx=30, pady=5)
            else:
                ttk.Label(panel, text=str(datos[clave]), style="Card.TLabel").grid(
                    row=fila, column=1, sticky="w", padx=30, pady=5)
        self._tarjetas_individuales(datos)
        ttk.Label(self.contenido, text="Cálculo: " + str(datos["stock_inicial"]) + " − " +
                  str(datos["ventas"]) + " − " + str(datos["mermas"]) + " = " +
                  str(datos["stock_actualizado"])).pack(anchor="w", pady=8)
        botones = ttk.Frame(self.contenido)
        botones.pack(fill="x", pady=12)
        ttk.Button(botones, text="Registrar otro producto", command=self.mostrar_registro).pack(side="left")
        ttk.Button(botones, text="Ver inventario", command=self.mostrar_inventario).pack(side="left", padx=10)

    def _tarjetas_individuales(self, datos):
        self._tarjetas([("Stock actualizado", datos["stock_actualizado"]),
                        ("Unidades por comprar", datos["unidades_por_comprar"])])
        critico = datos["requiere_reposicion"]
        tk.Label(self.contenido, text="REQUIERE REPOSICIÓN" if critico else "STOCK SUFICIENTE",
                 bg="#fff1e8" if critico else "#f0fdf4", fg="#9a3412" if critico else "#166534",
                 font=("Segoe UI", 12, "bold"), padx=16, pady=10).pack(fill="x")

    # Indicadores generales y productos con mayor merma.
    def mostrar_general(self):
        self._vista("Reporte general", "Indicadores del periodo. Las cantidades son unidades, no importes monetarios.")
        datos = self.inventario.generar_reporte(ReporteGeneral())
        self._tarjetas([("Productos", datos["total_productos"]),
                        ("Críticos", datos["productos_criticos"]),
                        ("Suficientes", datos["productos_suficientes"])])
        self._tarjetas([("Ventas", datos["total_ventas"]),
                        ("Mermas", datos["total_mermas"]),
                        ("Por comprar", datos["total_compra"])])
        ttk.Label(self.contenido, text="Productos críticos: " + format(datos["porcentaje_critico"], ".2f") + " %",
                  style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 14))
        ttk.Label(self.contenido, text="Mayor merma", style="Subtitulo.TLabel").pack(anchor="w", pady=(0, 8))
        marco = ttk.Frame(self.contenido)
        marco.pack(fill="both", expand=True)
        texto = tk.Text(marco, height=5, wrap="word", font=("Segoe UI", 11), relief="flat",
                        padx=14, pady=12, bg="white", fg="#24344b")
        texto.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(marco, orient="vertical", command=texto.yview)
        scroll.pack(side="right", fill="y")
        texto.configure(yscrollcommand=scroll.set)
        if datos["mayor_merma"] == 0:
            texto.insert("end", "No hay mermas registradas.")
        else:
            texto.insert("end", "Mayor merma: " + str(datos["mayor_merma"]) + " unidades.\n")
            for producto in datos["productos_mayor_merma"]:
                texto.insert("end", producto["sku"] + " · " + producto["nombre"] + "\n")
        texto.configure(state="disabled")
        ttk.Button(self.contenido, text="Ver productos críticos", command=self.mostrar_criticos).pack(anchor="w", pady=16)

    # Confirmación de salida.
    def salir(self):
        confirmar = messagebox.askyesno("Cerrar SIGRI", "¿Quieres salir?\n\nLos datos de esta sesión no se conservarán.",
                                        parent=self.ventana)
        if confirmar:
            self.ventana.destroy()

    def ejecutar(self):
        self.ventana.mainloop()
