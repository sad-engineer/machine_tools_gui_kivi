#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools import get_finder_with_list_names as finder
import timeit

MACHINE_TOOL_NAMES = finder().all()


def filter_names(name: str) -> list[str]:
    """Фильтрует список машин по имени."""
    if len(name) == 0:
        return MACHINE_TOOL_NAMES
    return [machine_name for machine_name in MACHINE_TOOL_NAMES if name in machine_name]


def filter_names1(name: str) -> list[str]:
    """Фильтрует список машин по имени."""
    # if len(name) == 0:
    #     return MACHINE_TOOL_NAMES
    return [machine_name for machine_name in MACHINE_TOOL_NAMES if name in machine_name]


if __name__ == "__main__":
    print(filter_names(""))

    # Пример строки для поиска
    search_str = ""

    # Обернем вызовы функций в лямбды для timeit
    t1 = timeit.timeit(lambda: filter_names(search_str), number=1000)
    t2 = timeit.timeit(lambda: filter_names1(search_str), number=1000)

    print(f"filter_names:  {t1:.6f} сек")
    print(f"filter_names1: {t2:.6f} сек")
