import math

def get_function():
    while True:
        try:
            func_str = input("Введите функцию f(x): ")
            return lambda x: eval(func_str, {"x": x, **math.__dict__})
        except Exception as e:
            print(f"Ошибка ввода функции: {e}. Попробуйте снова.")

def get_float_input(prompt, error_msg):
    while True:
        try:
            value_str = input(prompt).replace(',', '.')
            return eval(value_str, {"__builtins__": None}, {"math": math, **math.__dict__})
        except Exception as e:
            print(f"{error_msg}: {e}")

def get_limit(name):
    return get_float_input(
        f"Введите {name} предел: ",
        "Ошибка: Введите число или допустимое выражение"
    )

def get_eps():
    while True:
        try:
            eps_str = input("Введите требуемую точность eps (например, 1e-6): ").replace(',', '.')
            eps = float(eps_str)
            if eps > 0:
                return eps
            else:
                raise ValueError("Точность должна быть положительным числом.")
        except ValueError as e:
            print(f"Ошибка: {e}")

def format_result(value, precision):
    formatted = f"{value:.{precision}f}"
    if '.' in formatted:
        return formatted.rstrip('0').rstrip('.')
    return formatted

def simpsons_rule(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("Количество интервалов должно быть чётным")
    h = (b - a) / n
    result = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        coefficient = 4 if i % 2 else 2
        result += coefficient * f(x)
    return result * h / 3

def compute_integral(f, a, b, eps):
    max_iterations = 100
    min_h = 1e-16
    n = 2
    prev_result = simpsons_rule(f, a, b, n)
    
    for iteration in range(max_iterations):
        n *= 2
        current_h = (b - a)/n
        if current_h < min_h:
            break
        current_result = simpsons_rule(f, a, b, n)
        if abs(current_result - prev_result) <= eps:
            return current_result, True
        prev_result = current_result
    
    return prev_result, False

def main():
    try:
        # Ввод данных
        f = get_function()
        a = get_limit("нижний")
        b = get_limit("верхний")
        eps = get_eps()
        
        # Определение точности вывода
        precision = max(0, min(int(math.ceil(-math.log10(eps))), 15))
        
        # Вычисление интеграла
        result, success = compute_integral(f, a, b, eps)
        
        # Форматирование результата
        formatted_result = format_result(result, precision)
        
        # Вывод
        if success:
            print(f"Интеграл от {a} до {b} с точностью eps={eps} равен {formatted_result}")
        else:
            print(f"Не удалось достичь точности eps={eps}")
            print(f"Приблизительное значение интеграла: {formatted_result}")
            
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
