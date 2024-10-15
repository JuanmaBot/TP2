import sys

def juega_mateo(monedas, izq, der, g_mateo):
    """
    # Descripción
    Recibe una lista de monedas y dos indices que representan los extremos de un subarreglo de monedas que le tocaría a Mateo.
    Devuelve una tupla con (un string que indica que moneda agarra Mateo, la sumatoria de monedas que tiene Mateo, el primer indice del proximo subarreglo)
    # Complejidad
    La complejidad de este algoritmo es **O(1)**, ya que solo hace operaciones en tiempo constante.
    """
    if monedas[izq] > monedas[der]:
        mateo = f"Mateo agarra la primera ({monedas[izq]})" 
        g_mateo += monedas[izq]
        indice = izq + 1
    else:
        mateo = f"Mateo agarra la ultima ({monedas[der]})"
        g_mateo += monedas[der]
        indice = izq
    
    return mateo, g_mateo, indice

def recontruir(monedas, optimos):
    """
    # Descripción
    Recibe una lista de monedas y una lista de listas de tuplas que representan los subarreglos de monedas y las sumatorias de monedas optimas.
    Devuelve una tupla con (una lista de strings que indican que monedas agarran Sophia y Mateo, la sumatoria de monedas que tiene Sophia, la sumatoria de monedas que tiene Mateo)
    # Complejidad
    La complejidad de este algoritmo depende en su totalidad de la cantidad de monedas/optimos que se le pasen.
    Recorre la matriz de optimos accediendo a un elemento de cada fila y haciendo operaciones en tiempo constante.
    Dado esto, la complejidad es **O(n)**, donde n es la cantidad de monedas.
    """
    # Inicializo variables
    final = []
    g_sophia = g_mateo = indice = 0

    # Recorro la lista de optimos de atras para adelante
    for i in range(len(optimos)-1, 0, -2):
        izq, der, opt = optimos[i][indice]
       
        # Veo si queda solo un elemento o si agarre la moneda de la izquierda con la ecuacion de recurrencia
        prox_i_si_agarro_izq = izq + 2 if izq == der or monedas[izq+1] > monedas[der] else izq + 1
        if izq == der or opt == monedas[izq] + optimos[i-2][prox_i_si_agarro_izq][-1]: 
            final.append(f"Sophia debe agarrar la primera ({monedas[izq]})")
            g_sophia += monedas[izq]
            if izq == der: break # Si era solo un elemento, termino
            mateo, g_mateo, indice = juega_mateo(monedas, izq+1, der, g_mateo) # Si no, juega Mateo
        else:
            final.append(f"Sophia debe agarrar la ultima ({monedas[der]})")
            g_sophia += monedas[der]
            mateo, g_mateo, indice = juega_mateo(monedas, izq, der-1, g_mateo)
        
        final.append(mateo)

    return final, g_sophia, g_mateo

def monedas_dinamicas(mon):
    """
    # Descripción
    Recibe una lista de monedas y calcula la maxima sumatoria posible que puede obtener Sophia si juega de manera optima para todos los subarreglos de monedas posibles.
    Esto se hace mediante programacion dinamica, sin hacer recalculos innecesarios.
    # Complejidad
    El algoritmo depende en su totalidad del tamaño del arreglo de monedas.
    Éste genera una matriz triangular de base n, donde n es la cantidad de monedas, y luego hace operaciones en tiempo constante.
    Por lo tanto, se hacen (n^2)/2 operaciones, pero como el 2 es constante, la complejidad queda **O(n^2)**.
    Luego de esto está la reconstrucción de la solución, que es lineal en la cantidad de monedas, por lo que la cota superior de la complejidad es **O(n^2)**.
    """
    # Inicializo la lista de optimos
    optimos =  [
        [(0,0,0)] * (len(mon)+1), 
        [(i, i, mon[i]) for i in range(len(mon))]
    ] 
    # Voy llenando las listas de optimos para todos los subarreglos posibles, empezando por los de tamaño 2 y terminando en el de tamaño n
    for i in range(2,len(mon)+1):
        local =  []
        # Recorro todos los subarreglos de tamaño i combinando 2 subarreglos de tamaño i-1
        for j in range(len(mon)+1-i):
            # Obtengo los extremos de mi nuevo subarreglo
            izq, der = optimos[i-1][j][0], optimos[i-1][j+1][1]

            # Simulo los proximos subarreglos si agarro la moneda de la izquierda o la de la derecha sabiendo que Mateo agarra la moneda de mayor valor
            prox_subarr_si_agarro_izq = (izq+2,der) if mon[izq+1] > mon[der] else (izq+1, der-1) 
            prox_subarr_si_agarro_der = (izq,der-2) if mon[der-1] > mon[izq] else (izq+1, der-1) 
    
            # Calculo los óptimos posibles sacando la moneda de la izquierda o la de la derecha y me quedo con el máximo
            opcion_izq, opcion_der = mon[izq] + optimos[i-2][prox_subarr_si_agarro_izq[0]][2], mon[der] + optimos[i-2][prox_subarr_si_agarro_der[0]][2]
            local.append((izq, der, max(opcion_izq, opcion_der)))

        optimos.append(local)

    # Reconstruyo la solución
    return recontruir(mon, optimos)

if __name__ == "__main__":
    # Recibir archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py <archivo>")
        sys.exit(1)

    # Leer archivo. Ignorar las lineas que comienzan con #. Las monedas estan en una linea separadas por ;
    with open(sys.argv[1], "r") as file:
        for line in file:
            if not line.startswith("#"):
                monedas = list(map(int, line.strip().split(";")))

    # Calcular la maxima sumatoria posible que puede obtener Sophia
    resultado, g_sophia, g_mateo = monedas_dinamicas(monedas)

    # Imprimir resultado
    print("; ".join(resultado))
    print(f"Ganancia Sophia: {g_sophia}")
    print(f"Ganancia Mateo: {g_mateo}")
