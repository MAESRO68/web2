from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    CATEGORIAS = [
        ('electronica', 'Electrónica'),
        ('hogar', 'Hogar y Cocina'),
        ('moda', 'Moda'),
        ('deportes', 'Deportes'),
        ('libros', 'Libros'),
        ('otros', 'Otros'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='otros', verbose_name="Categoría")
    fecha_adquisicion = models.DateField(null=True, blank=True, verbose_name="Fecha de adquisición")

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
