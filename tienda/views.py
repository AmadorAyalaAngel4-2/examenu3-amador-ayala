# tienda/views.py
from django.shortcuts import render, redirect, get_object_or_404 # Funciones comunes para renderizar, redirigir y obtener objetos.
from django.contrib.auth.decorators import login_required, permission_required # Decoradores para requerir autenticación y permisos.
from django.contrib.auth.views import LoginView, LogoutView # Vistas predefinidas de Django para autenticación.
from django.urls import reverse_lazy # Función para obtener URLs de forma perezosa.
from django.contrib.auth.models import Group # Modelo para gestionar grupos/roles de usuarios.
from django.contrib import messages # Módulo para enviar mensajes de notificación al usuario.
from .models import Producto, Categoria # Importa los modelos necesarios.
from .forms import ProductoForm # Importa el formulario de Producto.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Producto, Categoria, Proveedor, Cliente, PerfilUsuario, Venta
from .forms import ProductoForm, CategoriaForm, ProveedorForm, ClienteForm
from django.db.models import Sum
from django.utils import timezone


# ============ DECORADOR PERSONALIZADO PARA PERMISOS POR ROL ============
def rol_requerido(*roles_permitidos):
    """
    Decorador personalizado que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
        @rol_requerido('gerente', 'administrador')
        def mi_vista(request):
            ...
    
    Parámetros:
        *roles_permitidos: Lista de roles que pueden acceder a la vista
                          Opciones: 'vendedor', 'gerente', 'administrador'
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # 1. Verificar si el usuario está autenticado
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder')
                return redirect('login')
            
            # 2. Si es superusuario, permitir acceso siempre
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # 3. Verificar si el usuario tiene perfil con rol asignado
            try:
                perfil = request.user.perfil  # Obtener perfil del usuario
                # 4. Verificar si su rol está en los roles permitidos
                if perfil.rol in roles_permitidos:
                    return view_func(request, *args, **kwargs)  # Permitir acceso
                else:
                    # Mostrar mensaje de error indicando roles necesarios
                    roles_texto = ', '.join([r.capitalize() for r in roles_permitidos])
                    messages.error(request, f'⚠️ Acceso denegado. Se requiere rol: {roles_texto}')
                    return redirect('home')  # Redirigir al home
            except PerfilUsuario.DoesNotExist:
                # Si el usuario no tiene perfil asignado
                messages.error(request, '⚠️ Tu cuenta no tiene un perfil asignado. Contacta al administrador.')
                return redirect('home')
        
        return _wrapped_view
    return decorator


# ============ VISTA DE LOGIN ============
def login_view(request):
    """Vista para el inicio de sesión de usuarios"""
    # Si el usuario ya está autenticado, redirigir al home
    if request.user.is_authenticated:
        return redirect('home')
    
    # Si el método es POST, procesamos el formulario de login
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # Creamos el formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido
            username = form.cleaned_data.get('username')  # Obtenemos el nombre de usuario
            password = form.cleaned_data.get('password')  # Obtenemos la contraseña
            user = authenticate(username=username, password=password)  # Autenticamos al usuario
            if user is not None:  # Si la autenticación fue exitosa
                login(request, user)  # Iniciamos sesión
                messages.success(request, f'Bienvenido {username}!')  # Mensaje de bienvenida
                return redirect('home')  # Redirigimos al home
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')  # Mensaje de error
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')  # Mensaje de error si el formulario no es válido
    else:
        form = AuthenticationForm()  # Si es GET, creamos un formulario vacío
    
    return render(request, 'tienda/login.html', {'form': form})  # Renderizamos el template de login


# ============ VISTA DE LOGOUT ============
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)  # Cerramos la sesión del usuario
    messages.info(request, 'Sesión cerrada correctamente')  # Mensaje informativo
    return redirect('login')  # Redirigimos al login


# ============ VISTA PRINCIPAL (HOME) ============
@login_required  # Decorador que requiere autenticación para acceder a esta vista
def home(request):
    """Vista principal que muestra el dashboard con estadísticas"""
    
    # --- OBTENER FECHA DE HOY (LA PARTE IMPORTANTE) ---
    today = timezone.now().date()  # <-- Aquí se define 'today' como solo la fecha

    # --- CONSULTAS DE ESTADÍSTICAS ---
    
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_proveedores = Proveedor.objects.count()
    total_clientes = Cliente.objects.count()
    
    ventas_de_hoy = Venta.objects.filter(fecha_venta__date=today)
    
    total_ventas_hoy = ventas_de_hoy.aggregate(
        total_sum=Sum('total')
    ).get('total_sum') or 0.00
    
    conteo_ventas_hoy = ventas_de_hoy.count()
    
    productos_recientes = Producto.objects.order_by('-fecha_creacion')[:5]
    
    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_proveedores': total_proveedores,
        'total_clientes': total_clientes,
        'productos_recientes': productos_recientes,
        'total_ventas_hoy': total_ventas_hoy,
        'conteo_ventas_hoy': conteo_ventas_hoy,
    }
    
    return render(request, 'tienda/home.html', context)

# ============ VISTAS CRUD PARA PRODUCTOS ============
@login_required
def producto_lista(request):
    """Vista que lista todos los productos"""
    productos = Producto.objects.all()  # Obtenemos todos los productos de la base de datos
    return render(request, 'tienda/producto_lista.html', {'productos': productos})  # Renderizamos template con la lista


@login_required
@rol_requerido('gerente', 'administrador')
def producto_crear(request):
    """Vista para crear un nuevo producto"""
    if request.method == 'POST':  # Si se envió el formulario
        form = ProductoForm(request.POST)  # Creamos el formulario con los datos enviados
        if form.is_valid():  # Si el formulario es válido (todos los campos correctos)
            form.save()  # Guardamos el producto en la base de datos
            messages.success(request, 'Producto creado exitosamente')  # Mensaje de éxito
            return redirect('producto_lista')  # Redirigimos a la lista de productos
    else:
        form = ProductoForm()  # Si es GET, creamos un formulario vacío
    
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Crear'})  # Renderizamos el formulario


@login_required
@rol_requerido('gerente', 'administrador')  # Solo Gerente y Administrador pueden editar
def producto_editar(request, pk):
    """Vista para editar un producto existente"""
    producto = get_object_or_404(Producto, pk=pk)  # Obtenemos el producto por su ID (Primary Key), si no existe muestra 404
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)  # Creamos el formulario con los datos del producto existente
        if form.is_valid():
            form.save()  # Guardamos los cambios
            messages.success(request, 'Producto actualizado exitosamente')
            return redirect('producto_lista')
    else:
        form = ProductoForm(instance=producto)  # Mostramos el formulario con los datos actuales del producto
    
    return render(request, 'tienda/producto_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador')  # Solo Administrador puede eliminar
def producto_eliminar(request, pk):
    """Vista para eliminar un producto"""
    producto = get_object_or_404(Producto, pk=pk)  # Obtenemos el producto
    if request.method == 'POST':  # Confirmación de eliminación debe ser POST por seguridad
        producto.delete()  # Eliminamos el producto de la base de datos
        messages.success(request, 'Producto eliminado exitosamente')
        return redirect('producto_lista')
    
    return render(request, 'tienda/producto_eliminar.html', {'producto': producto})  # Mostramos página de confirmación


# ============ VISTAS CRUD PARA CATEGORÍAS ============
@login_required
@rol_requerido('gerente', 'administrador')  # Vendedor NO puede ver categorías
def categoria_lista(request):
    """Vista que lista todas las categorías"""
    categorias = Categoria.objects.all()
    return render(request, 'tienda/categoria_lista.html', {'categorias': categorias})


@login_required
@rol_requerido('gerente', 'administrador')  # Solo Gerente y Administrador
def categoria_crear(request):
    """Vista para crear una nueva categoría"""
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('categoria_lista')
    else:
        form = CategoriaForm()
    
    return render(request, 'tienda/categoria_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('gerente', 'administrador')
def categoria_editar(request, pk):
    """Vista para editar una categoría existente"""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('categoria_lista')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'tienda/categoria_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador')  # Solo Administrador
def categoria_eliminar(request, pk):
    """Vista para eliminar una categoría"""
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('categoria_lista')
    
    return render(request, 'tienda/categoria_eliminar.html', {'categoria': categoria})


# ============ VISTAS CRUD PARA PROVEEDORES ============
@login_required
@rol_requerido('gerente', 'administrador')  # Vendedor NO puede ver proveedores
def proveedor_lista(request):
    """Vista que lista todos los proveedores"""
    proveedores = Proveedor.objects.all()
    return render(request, 'tienda/proveedor_lista.html', {'proveedores': proveedores})


@login_required
@rol_requerido('gerente', 'administrador')  # Solo Gerente y Administrador
def proveedor_crear(request):
    """Vista para crear un nuevo proveedor"""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado exitosamente')
            return redirect('proveedor_lista')
    else:
        form = ProveedorForm()
    
    return render(request, 'tienda/proveedor_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('gerente', 'administrador')
def proveedor_editar(request, pk):
    """Vista para editar un proveedor existente"""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente')
            return redirect('proveedor_lista')
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'tienda/proveedor_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador')
def proveedor_eliminar(request, pk):
    """Vista para eliminar un proveedor"""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente')
        return redirect('proveedor_lista')
    
    return render(request, 'tienda/proveedor_eliminar.html', {'proveedor': proveedor})


# ============ VISTAS CRUD PARA CLIENTES ============
@login_required
def cliente_lista(request):
    """Vista que lista todos los clientes"""
    clientes = Cliente.objects.all()
    return render(request, 'tienda/cliente_lista.html', {'clientes': clientes})


@login_required
@rol_requerido('gerente', 'administrador')
def cliente_crear(request):
    """Vista para crear un nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('cliente_lista')
    else:
        form = ClienteForm()
    
    return render(request, 'tienda/cliente_form.html', {'form': form, 'accion': 'Crear'})


@login_required
@rol_requerido('gerente', 'administrador')
def cliente_editar(request, pk):
    """Vista para editar un cliente existente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente')
            return redirect('cliente_lista')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'tienda/cliente_form.html', {'form': form, 'accion': 'Editar'})


@login_required
@rol_requerido('administrador')
def cliente_eliminar(request, pk):
    """Vista para eliminar un cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('cliente_lista')
    
    return render(request, 'tienda/cliente_eliminar.html', {'cliente': cliente})