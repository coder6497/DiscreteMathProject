from itertools import product
from prettytable import PrettyTable

class Stack:
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
    

def parse(expression, variables):
    def get_postfix():
        tokens = list(filter(lambda x: x != ' ', expression))
        precendence = {'(': 0, "!": 3, '&': 2, '|': 1}
        operators = Stack()
        output = []
        for tk in tokens:
            if tk.isalpha():
                output.append(tk)
            elif tk == '(':
                operators.push(tk)
            elif tk == ')':
                while operators.top() != '(':
                    output.append(operators.top())
                    operators.pop()
                operators.pop()
            else:
                while not operators.empty() and precendence[operators.top()] >= precendence[tk]:
                    output.append(operators.top())
                    operators.pop()
                operators.push(tk)
        while not operators.empty():
            output.append(operators.top())
            operators.pop()
        return output
    

    def get_result(postfix):
        stack = Stack()
        for token in postfix:
            if token in variables:
                stack.push(variables[token])
            elif token == '!':
                a = stack.top()
                stack.pop()
                stack.push(not a)
            else:
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


def get_data_for_function(expression, variables):
    trush_table = []

    def get_trush_table():
        table_init = PrettyTable(variables + ['F'])
        vector = ''
        for i in product((0, 1), repeat=len(variables)):
            var_values = dict(zip(variables, i))
            parsed = parse(expression, var_values)
            trush_table.append(list(var_values.values()) + [int(parsed)])
            vector += str(int(parsed))
        table_init.add_rows(trush_table)
        print(table_init)
        print(f'{expression} -> {vector}')

    get_trush_table()

    def get_sdnf():
        sdnf_disjuncts = []
        for row in trush_table:
            if row[-1] == 1:
                conjuncts = []
                for var, var_value in zip(variables, row[:-1]):
                    if var_value == 1:
                        conjuncts.append(var)
                    else:
                        conjuncts.append(f'!{var}')
                sdnf_disjuncts.append('&'.join(conjuncts))
        print("СДНФ: ", ' | '.join(sdnf_disjuncts))

    get_sdnf()


def main():
    try:
        count = int(input("Введите кол-во переменных >>> "))
        variables = sorted([input("Введите переменную >>> ") for _ in range(count)])
        expression = input("Введите выражение >>> ")
        get_data_for_function(expression, variables)
    except ValueError:
        print("Неверный формат числа")
        main()
    except IndexError:
        print("Неверный формат выражения")
        main()


if __name__ == "__main__":
    main()