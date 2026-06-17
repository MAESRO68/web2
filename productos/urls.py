from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Productos CRUD
    path('productos/', views.product_list, name='product_list'),
    path('productos/<int:pk>/', views.product_detail, name='product_detail'),
    path('productos/crear/', views.product_create, name='product_create'),
    path('productos/<int:pk>/editar/', views.product_update, name='product_update'),
    path('productos/<int:pk>/eliminar/', views.product_delete, name='product_delete'),

    # Pedidos CRUD
    path('pedidos/', views.order_list, name='order_list'),
    path('pedidos/<int:pk>/', views.order_detail, name='order_detail'),
    path('pedidos/crear/', views.order_create, name='order_create'),
    path('pedidos/<int:pk>/editar/', views.order_update, name='order_update'),
    path('pedidos/<int:pk>/eliminar/', views.order_delete, name='order_delete'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]
