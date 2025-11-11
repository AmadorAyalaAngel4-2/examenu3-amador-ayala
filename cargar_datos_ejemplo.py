# Script para cargar datos de ejemplo en la base de datos
# Ejecutar con: python manage.py shell < cargar_datos_ejemplo.py

# Importamos los modelos
from .tienda.models import Categoria, Producto, Proveedor, Cliente

# Limpiamos datos anteriores (opcional)
print("Limpiando datos anteriores...")
Producto.objects.all().delete()
Categoria.objects.all().delete()
Proveedor.objects.all().delete()
Cliente.objects.all().delete()

# ============ CREAR CATEGORÍAS ============
print("\nCreando categorías...")
cat_electronica = Categoria.objects.create(
    nombre="Electrónica",
    descripcion="Productos electrónicos y tecnología"
)
print(f"✓ Categoría creada: {cat_electronica.nombre}")

cat_ropa = Categoria.objects.create(
    nombre="Ropa",
    descripcion="Prendas de vestir y accesorios"
)
print(f"✓ Categoría creada: {cat_ropa.nombre}")

cat_alimentos = Categoria.objects.create(
    nombre="Alimentos",
    descripcion="Productos alimenticios"
)
print(f"✓ Categoría creada: {cat_alimentos.nombre}")

cat_hogar = Categoria.objects.create(
    nombre="Hogar",
    descripcion="Artículos para el hogar"
)
print(f"✓ Categoría creada: {cat_hogar.nombre}")

# ============ CREAR PRODUCTOS ============
print("\nCreando productos...")

# Productos de Electrónica
Producto.objects.create(
    nombre="Laptop HP Pavilion",
    descripcion="Laptop HP con procesador Intel Core i5, 8GB RAM, 256GB SSD",
    precio_venta=12999.99,
    stock=15,
    categoria=cat_electronica,
    activo=True
)

Producto.objects.create(
    nombre="Mouse Inalámbrico Logitech",
    descripcion="Mouse inalámbrico con sensor óptico de alta precisión",
    precio_venta=299.50,
    stock=50,
    categoria=cat_electronica,
    activo=True
)

Producto.objects.create(
    nombre="Teclado Mecánico RGB",
    descripcion="Teclado mecánico gaming con iluminación RGB",
    precio_venta=899.00,
    stock=30,
    categoria=cat_electronica,
    activo=True
)

# Productos de Ropa
Producto.objects.create(
    nombre="Playera Polo Azul",
    descripcion="Playera polo de algodón 100%, talla M",
    precio_venta=349.99,
    stock=100,
    categoria=cat_ropa,
    activo=True
)

Producto.objects.create(
    nombre="Jeans Mezclilla",
    descripcion="Pantalón de mezclilla corte recto",
    precio_venta=599.00,
    stock=75,
    categoria=cat_ropa,
    activo=True
)

# Productos de Alimentos
Producto.objects.create(
    nombre="Café Gourmet 500g",
    descripcion="Café molido gourmet, tostado medio",
    precio_venta=189.90,
    stock=200,
    categoria=cat_alimentos,
    activo=True
)

Producto.objects.create(
    nombre="Galletas de Chocolate",
    descripcion="Paquete de galletas con chispas de chocolate",
    precio_venta=45.50,
    stock=150,
    categoria=cat_alimentos,
    activo=True
)

# Productos de Hogar
Producto.objects.create(
    nombre="Sartén Antiadherente",
    descripcion="Sartén de 28cm con recubrimiento antiadherente",
    precio_venta=399.00,
    stock=40,
    categoria=cat_hogar,
    activo=True
)

Producto.objects.create(
    nombre="Set de Toallas 3 piezas",
    descripcion="Set de toallas de algodón: baño, manos y cara",
    precio_venta=249.99,
    stock=60,
    categoria=cat_hogar,
    activo=True
)

print(f"✓ {Producto.objects.count()} productos creados")

# ============ CREAR PROVEEDORES ============
print("\nCreando proveedores...")

Proveedor.objects.create(
    nombre="Juan Pérez",
    empresa="Electrónica del Norte SA",
    telefono="555-1234",
    email="juan.perez@electronorte.com",
    direccion="Av. Tecnología 123, Monterrey, NL"
)

Proveedor.objects.create(
    nombre="María García",
    empresa="Textiles y Moda SRL",
    telefono="555-5678",
    email="maria.garcia@textilesmoda.com",
    direccion="Calle Industria 456, Guadalajara, JAL"
)

Proveedor.objects.create(
    nombre="Carlos López",
    empresa="Distribuidora Alimentaria",
    telefono="555-9012",
    email="carlos.lopez@distalimentaria.com",
    direccion="Blvd. Comercio 789, Ciudad de México"
)

print(f"✓ {Proveedor.objects.count()} proveedores creados")

# ============ CREAR CLIENTES ============
print("\nCreando clientes...")

Cliente.objects.create(
    nombre="Ana",
    apellido="Martínez",
    email="ana.martinez@email.com",
    telefono="555-1111",
    direccion="Calle Principal 100, Col. Centro"
)

Cliente.objects.create(
    nombre="Pedro",
    apellido="Sánchez",
    email="pedro.sanchez@email.com",
    telefono="555-2222",
    direccion="Av. Reforma 200, Col. Juárez"
)

Cliente.objects.create(
    nombre="Laura",
    apellido="Fernández",
    email="laura.fernandez@email.com",
    telefono="555-3333",
    direccion="Calle Libertad 300, Col. Americana"
)

Cliente.objects.create(
    nombre="Roberto",
    apellido="Torres",
    email="roberto.torres@email.com",
    telefono="555-4444",
    direccion="Av. Universidad 400, Col. Del Valle"
)

print(f"✓ {Cliente.objects.count()} clientes creados")

# ============ RESUMEN ============
print("\n" + "="*50)
print("DATOS DE EJEMPLO CARGADOS EXITOSAMENTE")
print("="*50)
print(f"Categorías: {Categoria.objects.count()}")
print(f"Productos:  {Producto.objects.count()}")
print(f"Proveedores: {Proveedor.objects.count()}")
print(f"Clientes:   {Cliente.objects.count()}")
print("="*50)
print("\n¡Ahora puedes iniciar sesión y explorar el sistema!")
