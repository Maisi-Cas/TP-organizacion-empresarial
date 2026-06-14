# -*- coding: utf-8 -*-
# ============================================================
# PROY-2: Script de análisis de ventas
# Autor: [TU NOMBRE]
# Escenario B - Organización Empresarial
# ====================
# ========================================

# Importación de librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import utils as u

# Utilizar caracteres unicode
sys.stdout.reconfigure(encoding="utf-8")

# ============================================================
# CREACIÓN DE CARPETAS
# ============================================================
# Se crean las carpetas de resultados si no existen.
# Esto garantiza reproducibilidad en cualquier entorno.

os.makedirs("../resultados", exist_ok=True)

# ============================================================
# CARGA DEL DATASET
# ============================================================
# El archivo CSV debe encontrarse dentro de la carpeta /datos

# Verifica que exista la dirección
if not os.path.isfile("../datos/dataset.csv"):
    print("=" * 48)
    print("No se ha encontrado ../datos/dataset.csv")
    exit()

ruta_dataset = "../datos/dataset.csv"

# En caso de que el CSV esté vacio, esto termina el programa
import os

if os.path.getsize("../datos/dataset.csv") == 0:
    print("=" * 48)
    print(">EL ARCHIVO .CSV ESTÁ VACIO<")
    print("Ingrese sus ventas en")
    print("=" * 48)
    print(".")
    print("   datos/")
    print("       dataset.csv < aquí")
    print("   resultados/")
    print("   scripts/")
    print("=" * 48)
    print("El formato debe ser el siguiente:")
    print("[sales_date,producto,cantidad,sales amount]")
    print("sales_date : AAAA-MM-DD")
    print("producto : producto: str")
    print("cantidad : cantidad: int")
    print("sales amount : importe de ventas: int")
    print("=" * 48)
    print("PD: Prueba Maisapaint en")
    print("https://github.com/Maisi-Cas/THE-Maisapaint")
    
    exit()
    


# Lectura del archivo CSV
df = pd.read_csv(ruta_dataset)
flag = False
keys = {
    'fecha de venta' : str,
    'producto' : str,
    'cantidad' : int,
    'importe de ventas' : int
}

# Verificar que hayan 4 columndas y que tengan los nombres respectivos

for i in keys.keys():
    if not i in df.keys():
        flag = True
        print(f"=" * 48)
        print(f" > [{i}] no se encuentra dentro de dataset.csv")

if flag:
    exit()

# Revisar que los diccionarios tengan contenido
for i, j in df.items():
    if len(j) == 0:
        flag = True
        print(f"=" * 48)
        print(f"La columna {i} está vacía") 

if flag:
    exit()

# Verificar si los datos son los adecuados para cada lista



for i, j in keys.items():
    d = u.onlyType(df[i], j)
    if not d['estado']:
        flag = True
        print("=" * 48)
        for k in d['log']:
            print(f"{k} cuando debería ser {str(j)}")
            
if flag:
    exit()
        



# ============================================================
# LIMPIEZA Y PREPARACIÓN DE DATOS
# ============================================================

# Conversión de fechas al formato datetime
df["fecha de venta"] = pd.to_datetime(df["fecha de venta"])

# Verificación de valores nulos
print("Valores nulos por columna:")
print(df.isnull().sum())

# Eliminación de filas vacías si existen
df = df.dropna()

# ============================================================
# CÁLCULO DE INDICADORES
# ============================================================

# ------------------------------------------------------------
# 1. Ventas Totales
# ------------------------------------------------------------

ventas_totales = df["importe de ventas"].sum()

# ------------------------------------------------------------
# 2. Producto más vendido
# ------------------------------------------------------------

productos_vendidos = (
    df.groupby("producto")["cantidad"]
    .sum()
    .sort_values(ascending=False)
)

producto_mas_vendido = productos_vendidos.idxmax()
cantidad_mas_vendida = productos_vendidos.max()

# ------------------------------------------------------------
# 3. Ventas por mes
# ------------------------------------------------------------

df["mes"] = df["fecha de venta"].dt.month

ventas_por_mes = (
    df.groupby("mes")["importe de ventas"]
    .sum()
)

# ============================================================
# MOSTRAR RESULTADOS EN CONSOLA
# ============================================================

print("\n======================================")
print("RESULTADOS DEL ANÁLISIS DE VENTAS")
print("======================================")

print(f"\nVentas Totales: ${ventas_totales:,.2f}")

print(f"\nProducto Más Vendido: {producto_mas_vendido}")
print(f"Cantidad Vendida: {cantidad_mas_vendida}")

print("\nVentas por Mes:")
print(ventas_por_mes)

# ============================================================
# EXPORTACIÓN DE RESULTADOS
# ============================================================

# Guardar resumen en archivo TXT

ruta_resumen = "../resultados/resumen_ventas.txt"

with open(ruta_resumen, "w", encoding="utf-8") as archivo:

    archivo.write("=====================================\n")
    archivo.write("RESULTADOS DEL ANÁLISIS DE VENTAS\n")
    archivo.write("=====================================\n\n")

    archivo.write(f"Ventas Totales: ${ventas_totales:,.2f}\n\n")

    archivo.write(f"Producto Más Vendido: {producto_mas_vendido}\n")
    archivo.write(f"Cantidad Vendida: {cantidad_mas_vendida}\n\n")

    archivo.write("VENTAS POR MES\n")
    archivo.write("-------------------------\n")

    archivo.write(ventas_por_mes.to_string())

# ============================================================
# GENERACIÓN DE GRÁFICOS
# ============================================================

# ------------------------------------------------------------
# Gráfico 1 - Ventas por mes
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

ventas_por_mes.plot(kind="bar")

plt.title("Ventas por Mes")
plt.xlabel("Mes")
plt.ylabel("Monto de Ventas")

# Ajuste automático de diseño
plt.tight_layout()

# Guardar gráfico
ruta_grafico_1 = "../resultados/grafico_ventas_mes.png"

plt.savefig(ruta_grafico_1)

# Mostrar gráfico
plt.show()

# ============================================================
# Gráfico 2 - Productos más vendidos
# ============================================================

plt.figure(figsize=(10, 6))

productos_vendidos.plot(kind="bar")

plt.title("Cantidad Vendida por Producto")
plt.xlabel("Producto")
plt.ylabel("Cantidad")

plt.tight_layout()

# Guardar gráfico
ruta_grafico_2 = "../resultados/grafico_productos.png"

plt.savefig(ruta_grafico_2)

plt.show()

# ============================================================
# EXPORTAR DATOS AGRUPADOS
# ============================================================

# Guardar ventas por mes en CSV

ventas_por_mes.to_csv(
    "../resultados/ventas_por_mes.csv",
    header=["ventas"]
)

# Guardar ranking de productos

productos_vendidos.to_csv(
    "../resultados/productos_vendidos.csv",
    header=["cantidad"]
)

# ============================================================
# MENSAJE FINAL
# ============================================================

print("\n======================================")
print("ANÁLISIS FINALIZADO CORRECTAMENTE")
print("Los resultados fueron guardados en")
print(".")
print("   resultados/ < aquí")
print("   scripts/")
print("   datos/")
print("======================================")
