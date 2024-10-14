def juega_mateo(monedas, izq, der, g_mateo):
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
    final = []
    g_sophia = g_mateo = indice = 0

    for i in range(len(optimos)-1, 0, -2):
        izq, der, opt = optimos[i][indice]
       
        # Veo si agarre la de la izq o si queda solo un elemento
        prox_i_si_agarro_izq = izq + 2 if monedas[izq+1] > monedas[der] else izq + 1
        if izq == der or opt == monedas[izq] + optimos[i-2][prox_i_si_agarro_izq][-1]: ################
            final.append(f"Sophia debe agarrar la primera ({monedas[izq]})")
            g_sophia += monedas[izq]
            if izq == der: break
            mateo, g_mateo, indice = juega_mateo(monedas, izq+1, der, g_mateo)
        else:
            final.append(f"Sophia debe agarrar la ultima ({monedas[der]})")
            g_sophia += monedas[der]
            mateo, g_mateo, indice = juega_mateo(monedas, izq, der-1, g_mateo)
        
        final.append(mateo)

    return final, g_sophia, g_mateo

def monedas_dinamicas(mon):
    optimos =  [
        [(0,0,0)] * (len(mon)+1), #################
        [(i, i, mon[i]) for i in range(len(mon))]
    ] 
    for i in range(2,len(mon)+1):
        local =  []
        for j in range(len(mon)+1-i):
            izq, der = optimos[i-1][j][0], optimos[i-1][j+1][1]

            prox_subarr_si_agarro_izq = (izq+2,der) if mon[izq+1] > mon[der] else (izq+1, der-1) ###############
            prox_subarr_si_agarro_der = (izq,der-2) if mon[der-1] > mon[izq] else (izq+1, der-1) ##############
    
            opcion_izq, opcion_der = mon[izq] + optimos[i-2][prox_subarr_si_agarro_izq[0]][2], mon[der] + optimos[i-2][prox_subarr_si_agarro_der[0]][2]
            local.append((izq, der, max(opcion_izq, opcion_der)))

        optimos.append(local)

    return recontruir(mon, optimos)
