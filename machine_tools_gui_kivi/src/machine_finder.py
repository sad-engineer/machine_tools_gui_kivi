#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import timeit
import machine_tools
print(machine_tools.__file__)

from machine_tools import Finder, ListMachineInfoFormatter

with Finder(limit=None) as finder:
    MACHINE_TOOL_NAMES = finder.find_all()


def filter_names(name: str) -> list[str]:
    """Фильтрует список машин по имени."""
    if len(name) == 0:
        return MACHINE_TOOL_NAMES
    return [machine_name for machine_name in MACHINE_TOOL_NAMES if name in machine_name]


def filter_names1(name: str) -> list[str]:
    """Фильтрует список машин по имени."""
    return [machine_name for machine_name in MACHINE_TOOL_NAMES if name in machine_name]


def info_by_name(name: str) -> dict:
    """Возвращает информацию о машине по имени."""
    with Finder(limit=None) as finder:
        finder.set_formatter(ListMachineInfoFormatter())
        machine = finder.find_by_name(name=name, exact_match=True)
        print(machine)
        return machine[0]



if __name__ == "__main__":
    # print(filter_names(""))
    #
    # # Пример строки для поиска
    # search_str = ""
    #
    # # Обернем вызовы функций в лямбды для timeit
    # t1 = timeit.timeit(lambda: filter_names(search_str), number=1000)
    # t2 = timeit.timeit(lambda: filter_names1(search_str), number=1000)
    #
    # print(f"filter_names:  {t1:.6f} сек")
    # print(f"filter_names1: {t2:.6f} сек")
    #
    # from machine_tools import info_by_name
    # for name in MACHINE_TOOL_NAMES:
    #     try:
    #         info = info_by_name(name)
    #         if not info:
    #             print(name)
    #     except Exception as e:
    #         print(name)
    #         print(e)
    
    info = info_by_name("16К20Ф3")
    print(f"{info.name} {info.software_control}")

