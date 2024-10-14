import random
import datetime
import matplotlib.pyplot as plt
import csv
from TP2 import monedas_dinamicas

# Listas para almacenar los tiempos de ejecución
tamanos = [1, 10, 100, 1000, 6000, 10000, 15000, 20000]
tiempos_poco_variado = []
tiempos_medianamente_variado = []
tiempos_muy_variado = []

# Función para medir tiempos de ejecución
def medir_tiempo(n):
    poco_variado = []
    medianamente_variado = []
    muy_variado = []

    for _ in range(n):
        poco_variado.append(random.randint(1, 10))
        medianamente_variado.append(random.randint(1, 5000))
        muy_variado.append(random.randint(1, 100000000000))

    # Medimos tiempo para conjunto poco variado
    inicio = datetime.datetime.now()
    monedas_dinamicas(poco_variado)
    fin = datetime.datetime.now()
    tiempo_poco_variado = fin - inicio

    # Medimos tiempo para conjunto medianamente variado
    inicio = datetime.datetime.now()
    monedas_dinamicas(medianamente_variado)
    fin = datetime.datetime.now()
    tiempo_medianamente_variado = fin - inicio

    # Medimos tiempo para conjunto muy variado
    inicio = datetime.datetime.now()
    monedas_dinamicas(muy_variado)
    fin = datetime.datetime.now()
    tiempo_muy_variado = fin - inicio

    return tiempo_poco_variado.total_seconds(), tiempo_medianamente_variado.total_seconds(), tiempo_muy_variado.total_seconds()

# Ejecutamos para cada tamaño de conjunto
for tamano in tamanos:
    tiempo_poco, tiempo_med, tiempo_muy = medir_tiempo(tamano)
    tiempos_poco_variado.append(tiempo_poco)
    tiempos_medianamente_variado.append(tiempo_med)
    tiempos_muy_variado.append(tiempo_muy)
    print(f"Terminado para {tamano} monedas")

# Guardamos los resultados en un archivo CSV
with open('TP2/tablas/tabla_variabilidad.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Escribimos el encabezado
    writer.writerow(["Número de Monedas", "Tiempo Poco Variado (s)", "Tiempo Medianamente Variado (s)", "Tiempo Muy Variado (s)"])
    # Escribimos los datos
    for i, tamano in enumerate(tamanos):
        writer.writerow([tamano, tiempos_poco_variado[i], tiempos_medianamente_variado[i], tiempos_muy_variado[i]])

# Graficamos los resultados
plt.figure(figsize=(10, 6))
plt.plot(tamanos, tiempos_poco_variado, label="Poco Variado (1 - 10)", marker="o")
plt.plot(tamanos, tiempos_medianamente_variado, label="Medianamente Variado (1 - 5,000)", marker="o", linestyle=":")
plt.plot(tamanos, tiempos_muy_variado, label="Muy Variado (1 - 100,000,000,000)", marker="o", linestyle="--")
plt.xlabel("Número de Monedas")
plt.ylabel("Tiempo de Ejecución (segundos)")
plt.title("Comparación de Tiempos de Ejecución para Diferentes Variaciones de Monedas")
plt.legend()
plt.grid(True)

# Guardamos la gráfica como "grafico_var.png"
plt.savefig("TP2/graficos/grafico_var.png")
plt.show()
