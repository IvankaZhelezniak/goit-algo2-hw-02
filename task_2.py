# Завдання 2. Оптимізація черги 3D-принтера в університетській лабораторії.

# Розробіть програму для оптимізації черги завдань 3D-друку 
# з урахуванням пріоритетів та технічних обмежень принтера, використовуючи жадібний алгоритм.

from typing import List, Dict
from dataclasses import dataclass, field

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int
    order: int = field(default=0)  # стабільне впорядкування за початковою позицією

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def _to_dataclasses(print_jobs: List[Dict], constraints: Dict) -> tuple[list[PrintJob], PrinterConstraints]:
    jobs: list[PrintJob] = []
    for i, j in enumerate(print_jobs):
        job = PrintJob(
            id=str(j["id"]),
            volume=float(j["volume"]),
            priority=int(j["priority"]),
            print_time=int(j["print_time"]),
            order=i
        )
        if job.volume <= 0 or job.print_time <= 0:
            raise ValueError(f"Некоректні дані завдання {job.id}: volume/print_time мають бути > 0")
        if job.priority not in (1, 2, 3):
            raise ValueError(f"Некоректний пріоритет у {job.id}: {job.priority}")
        jobs.append(job)

    cons = PrinterConstraints(
        max_volume=float(constraints["max_volume"]),
        max_items=int(constraints["max_items"]),
    )
    if cons.max_volume <= 0 or cons.max_items <= 0:
        raise ValueError("Обмеження принтера мають бути додатними")
    return jobs, cons

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера.
    Жадібна стратегія: беремо завдання у порядку (priority ↑, початковий порядок ↑),
    формує поточну партію, додаючи наступні завдання, які ще в черзі і поміщаються
    у ліміти max_volume та max_items. Час партії — максимум з print_time.
    """
    jobs, cons = _to_dataclasses(print_jobs, constraints)

    # 1) Спочатку впорядковує за пріоритетом (1 вище), потім стабільно за початковим порядком
    remaining = sorted(jobs, key=lambda x: (x.priority, x.order))

    total_time = 0
    print_order: list[str] = []

    # 2) Поки є завдання — формує наступну партію
    while remaining:
        batch: list[PrintJob] = []
        used_idx: list[int] = []
        cur_vol = 0.0
        cur_cnt = 0
        batch_max_time = 0

        # Жадібно проходимо по впорядкованому списку і забирає те, що вміщується
        for idx, job in enumerate(remaining):
            if cur_cnt >= cons.max_items:
                break
            if cur_vol + job.volume <= cons.max_volume and cur_cnt + 1 <= cons.max_items:
                batch.append(job)
                used_idx.append(idx)
                cur_vol += job.volume
                cur_cnt += 1
                if job.print_time > batch_max_time:
                    batch_max_time = job.print_time

        # Безпека: якщо з якоїсь причини не змогли додати жодного (занадто малі ліміти)
        if not batch:
            # Бере перше (найпріоритетніше), друкує окремо
            job = remaining[0]
            batch = [job]
            used_idx = [0]
            batch_max_time = job.print_time

        # Додає час партії
        total_time += batch_max_time
        # Додає порядок друку (ідентифікатори завдань)
        print_order.extend([j.id for j in batch])

        # Прибирає надруковані з черги (з кінця, щоб індекси не зсувалися)
        for i in reversed(used_idx):
            remaining.pop(i)

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
