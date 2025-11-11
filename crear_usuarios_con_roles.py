# Importamos los modelos necesarios
from django.contrib.auth.models import User
from tienda.models import PerfilUsuario

def crear_usuario_con_perfil(username, password, rol, departamento):
    """
    Función para crear un usuario con su perfil de tienda.
    """
    # Evita crear el usuario si ya existe (para poder correr el script varias veces)
    if User.objects.filter(username=username).exists():
        print(f"El usuario '{username}' ya existe. No se ha modificado.")
        return

    # 1. Crear el objeto User (para el login)
    # create_user se encarga de hashear (proteger) la contraseña
    user = User.objects.create_user(username=username, password=password)
    
    # 2. Crear el PerfilUsuario (para el rol)
    PerfilUsuario.objects.create(
        user=user,
        rol=rol,
        departamento=departamento
    )
    
    print(f"Usuario '{username}' (Rol: {rol}) creado exitosamente.")

# --- INICIO DEL SCRIPT ---
# Aquí se crean los 3 usuarios que pide tu guía

print("Iniciando creación de usuarios...")

crear_usuario_con_perfil(
    username='vendedor1', 
    password='vendedor123', 
    rol='vendedor', 
    departamento='Ventas'
)

crear_usuario_con_perfil(
    username='gerente1', 
    password='gerente123', 
    rol='gerente', 
    departamento='Gerencia'
)

crear_usuario_con_perfil(
    username='admin1', 
    password='admin123', 
    rol='administrador', 
    departamento='Sistemas'
)

print("\n--- Proceso de creación de usuarios finalizado ---")