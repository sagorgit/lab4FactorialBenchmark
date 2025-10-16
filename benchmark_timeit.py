"""
Бенчмарк двух реализаций факториала с использованием timeit.

Идея:
- Используем ОДИН фиксированный набор входов (список n) для обоих функций.
- Для каждого n делаем «чистый» замер времени одного вызова (number=1)
  и несколько повторений (repeat), затем берём минимум (наименее зашумлённое).
- Сравниваем рекурсивную и итеративную версии на одинаковом наборе n.

Почему минимум?
- По документации timeit более информативно брать минимальное время из повторов,
  так как оно ближе к «нижней границе» без случайных задержек ОС/фона.
"""

from __future__ import annotations

import random
import timeit
from typing import Callable, Final

# Импортируем наши функции из файла Шага 1
from factorial import fact_recursive, fact_iterative


def benchmark_one_call(func: Callable[[int], int], n: int, repeat: int = 7) -> float:
    """Замерьте «чистое» время одного вызова func(n) в секундах.

    Параметры:
        func: вызываемая функция от одного аргумента n -> int.
        n: целевой вход для факториала.
        repeat: сколько раз повторить замер (берём минимум).

    Возвращает:
        Наименьшее время (в секундах) из repeat запусков одного вызова.
    """
    # Создаём вызываемый объект без аргументов (lambda закрывает n)
    stmt = lambda: func(n)  # noqa: E731 — намеренно краткая лямбда
    # number=1 => «один вызов» за прогон; repeat — сколько прогонов.
    times: list[float] = timeit.repeat(stmt, number=1, repeat=repeat)
    best: float = min(times)
    return best


def make_fixed_inputs(k: int = 10) -> list[int]:
    """Сформируйте фиксированный список входов для всех прогонов.

    Мы фиксируем seed, чтобы набор всегда получался одинаковым.
    Значения берём умеренные, чтобы не упереться в лимит рекурсии Python.
    """
    FIXED_SEED: Final[int] = 20251015  # фиксируем дату как seed
    random.seed(FIXED_SEED)
    # Возьмём k уникальных чисел из диапазона [20, 300] и отсортируем.
    # Почему с 20? Так немного нивелируем «очень маленькие» n,
    # но остаёмся далеко от лимита рекурсии (~1000 уровней).
    values = sorted(random.sample(range(20, 300), k))
    return values


def main() -> None:
    """Запустите «чистый» бенчмарк и распечатайте таблицу результатов."""
    n_values = make_fixed_inputs(k=10)

    print("Фиксированный набор n:", n_values)
    print("Повторы (repeat) = 7, number = 1 (единственный вызов на замер)")
    print()
    print("Результаты (секунды, меньше — лучше):")
    print(f"{'n':>5} | {'recursive':>12} | {'iterative':>12} | faster")
    print("-" * 50)

    for n in n_values:
        t_rec = benchmark_one_call(fact_recursive, n, repeat=7)
        t_it = benchmark_one_call(fact_iterative, n, repeat=7)
        faster = "Iterative" if t_it < t_rec else ("Recursive" if t_rec < t_it else "≈ tie")
        print(f"{n:>5} | {t_rec:>12.6e} | {t_it:>12.6e} | {faster}")

    print("\nПояснение:")
    print("- Мы использовали ОДИН и тот же список n для обеих функций.")
    print("- Для каждого n был замер «одного вызова» (number=1) несколько раз (repeat=7),")
    print("  и выбран МИНИМУМ — наименее зашумлённый результат.")


if __name__ == "__main__":
    main()
