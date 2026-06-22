from django.contrib import admin
from .models import Producto, Pedido

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en el listado del administrador
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'fecha_adquisicion')
    
    # Filtros laterales para agrupar registros rápidamente
    list_filter = ('categoria', 'fecha_adquisicion', 'stock')
    
    # Campos por los que se puede realizar búsquedas
    search_fields = ('nombre', 'descripcion')
    
    # Permitir editar el precio, stock y categoría directamente desde el listado
    list_editable = ('precio', 'stock', 'categoria')
    
    # Criterio de ordenación por defecto
    ordering = ('nombre',)
    
    # Diseño de formularios en pestañas o fieldsets para mayor claridad
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'categoria')
        }),
        ('Inventario y Finanzas', {
            'fields': ('precio', 'stock')
        }),
        ('Fechas', {
            'fields': ('fecha_adquisicion',)
        }),
    )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Columnas mostradas en el panel
    list_display = ('id', 'producto', 'usuario', 'cantidad', 'fecha')
    
    # Filtros del panel
    list_filter = ('fecha', 'usuario', 'producto')
    
    # Campos de búsqueda
    search_fields = ('producto__nombre', 'usuario__username', 'usuario__email')
    
    # Ordenación por defecto (pedidos más recientes primero)
    ordering = ('-fecha',)
    
    # El usuario y el producto se pueden autocompletar o mostrar como de solo lectura en detalle
    readonly_fields = ('fecha',)