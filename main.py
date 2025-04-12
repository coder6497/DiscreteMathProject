from function_processing import get_data_for_function

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