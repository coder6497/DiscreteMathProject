from itertools import product
from prettytable import PrettyTable

class Stack: # Класс для реализации стека
    def __init__(self):
        self.stack = []
    
    def push(self, data):
        self.stack.append(data)
    
    def pop(self):
        self.stack.pop()
    
    def top(self):
        return self.stack[-1]
    
    def empty(self):
        return len(self.stack) == 0
    

def parse(expression, variables): # Функция для парсинга логических выражений
    def get_postfix():
        tokens = list(filter(lambda x: x != ' ', expression))  
        precendence = {'(': 0, "!": 3, '&': 2, '|': 1} #Приоритет операций
        operators = Stack()
        output = []
        for tk in tokens:  # Если буква то добавляем на выход если ( то в стек операторов
            if tk.isalpha():
                output.append(tk)
            elif tk == '(':
                operators.push(tk) 
            elif tk == ')':   # Если встречаем ) добавляем все операторы в скобках на выход пока не встретим открывающуюю скобку за ем удалаем )
                while operators.top() != '(':
                    output.append(operators.top())
                    operators.pop()
                operators.pop()
            else:
                while not operators.empty() and precendence[operators.top()] >= precendence[tk]:  # Добавляем операторы в стек операторов
                    output.append(operators.top())      # Затем учитывая порядок добавляем их на выход
                    operators.pop()
                operators.push(tk)  
        while not operators.empty():    # Добавляем оставшиеся операторы из стека на выход
            output.append(operators.top())
            operators.pop()
        return output
    

    def get_result(postfix): # Функция для вычисления выражения
        stack = Stack()
        for token in postfix:  # Проверяем на переменную и добавляем в стек значение словаря {"A": True}
            if token in variables:
                stack.push(variables[token])
            elif token == '!':  # Если встречаем инверсию берем из стека один операнд проводим операцию и добавляем результат в стек
                a = stack.top()
                stack.pop()
                stack.push(not a)
            else:   # Если встречаем & | то берем 2 операнда и добавляем в стек операцию
                b = stack.top()
                stack.pop()
                a = stack.top()
                stack.pop()
                if token == '&':
                    stack.push(a and b)
                if token == '|':
                    stack.push(a or b)
        return stack.top()
    return get_result(get_postfix())


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


def main():
    try:
        count = int(input("Введите кол-во переменных >>> "))
        variables = sorted([input("Введите переменную >>> ") for _ in range(count)])
        expression = input("Введите выражение >>> ")
        table, vector = get_trush_table(expression, variables)
        table_init = PrettyTable(variables + ['F']) #Иницаилизируем таблицу и векторный вид
        table_init.add_rows(table)
        print(f'{table_init}\n\n{vector}\n')
        print(get_sdnf(table, variables))
    except ValueError:
        print("Неверный формат числа")
        main()
    except IndexError:
        print("Неверный формат выражения")
        main()


if __name__ == "__main__":
    main()