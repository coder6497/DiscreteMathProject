from itertools import product
from prettytable import PrettyTable
from parse_expression import parse

trush_table = []
# Здесь мы получаем результат (СДНФ таблица истинности)

def get_trush_table(expression, variables):
    table_init = PrettyTable(variables + ['F']) #Иницаилизируем таблицу и векторный вид
    vector = ''
    for i in product((0, 1), repeat=len(variables)): # Перебираем нули и единицы и создаем словарь по типу {"A": 1 "B': 0}
        var_values = dict(zip(variables, i))
        parsed = parse(expression, var_values)
        trush_table.append(list(var_values.values()) + [int(parsed)]) # Добавляем в таблицу значения словаря + значения выражения
        vector += str(int(parsed)) 
    table_init.add_rows(trush_table)
    result = table_init.get_string() + '\n' +  f'{expression} -> {vector}' # Печатаем саму таблицу и векторный вид
    return result
    

def get_sdnf(variables):
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
    return "СДНФ: ", ' | '.join(sdnf_disjuncts) # Собираем СДНФ

trush_table.clear()