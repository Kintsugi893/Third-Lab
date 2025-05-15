import math

def main():
    # Ввод функции
    while True:
        try:
            func_str = input("Введите интеграл f(x): ")
            break
        except Exception as e:
            print(f"Ошибка ввода функции: {e}. Попробуйте снова.")

    # Ввод нижнего предела a
    while True:
        try:
            a_str = input("Введите нижний предел a: ").replace(',', '.')
            a = eval(a_str, {"__builtins__": None}, {"math": math, **math.__dict__})
            break
        except (NameError, SyntaxError, ValueError) as e:
            print(f"Ошибка: {e}. Введите число или допустимое выражение.")

    # Ввод верхнего предела b
    while True:
        try:
            b_str = input("Введите верхний предел b: ").replace(',', '.')
            b = eval(b_str, {"__builtins__": None}, {"math": math, **math.__dict__})
            break
        except (NameError, SyntaxError, ValueError) as e:
            print(f"Ошибка: {e}. Введите число или допустимое выражение.")

    # Ввод точности
    while True:
        try:
            eps_str = input("Введите требуемую точность eps (например, 1e-6): ").replace(',', '.')
            eps = float(eps_str)
            if eps <= 0:
                raise ValueError("Точность должна быть положительным числом.")
            break
        except ValueError as e:
            print(f"Ошибка: {e}. Введите число.")

    # Автоматическое определение точности вывода
    try:
        precision = max(0, min(int(math.ceil(-math.log10(eps))), 15))
    except ValueError:
        precision = 15

    # Определение функции f(x)
    def f(x):
        try:
            return eval(func_str, {"x": x, **math.__dict__})
        except Exception as e:
            raise ValueError(f"Ошибка вычисления функции в x={x}: {e}")

    # Вычисление интеграла с динамическим шагом
    try:
        def integrate_simpson(n):
            if n % 2 != 0:
                raise ValueError("n должно быть четным")
            h = (b - a) / n
            s = f(a) + f(b)
            for i in range(1, n):
                x = a + i * h
                if i % 2 == 0:
                    s += 2 * f(x)
                else:
                    s += 4 * f(x)
            return s * h / 3

        max_iterations = 100
        min_h = 1e-16
        n = 2
        prev_integral = integrate_simpson(n)
        iteration = 0
        current_integral = None

        while iteration < max_iterations:
            n *= 2
            current_h = (b - a) / n
            if current_h < min_h:
                break
            try:
                current_integral = integrate_simpson(n)
            except Exception as e:
                raise ValueError(f"Ошибка вычисления при n={n}: {e}")
            if abs(current_integral - prev_integral) <= eps:
                break
            prev_integral = current_integral
            iteration += 1

        # Проверка на достижение точности
        if iteration >= max_iterations or current_h <= min_h:
            print(f"Не удалось достичь точности eps={eps}.")
        else:
            # Форматирование результата
            formatted_result = f"{current_integral:.{precision}f}".rstrip('0').rstrip('.') if '.' in f"{current_integral:.{precision}f}" else f"{current_integral:.0f}"
            print(f"Интеграл от {a} до {b} с точностью eps={eps} равен {formatted_result}")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
