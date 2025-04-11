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


def create_table(expression, count, variables):
    table = PrettyTable(variables + ['F'])
    vector = ''
    for i in product((0, 1), repeat=len(variables)):
        var_values = dict(zip(variables, i))
        parsed = parse(expression, var_values)
        table.add_row(list(var_values.values()) + [parsed])
        vector += str(parsed)
    print(table)
    print(f'{expression} -> {vector}')

expression = input("Введите выражение >>> ")
count = int(input("Введите кол-во переменных >>> "))
variables = sorted([input("Введите переменную >>> ") for _ in range(count)])

create_table(expression, count, variables)