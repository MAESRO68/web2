from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Producto, Pedido
from .forms import ProductoForm, PedidoForm, RegistroForm


# -------------------------
# HOME
# -------------------------
def home(request):
    return render(request, 'productos/home.html')


# -------------------------
# CRUD PRODUCTOS
# -------------------------
@login_required
def product_list(request):
    productos = Producto.objects.all()
    return render(request, 'productos/product_list.html', {
        'productos': productos
    })


@login_required
def product_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/product_detail.html', {
        'producto': producto
    })


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductoForm()

    return render(request, 'productos/product_form.html', {
        'form': form
    })


@login_required
def product_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/product_form.html', {
        'form': form
    })


@login_required
def product_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('product_list')


# -------------------------
# CRUD PEDIDOS
# -------------------------
@login_required
def order_list(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'productos/order_list.html', {
        'pedidos': pedidos
    })


@login_required
def order_detail(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
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
            pedido.save()
            return redirect('order_list')
    else:
        form = PedidoForm()

    return render(request, 'productos/order_form.html', {
        'form': form
    })


@login_required
def order_update(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'productos/order_form.html', {
        'form': form
    })


@login_required
def order_delete(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    pedido.delete()
    return redirect('order_list')


# -------------------------
# AUTENTICACIÓN
# -------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'productos/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'productos/signup.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    return redirect('home')
