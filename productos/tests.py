from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Producto
from .forms import ProductoForm, PedidoForm

class ProductoFormTestCase(TestCase):
    def test_form_validation_valid_data(self):
        # Datos correctos
        data = {
            'nombre': 'Teclado Mecánico',
            'descripcion': 'Teclado RGB con switches red',
            'precio': 79.99,
            'stock': 15,
            'categoria': 'electronica',
            'fecha_adquisicion': date.today()
        }
        form = ProductoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_validation_negative_price(self):
        # Precio negativo debe fallar
        data = {
            'nombre': 'Raton Gaming',
            'descripcion': 'Raton con 12000 DPI',
            'precio': -5.00,
            'stock': 10,
            'categoria': 'electronica',
            'fecha_adquisicion': date.today()
        }
        form = ProductoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('precio', form.errors)

    def test_form_validation_negative_stock(self):
        # Stock negativo debe fallar
        data = {
            'nombre': 'Raton Gaming',
            'descripcion': 'Raton con 12000 DPI',
            'precio': 12.50,
            'stock': -1,
            'categoria': 'electronica',
            'fecha_adquisicion': date.today()
        }
        form = ProductoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_form_validation_future_date(self):
        # Fecha futura debe fallar
        future_date = date.today() + timedelta(days=5)
        data = {
            'nombre': 'Auriculares Pro',
            'descripcion': 'Sonido envolvente 7.1',
            'precio': 99.90,
            'stock': 5,
            'categoria': 'electronica',
            'fecha_adquisicion': future_date
        }
        form = ProductoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_adquisicion', form.errors)


class PedidoFormTestCase(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Mesa Escritorio',
            descripcion='Mesa de madera para oficina',
            precio=120.00,
            stock=5,
            categoria='hogar',
            fecha_adquisicion=date.today()
        )

    def test_pedido_valid_quantity(self):
        data = {
            'producto': self.producto.id,
            'cantidad': 3
        }
        form = PedidoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_pedido_insufficient_stock(self):
        # Pedir más del stock disponible (5) debe fallar
        data = {
            'producto': self.producto.id,
            'cantidad': 10
        }
        form = PedidoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad', form.errors)
        self.assertEqual(
            form.errors['cantidad'][0],
            f"No hay suficiente stock. El stock actual de {self.producto.nombre} es {self.producto.stock}."
        )

    def test_pedido_negative_quantity(self):
        # Pedir cantidad negativa o cero debe fallar
        data = {
            'producto': self.producto.id,
            'cantidad': 0
        }
        form = PedidoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('cantidad', form.errors)
