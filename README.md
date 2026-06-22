# Portal de Gestión de Inventario & Pedidos (Antigravity Stock)

Este proyecto es una aplicación web Django ampliada que implementa un catálogo público de productos con búsqueda, filtrado por categorías y stock, ordenación de columnas y paginación persistente. También incluye formularios de registro y autenticación para restringir operaciones de modificación (creación, edición y eliminación de productos y pedidos) a usuarios autenticados.

---

## Características de la Aplicación

1. **Catálogo de Productos**:
   - Acceso público para visualizar productos y sus detalles.
   - Búsqueda por texto libre sobre el nombre y la descripción.
   - Filtrado por categoría y disponibilidad en stock (en stock / agotado).
   - Ordenación dinámica por nombre, precio, stock y fecha de adquisición (ascendente y descendente), con indicadores visuales en la interfaz.
   - Paginación persistente (10 productos por página) que conserva el estado de filtros, búsquedas y orden.

2. **Gestión de Pedidos**:
   - Registro de pedidos vinculados a usuarios autenticados.
   - Gestión inteligente de stock: al realizar un pedido, se descuenta la cantidad solicitada automáticamente. Al cancelarlo, se reintegra al inventario.
   - Validación para evitar pedidos de cantidades superiores al stock disponible.
   - Los usuarios comunes solo pueden gestionar sus propios pedidos, mientras que el superusuario puede gestionarlos todos.

3. **Seguridad y Formularios**:
   - Validación personalizada en formularios (precios mayores que 0, stock no negativo y fechas de adquisición no futuras).
   - Restricción de accesos mediante decoradores y verificación de seguridad.
   - Mensajes dinámicos de éxito y error en pantalla (`django.contrib.messages`).

4. **Administración de Django Mejorada**:
   - Búsquedas, filtros rápidos laterales, paginación y edición directa "en línea" (inline) de precios, stock y categorías de productos desde la lista principal del administrador.

---

## Cómo Ejecutar el Proyecto

### Requisitos Previos
* Python 3.10 o superior instalado en el sistema.

### Pasos de Despliegue

1. **Crear e inicializar el Entorno Virtual** (si no está creado):
   ```bash
   # En Windows
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. **Instalar Dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Nota: Asegúrate de tener Django instalado, por lo general incluido en el archivo `requirements.txt`).*

3. **Ejecutar las Migraciones de Base de Datos**:
   ```bash
   python manage.py migrate
   ```

4. **Crear un Superusuario de Prueba** (para acceder al administrador):
   ```bash
   python manage.py createsuperuser
   ```
   Sigue las instrucciones en consola para ingresar nombre de usuario, correo electrónico y contraseña.

5. **Iniciar el Servidor de Desarrollo**:
   ```bash
   python manage.py runserver
   ```
   La aplicación estará disponible en: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Cuentas de Acceso y Pruebas

* **Panel de Administración**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* **Usuarios de Prueba**:
  * Puedes registrarte directamente mediante el botón **"Registrarse"** de la barra de navegación para crear un usuario de pruebas estándar.
  * También puedes usar la consola con `createsuperuser` para crear una cuenta con privilegios administrativos.

---

## Ejemplos de URLs de Prueba con Parámetros

El catálogo de productos en `/productos/` admite combinaciones avanzadas de parámetros GET. A continuación se listan ejemplos:

1. **Búsqueda sencilla**:
   - `http://127.0.0.1:8000/productos/?q=teclado`
2. **Filtrar por categoría y ordenar por precio descendente**:
   - `http://127.0.0.1:8000/productos/?categoria=electronica&order=precio&dir=desc`
3. **Buscar, filtrar por stock disponible y ordenar por stock ascendente**:
   - `http://127.0.0.1:8000/productos/?q=auriculares&disponible=si&order=stock&dir=asc`
4. **Paginación combinada con búsquedas y orden**:
   - `http://127.0.0.1:8000/productos/?q=oficina&categoria=hogar&order=nombre&dir=asc&page=2`

---
*Desarrollado y ampliado por Angel Ramos - 2026*