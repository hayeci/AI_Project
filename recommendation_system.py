"""Recomendador sencillo de productos, ejecutable desde la terminal."""

import argparse


# Cada producto tiene una categoría, un precio y etiquetas que describen sus
# características principales.
PRODUCTOS = [
	{"nombre": "Auriculares inalámbricos", "categoria": "Audio", "precio": 89.99, "caracteristicas": {"inalambrico", "bluetooth", "cancelacion de ruido", "portatil"}},
	{"nombre": "Auriculares de estudio", "categoria": "Audio", "precio": 129.99, "caracteristicas": {"cable", "alta fidelidad", "microfono", "estudio"}},
	{"nombre": "Altavoz Bluetooth", "categoria": "Audio", "precio": 59.99, "caracteristicas": {"inalambrico", "bluetooth", "portatil", "resistente al agua"}},
	{"nombre": "Barra de sonido", "categoria": "Audio", "precio": 199.99, "caracteristicas": {"alta fidelidad", "inalambrico", "television", "cine en casa"}},
	{"nombre": "Teclado mecánico", "categoria": "Informática", "precio": 109.99, "caracteristicas": {"mecanico", "inalambrico", "retroiluminado", "compacto"}},
	{"nombre": "Ratón ergonómico", "categoria": "Informática", "precio": 49.99, "caracteristicas": {"inalambrico", "ergonomico", "bluetooth", "recargable"}},
	{"nombre": "Monitor 4K", "categoria": "Informática", "precio": 329.99, "caracteristicas": {"4k", "pantalla", "alta resolucion", "escritorio"}},
	{"nombre": "Webcam HD", "categoria": "Informática", "precio": 69.99, "caracteristicas": {"hd", "video", "microfono", "escritorio"}},
	{"nombre": "Cámara sin espejo", "categoria": "Fotografía", "precio": 749.99, "caracteristicas": {"sin espejo", "4k", "portatil", "lente intercambiable"}},
	{"nombre": "Trípode ligero", "categoria": "Fotografía", "precio": 39.99, "caracteristicas": {"portatil", "ajustable", "fotografia", "aluminio"}},
	{"nombre": "Lámpara de escritorio", "categoria": "Hogar", "precio": 34.99, "caracteristicas": {"led", "ajustable", "escritorio", "ahorro de energia"}},
	{"nombre": "Cafetera de filtro", "categoria": "Hogar", "precio": 79.99, "caracteristicas": {"cocina", "programable", "acero inoxidable", "ahorro de energia"}},
	{"nombre": "Botella térmica", "categoria": "Deporte", "precio": 24.99, "caracteristicas": {"portatil", "acero inoxidable", "reutilizable", "resistente"}},
	{"nombre": "Reloj deportivo", "categoria": "Deporte", "precio": 159.99, "caracteristicas": {"inalambrico", "resistente al agua", "actividad", "recargable"}},
	{"nombre": "Mochila urbana", "categoria": "Accesorios", "precio": 64.99, "caracteristicas": {"portatil", "compacto", "resistente", "viaje"}},
]


def calcular_similitud(producto, candidato):
	"""Calcula una puntuación entre 0 y 1 con categoría, etiquetas y precio."""
	etiquetas_producto = producto["caracteristicas"]
	etiquetas_candidato = candidato["caracteristicas"]
	union = etiquetas_producto | etiquetas_candidato
	similitud_etiquetas = (
		len(etiquetas_producto & etiquetas_candidato) / len(union) if union else 0.0
	)

	precios = [articulo["precio"] for articulo in PRODUCTOS]
	rango_precios = max(precios) - min(precios)
	similitud_precio = (
		1.0 - abs(producto["precio"] - candidato["precio"]) / rango_precios
		if rango_precios
		else 1.0
	)
	similitud_categoria = float(producto["categoria"] == candidato["categoria"])

	return (
		0.45 * similitud_etiquetas
		+ 0.35 * similitud_categoria
		+ 0.20 * similitud_precio
	)


def recomendar(producto, cantidad=5):
	"""Devuelve los productos más similares, sin incluir el producto elegido."""
	candidatos = [articulo for articulo in PRODUCTOS if articulo is not producto]
	candidatos.sort(
		key=lambda articulo: (-calcular_similitud(producto, articulo), articulo["nombre"])
	)
	return candidatos[:cantidad]


def mostrar_productos():
	"""Imprime el catálogo numerado para facilitar la selección."""
	print("\nCatálogo de productos:")
	for numero, producto in enumerate(PRODUCTOS, start=1):
		print(f"{numero:2}. {producto['nombre']} ({producto['categoria']}) - {producto['precio']:.2f} €")


def buscar_producto(nombre):
	"""Busca un producto por nombre, sin distinguir mayúsculas."""
	nombre_normalizado = nombre.strip().casefold()
	for producto in PRODUCTOS:
		if producto["nombre"].casefold() == nombre_normalizado:
			return producto
	return None


def seleccionar_producto():
	"""Solicita una selección válida y permite reintentar ante errores."""
	while True:
		seleccion = input("\nElige el número del producto que te interesa: ").strip()
		try:
			numero = int(seleccion)
		except ValueError:
			print("Entrada no válida. Escribe el número de un producto.")
			continue

		if 1 <= numero <= len(PRODUCTOS):
			return PRODUCTOS[numero - 1]
		print(f"El número debe estar entre 1 y {len(PRODUCTOS)}.")


def main():
	parser = argparse.ArgumentParser(description="Recomienda productos similares.")
	parser.add_argument(
		"--producto",
		help="nombre exacto del producto; si se omite, se solicitará una selección",
	)
	parser.add_argument(
		"--listar", action="store_true", help="muestra el catálogo y termina"
	)
	argumentos = parser.parse_args()

	mostrar_productos()
	if argumentos.listar:
		return 0

	if argumentos.producto:
		producto = buscar_producto(argumentos.producto)
		if producto is None:
			print(f"No se encontró el producto: {argumentos.producto}")
			return 1
	else:
		try:
			producto = seleccionar_producto()
		except (EOFError, KeyboardInterrupt):
			print("\nSelección cancelada.")
			return 1

	recomendaciones = recomendar(producto)
	print(f"\nProductos más similares a {producto['nombre']}:")
	for numero, articulo in enumerate(recomendaciones, start=1):
		puntuacion = calcular_similitud(producto, articulo)
		print(
			f"{numero}. {articulo['nombre']} ({articulo['categoria']}) - "
			f"{articulo['precio']:.2f} € | similitud: {puntuacion:.0%}"
		)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
