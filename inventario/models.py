from django.db import models

class PresentacionProducto(models.Model):
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(
        max_length=150,
        blank=True, 
        null=True
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return self.nombre + ' ' + str(self.descripcion)
    

class Marca(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )
    
    def __str__(self):
        return self.nombre + ' ' + str(self.descripcion)
    


class Categoria(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=150 ,blank=True, null=True)
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return self.nombre + ' ' + str(self.descripcion)
    

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio_venta = models.DecimalField(
        "Precio de venta", 
        max_digits=8, 
        decimal_places=2
    )
    referencia_ubicacion = models.CharField(
        "Referencia de Ubicacion",
        max_length=150,
        blank=True, 
        null=True
    )
    minimo_permitido = models.IntegerField("Cantidad minima permitida")
    presentacion = models.ForeignKey(
        PresentacionProducto,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='productos'
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return self.nombre + ' Q' + str(self.precio_venta)
    


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(
        max_length=150, 
        blank=True, 
        null=True
    )
    email = models.CharField(max_length=100, blank=True, null=True)
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return self.nombre + ' ' + str(self.email)
    


class VisitaProveedor(models.Model):
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    motivo = models.CharField(
        max_length=150,
        blank=True, 
        null=True
    )
    anotaciones = models.CharField(
        max_length=150,
        blank=True, 
        null=True
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        related_name='visitas'
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado'),
            (3,'Atendido')
        ],
        default=1
    )

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.motivo)
    

class Compra(models.Model):
    fecha_hora_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        blank=True, 
        null=True
    )
    observaciones = models.CharField(
        max_length=150,
        blank=True, 
        null=True
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete = models.CASCADE,
        related_name='compras'
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return str(self.fecha_hora_creacion) + ' ' + str(self.total)
    


class Lote(models.Model):
    codigo = models.CharField(max_length=20, blank=True, null=True)
    fecha_vencimiento = models.DateField(
        "Fecha de vencimiento", 
        auto_now=False,  
        null=True
    )
    descripcion = models.CharField(
        max_length=150,
        blank=True, 
        null=True
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='lotes'
    )
    cantidad_comprada = models.IntegerField(default=0)
    costo_unitario = models.DecimalField(
        "Costo Unitario",
        max_digits=8,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='lotes'
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return str(self.codigo) + ' ' + self.producto.nombre + ' ' + str(self.fecha_vencimiento) + ' ' + str(self.descripcion)
    


class Venta(models.Model):
    fecha_hora_creacion = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    observaciones = models.CharField(
        max_length=150,
        blank=True, 
        null=True
    )
    usuario = models.ForeignKey(
        'cuentas.User',
        on_delete=models.CASCADE,
        related_name='ventas'
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return str(self.fecha_hora_creacion) + ' Q' + str(self.total)
    


class DetalleVenta(models.Model):
    cantidad = models.IntegerField()
    precio_venta_real = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True, 
        null=True
    )
    subtotal = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name='detalle_venta'
    )
    lote = models.ForeignKey(
        Lote,
        on_delete=models.CASCADE,
        related_name='detalle_venta'
    )
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return str(self.lote.producto.nombre) + ' ' + str(self.cantidad) + ' Q' + str(self.precio_venta_real)
    


class Transaccion(models.Model):
    monto = models.DecimalField(
        "Monto",
        max_digits=8,
        decimal_places=2,
        blank=True, 
        null=True
    )
    usuario = models.ForeignKey(
        'cuentas.User',
        on_delete=models.CASCADE,
        related_name='transacciones'
    )
    tipo = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Seleccionar Tipo'),
            (1, 'Debito'),
            (2, 'Credito')
        ],
        default=0
    )
    descripcion = models.CharField(max_length=150)
    fecha_hora_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.PositiveSmallIntegerField(
        choices=[
            (0, 'Inactivo'),
            (1, 'Activo'),
            (2, 'Eliminado')
        ],
        default=1
    )

    def __str__(self):
        return str(self.monto) + ' ' + str(self.tipo) + ' ' + str(self.descripcion)
    