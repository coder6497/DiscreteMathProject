from itertools import product
from prettytable import PrettyTable
from parse_expression import parse

def get_data_for_function(expression, variables): # Здесь мы получаем результат (СДНФ таблица истинности)
    trush_table = []

    def get_trush_table():
        table_init = PrettyTable(variables + ['F']) #Иницаилизируем таблицу и векторный вид
        vector = ''
        for i in product((0, 1), repeat=len(variables)): # Перебираем нули и единицы и создаем словарь по типу {"A": 1 "B': 0}
            var_values = dict(zip(variables, i))
            parsed = parse(expression, var_values)
            trush_table.append(list(var_values.values()) + [int(parsed)]) # Добавляем в таблицу значения словаря + значения выражения
            vector += str(int(parsed)) 
        table_init.add_rows(trush_table)
        print(table_init)  # Печатаем саму таблицу и векторный вид
        print(f'{expression} -> {vector}') 

    get_trush_table()

    def get_sdnf():
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
        print("СДНФ: ", ' | '.join(sdnf_disjuncts)) # Собираем СДНФ

    get_sdnf()