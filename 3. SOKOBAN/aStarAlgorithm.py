def Astar(origin_coor, dest_coor, map, type_preference=0):
    
    origen=coord2station(origin_coor, map)
    destino=coord2station(dest_coor, map)
    idorigen=origen[0]
    iddestino=destino[0]
    lista = [Path(idorigen)]
    TCP = {}
    
    while(lista != None and lista[0].last != iddestino):
        C=lista[0]
        lista.pop(0) 
        E = expand(C,map)
        E = remove_cycles(E)
        E = calculate_cost(E, map,type_preference)
        E=calculate_heuristics(E,map,type_preference)
        E=update_f(E)
        ##E=update_f1(E)
        E, lista, TCP = remove_redundant_paths(E,lista,TCP)
        lista = insert_cost_f(lista, E)        
    if (lista != None):
        return lista[0]
    else:
        print("No existe solucion")  
    
    pass