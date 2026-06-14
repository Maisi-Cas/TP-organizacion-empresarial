def onlyType(lista: list, tipo) -> dict[bool, list[tuple]]:
    dic = {
        'estado' : all(isinstance(x, tipo) for x in lista),
        'log' : []
    }
    
    if dic['estado']:
        return dic
        
    for i in lista:
        if not i is tipo:
            dic['log'].append((i, str(type(i)))) 
    return dic