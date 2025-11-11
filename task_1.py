# Завдання 1. Пошук максимального та мінімального елементів.

# Реалізуйте функцію, яка знаходить максимальний та мінімальний елементи в масиві, 
# використовуючи метод «розділяй і володарюй».
from typing import Sequence, Tuple

def min_max_dc(arr: Sequence[float]) -> Tuple[float, float]:
    """
    Функція повертає (мінімум, максимум) у послідовності arr, використовуючи підхід
    «розділяй і володарюй».

    Критерії прийняття:
    - Приймає масив довільної довжини (Sequence[float]) - є,
    - Рекурсивний підхід (ділимо навпіл, комбінуємо)    - є.
    - Часова складність O(n) - є.
    - Повертає кортеж (min, max) - є.
    - Для порожнього масиву піднімає ValueError.
    """
    n = len(arr)
    if n == 0:
        raise ValueError("Послідовність порожня")

    # Базові випадки
    if n == 1:
        x = arr[0]
        return x, x
    if n == 2:
        a, b = arr[0], arr[1]
        return (a, b) if a <= b else (b, a)

    # Розділяй
    mid = n // 2
    left_min, left_max = min_max_dc(arr[:mid])
    right_min, right_max = min_max_dc(arr[mid:])

    # Об'єднуй
    return (left_min if left_min <= right_min else right_min,
            left_max if left_max >= right_max else right_max)


# Приклади запуску
if __name__ == "__main__":
    data = [7, -3, 5, 12, 0, 9, -8, 4]
    mn, mx = min_max_dc(data)               # розпаковую кортеж у дві змінні mn і mx
    print(f"Мінімум: {mn}, Максимум: {mx}")  # Мінімум: -8, Максимум: 12

    # pair = min_max_dc(data)
    # print(pair)              # -> (-8, 12)

    # Перевірка на одиничному та парі елементів
    print(min_max_dc([42]))        # (42, 42)
    print(min_max_dc([3, -1]))     # (-1, 3)
    print(min_max_dc([-5, -10]))   # (-10, -5)