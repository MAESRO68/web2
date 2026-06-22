from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Producto, Pedido
from .forms import ProductoForm, PedidoForm, RegistroForm

# -------------------------
# HOME
# -------------------------
def home(request):
    # Obtener algunos productos destacados o recientes para mostrar en la landing
    productos_recientes = Producto.objects.all().order_by('-id')[:3]
    return render(request, 'productos/home.html', {
        'productos_recientes': productos_recientes
    })


# -------------------------
# CRUD PRODUCTOS (PÚBLICO Y PRIVADO)
# -------------------------
def product_list(request):
    # Parámetros GET
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    disponible = request.GET.get('disponible', '').strip()
    order = request.GET.get('order', 'nombre').strip()
    dir = request.GET.get('dir', 'asc').strip()

    # Query inicial
    productos = Producto.objects.all()

    # Búsqueda por texto (nombre o descripción)
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q)
        )

    # Filtrado por categoría
    if categoria:
        productos = productos.filter(categoria=categoria)

    # Filtrado por disponibilidad en stock
    if disponible == 'si':
        productos = productos.filter(stock__gt=0)
    elif disponible == 'no':
        productos = productos.filter(stock=0)

    # Ordenamiento
    allowed_order_fields = {
        'nombre': 'nombre',
        'precio': 'precio',
        'stock': 'stock',
        'fecha_adquisicion': 'fecha_adquisicion'
    }
    
    order_field = allowed_order_fields.get(order, 'nombre')
    if dir == 'desc':
        order_field = f'-{order_field}'
        
    productos = productos.order_by(order_field)

    # Paginación (10 elementos por página)
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Mantener los parámetros GET para los enlaces de paginación
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    url_params = query_params.urlencode()

    # Opciones de categorías para el formulario de filtrado
    categorias = Producto.CATEGORIAS

    return render(request, 'productos/product_list.html', {
        'page_obj': page_obj,
        'url_params': url_params,
        'categorias': categorias,
        'q': q,
        'categoria_sel': categoria,
        'disponible_sel': disponible,
        'order_sel': order,
        'dir_sel': dir
    })


def product_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/product_detail.html', {
        'producto': producto
    })


@login_required
def product_create(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Acceso denegado. Solo los administradores pueden crear productos.")
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f"El producto '{producto.nombre}' ha sido creado exitosamente.")
            return redirect('product_list')
        else:
            messages.error(request, "Error al crear el producto. Por favor, revisa los campos.")
    else:
        form = ProductoForm()

    return render(request, 'productos/product_form.html', {
        'form': form,
        'title': 'Crear Producto'
    })


@login_required
def product_update(request, pk):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Acceso denegado. Solo los administradores pueden editar productos.")
        return redirect('product_list')

    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f"El producto '{producto.nombre}' ha sido actualizado exitosamente.")
            return redirect('product_detail', pk=producto.pk)
        else:
            messages.error(request, "Error al actualizar el producto. Revisa los datos ingresados.")
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/product_form.html', {
        'form': form,
        'producto': producto,
        'title': 'Editar Producto'
    })


@login_required
def product_delete(request, pk):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Acceso denegado. Solo los administradores pueden eliminar productos.")
        return redirect('product_list')

    producto = get_object_or_404(Producto, pk=pk)
    nombre = producto.nombre
    producto.delete()
    messages.success(request, f"El producto '{nombre}' ha sido eliminado exitosamente.")
    return redirect('product_list')


# -------------------------
# CRUD PEDIDOS (SOLO USUARIOS AUTENTICADOS)
# -------------------------
@login_required
def order_list(request):
    # Si es superusuario, puede ver todos los pedidos, de lo contrario solo los propios
    if request.user.is_superuser:
        pedidos = Pedido.objects.all().order_by('-fecha')
    else:
        pedidos = Pedido.objects.filter(usuario=request.user).order_by('-fecha')
        
    return render(request, 'productos/order_list.html', {
        'pedidos': pedidos
    })


@login_required
def order_detail(request, pk):
    if request.user.is_superuser:
        pedido = get_object_or_404(Pedido, pk=pk)
    else:
        pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
        
    return render(request, 'productos/order_detail.html', {
        'pedido': pedido
    })


@login_required
def order_create(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            
            # Gestionar stock
            producto = pedido.producto
            if producto.stock >= pedido.cantidad:
                producto.stock -= pedido.cantidad
                producto.save()
                pedido.save()
                messages.success(request, f"Pedido del producto '{producto.nombre}' realizado con éxito. Se han descontado {pedido.cantidad} unidades del stock.")
                return redirect('order_list')
            else:
                messages.error(request, "Error: No hay suficiente stock del producto seleccionado.")
        else:
            messages.error(request, "Error en el formulario del pedido. Por favor verifica los datos.")
    else:
        form = PedidoForm()

    return render(request, 'productos/order_form.html', {
        'form': form,
        'title': 'Crear Pedido'
    })


@login_required
def order_update(request, pk):
    if request.user.is_superuser:
        pedido = get_object_or_404(Pedido, pk=pk)
    else:
        pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
        
    cantidad_anterior = pedido.cantidad
    producto_anterior = pedido.producto

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            nuevo_pedido = form.save(commit=False)
            nuevo_producto = nuevo_pedido.producto
            nueva_cantidad = nuevo_pedido.cantidad
            
            # Devolver stock anterior
            producto_anterior.stock += cantidad_anterior
            producto_anterior.save()
            
            # Verificar y descontar nuevo stock
            if nuevo_producto.stock >= nueva_cantidad:
                nuevo_producto.stock -= nueva_cantidad
                nuevo_producto.save()
                nuevo_pedido.save()
                messages.success(request, "El pedido ha sido actualizado correctamente.")
                return redirect('order_list')
            else:
                # Revertir stock del anterior si no hay suficiente para el nuevo
                producto_anterior.stock -= cantidad_anterior
                producto_anterior.save()
                messages.error(request, f"No hay suficiente stock de '{nuevo_producto.nombre}' para actualizar el pedido.")
        else:
            messages.error(request, "Error al actualizar el pedido. Revisa los datos.")
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'productos/order_form.html', {
        'form': form,
        'pedido': pedido,
        'title': 'Editar Pedido'
    })


@login_required
def order_delete(request, pk):
    if request.user.is_superuser:
        pedido = get_object_or_404(Pedido, pk=pk)
    else:
        pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
        
    # Devolver stock
    producto = pedido.producto
    producto.stock += pedido.cantidad
    producto.save()
    
    pedido.delete()
    messages.success(request, f"Pedido #{pk} cancelado. Se han devuelto {pedido.cantidad} unidades de '{producto.nombre}' al stock.")
    return redirect('order_list')


# -------------------------
# AUTENTICACIÓN
# -------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"¡Hola de nuevo, {user.username}! Has iniciado sesión correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, 'productos/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Iniciar sesión automáticamente
            login(request, user)
            messages.success(request, f"¡Registro completado! Bienvenido {user.username} a nuestra plataforma.")
            return redirect('home')
        else:
            messages.error(request, "Error en el registro. Por favor, corrige los errores señalados.")
    else:
        form = RegistroForm()

    return render(request, 'productos/signup.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente. ¡Vuelve pronto!")
    return redirect('home')
