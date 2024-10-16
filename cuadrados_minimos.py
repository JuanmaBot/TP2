import csv
import matplotlib.pyplot as plt
import numpy as np

# ========= Aproximacion por cuadrados minimos ========= #

def ajuste_cuadratico(cantidades, tiempos):
    cantidades = np.array(cantidades)
    tiempos = np.array(tiempos)

    A = np.vstack([cantidades**2, cantidades, np.ones(len(tiempos))]).T
    AtA = A.T @ A
    Atb = A.T @ tiempos
    x = np.linalg.solve(AtA, Atb)

    a, b, c = x
    tiempos_predecidos = a * cantidades**2 + b * cantidades + c
    errores_residuales = list(map(abs, tiempos - tiempos_predecidos))

    return x, errores_residuales

# ========== Graficos ========== #

def graficar_benchmark(cantidades, tiempos):
    plt.plot(cantidades, tiempos, marker='o', linestyle='none')
    plt.title("Tiempos de ejecución del algoritmo")
    plt.xlabel("Cantidad de monedas")
    plt.ylabel("Tiempo de ejecución (segundos)")
    plt.grid(True)
    plt.show()

def graficar_ajuste_cuadratico(cantidades, tiempos, coeficiente_2, coeficiente_1, coeficiente_0):
    tiempos_ajustados = coeficiente_2 * np.array(cantidades)**2 + coeficiente_1 * np.array(cantidades) + coeficiente_0
    plt.plot(cantidades, tiempos, 'o', label='Tiempos medidos')  # Datos originales
    plt.plot(cantidades, tiempos_ajustados, '-', label=f'Ajuste cuadrático: t(n) = {coeficiente_2:.5e} * n^2 + {coeficiente_1:.5e} * n + {coeficiente_0:.5e}')
    plt.xlabel('Cantidad de monedas')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title('Ajuste por cuadrados mínimos usando $A^T Ax = A^T b$')
    plt.legend()
    plt.grid(True)
    plt.show()

def graficar_error(errores):
    plt.plot(errores, marker='o')
    plt.title("Errores residuales del ajuste")
    plt.xlabel("Cantidad de monedas")
    plt.ylabel("Error residual")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    with open('./tablas/tabla_variabilidad.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        cantidades = []
        tiempos_poco_variadas = []
        tiempos_medianamente_variadas = []
        tiempos_muy_variadas = []
        for row in reader:
            cantidades.append(int(row[0]))
            tiempos_poco_variadas.append(float(row[1]))
            tiempos_medianamente_variadas.append(float(row[2]))
            tiempos_muy_variadas.append(float(row[3]))

    # Graficamos los tiempos medidos
    x, errores = ajuste_cuadratico(cantidades, tiempos_poco_variadas)
    graficar_ajuste_cuadratico(cantidades, tiempos_poco_variadas, x[0], x[1], x[2])
    graficar_error(errores)

    x, errores = ajuste_cuadratico(cantidades, tiempos_medianamente_variadas)
    graficar_ajuste_cuadratico(cantidades, tiempos_medianamente_variadas, x[0], x[1], x[2])
    graficar_error(errores)

    x, errores = ajuste_cuadratico(cantidades, tiempos_muy_variadas)
    graficar_ajuste_cuadratico(cantidades, tiempos_muy_variadas, x[0], x[1], x[2])
    graficar_error(errores)