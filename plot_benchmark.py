"""
Визуализация «чистого» бенчмарка факториала.

Идея:
- Переиспользуем функции и фиксированный набор входов из Шага 2.
- Замеряем время для fact_recursive и fact_iterative (минимум из repeat запусков).
- Строим график: X — n, Y — время (сек). Сохраняем PNG и CSV.

Файлы на выходе:
- benchmark_results.png — картинка с графиком.
- benchmark_results.csv — таблица с результатами (n, t_recursive, t_iterative).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt  # matplotlib нужен для графика

# Импортируем из предыдущих шагов:
from factorial import fact_recursive, fact_iterative
from benchmark_timeit import make_fixed_inputs, benchmark_one_call


def collect_data(repeat: int = 7) -> tuple[list[int], list[float], list[float]]:
    """Соберите данные времени для обоих подходов на фиксированных n.

    Возвращает:
        (n_values, times_recursive, times_iterative)
    """
    n_values: list[int] = make_fixed_inputs(k=10)
    times_recursive: list[float] = []
    times_iterative: list[float] = []

    for n in n_values:
        t_rec = benchmark_one_call(fact_recursive, n, repeat=repeat)
        t_it = benchmark_one_call(fact_iterative, n, repeat=repeat)
        times_recursive.append(t_rec)
        times_iterative.append(t_it)

    return n_values, times_recursive, times_iterative


def save_csv(path: Path, n_vals: list[int], t_rec: list[float], t_it: list[float]) -> None:
    """Сохраните результаты в CSV для отчёта/проверки."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "time_recursive_sec", "time_iterative_sec"])
        for n, a, b in zip(n_vals, t_rec, t_it, strict=True):
            writer.writerow([n, f"{a:.9e}", f"{b:.9e}"])


def plot_times(n_vals: list[int], t_rec: list[float], t_it: list[float]) -> None:
    """Постройте и покажите график зависимости времени от n."""
    plt.figure(figsize=(8, 5))
    # Линии без специальных стилей — достаточно подписей и маркеров для наглядности.
    plt.plot(n_vals, t_rec, marker="o", label="Рекурсивная (fact_recursive)")
    plt.plot(n_vals, t_it, marker="s", label="Итеративная (fact_iterative)")
    plt.title("Сравнение времени выполнения n! (чистый бенчмарк, number=1)")
    plt.xlabel("n (размер входа)")
    plt.ylabel("время, секунды (меньше — лучше)")
    plt.legend()
    plt.grid(True)

    out_png: Final[Path] = Path("benchmark_results.png")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    print(f"График сохранён в: {out_png.resolve()}")

    # Показать окно с графиком (можно закрыть крестиком)
    plt.show()


def main() -> None:
    """Соберите данные, сохраните CSV и постройте график."""
    n_vals, t_rec, t_it = collect_data(repeat=7)

    # Сохраняем CSV рядом со скриптом
    out_csv = Path("benchmark_results.csv")
    save_csv(out_csv, n_vals, t_rec, t_it)
    print(f"CSV c результатами сохранён в: {out_csv.resolve()}")

    # Рисуем график и сохраняем PNG
    plot_times(n_vals, t_rec, t_it)


if __name__ == "__main__":
    main()
