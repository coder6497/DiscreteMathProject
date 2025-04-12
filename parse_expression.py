from stack_class import Stack

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