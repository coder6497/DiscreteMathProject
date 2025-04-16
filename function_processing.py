from itertools import product
from parse_expression import parse

def get_trush_table(expression, variables): # Здесь мы получаем результат (СДНФ таблица истинности)
    trush_table = []
    vector = ''
    for i in product((0, 1), repeat=len(variables)): # Перебираем нули и единицы и создаем словарь по типу {"A": 1 "B': 0}
        var_values = dict(zip(variables, i))
        parsed = parse(expression, var_values)
        trush_table.append(list(var_values.values()) + [int(parsed)]) # Добавляем в таблицу значения словаря + значения выражения
        vector += str(int(parsed)) 
    return trush_table, f'{expression} -> {vector}'

def get_sdnf(trush_table, variables):
    sdnf_disjuncts = []
    for row in trush_table:  # Перебираем таблицу истинности
        if row[-1] == 1:
            conjuncts = [] 
            for var, var_value in zip(variables, row[:-1]): # Если F = 1 то обьединяем переменные с их значениями в таблице
                if var_value == 1:
                    conjuncts.append(var) # Если 0 то добавляем в список коньюнктов переменную с отрицанием
                else:
                    conjuncts.append(f'!{var}')
            sdnf_disjuncts.append('&'.join(conjuncts))
    return "СДНФ: " + ' | '.join(sdnf_disjuncts) # Собираем СДНФ