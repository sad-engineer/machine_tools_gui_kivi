#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Union

from machine_tools import (ACCURACY_DESCRIPTIONS, GROUP_DESCRIPTIONS,
                           TYPE_DESCRIPTIONS)


def get_group_fields_descriptions() -> list[str]:
    """
    Возвращает список описаний групп станков.

    Формат:
    <номер группы>: <описание группы>

    Например:
    1: Токарные
    2: Сверлильные и расточные
    3: Шлифовальные, полировальные, доводочные
    4: Комбинированные
    5: Зубообрабатывающие и резьбообрабатывающие
    6: Фрезерные
    7: Строгальные, долбежные и протяжные
    8: Разрезные
    9: Разные

    :return: список описаний групп станков

    Из описания группы удаляется слово "станки" для удобства чтения
    и более короткой записи в выпадающем списке.
    Сами группы определяются в пакете machine_tools.
    """
    fields = []
    for group, descriptions in GROUP_DESCRIPTIONS.items():
        descriptions = descriptions.replace(" станки", "")
        field = f"{group}: {descriptions}"
        fields.append(field)
    return fields


GROUP_FIELDS_DESCRIPTIONS = get_group_fields_descriptions()


def get_type_fields_descriptions(group_id: Union[int, str]) -> list[str]:
    """
    Возвращает список описаний типов станков.

    Параметры:
    group_id: int|str - номер группы станков. Доступные типы станков определяются для конкретной группы.

    Формат:
    <номер типа>: <описание типа>

    Например:
    1: Вертикально-сверлильные
    2: Полуавтоматы одношпиндельные
    3: Полуавтоматы многошпиндельные
    4: Координатно-расточные
    5: Радиально-сверлильные
    6: Горизонтально-расточные
    7: Алмазно-расточные
    8: Горизонтально-сверлильные
    9: Разные

    :return: список описаний типов станков

    Сами типы определяются в пакете machine_tools.
    """
    group_id = str(group_id)
    fields = []
    for type_, descriptions in TYPE_DESCRIPTIONS.items():
        if type_.startswith(group_id):
            type_ = type_.replace(f"{group_id}, ", "", 1)
            field = f"{type_}: {descriptions}"
            fields.append(field)
    return fields


def get_accuracy_fields_descriptions() -> list[str]:
    """
    Возвращает список описаний точности станков (Только описание).
    """
    return ACCURACY_DESCRIPTIONS.values()


def get_accuracy_by_description(description: str) -> str:
    """
    Возвращает точность станка по его описанию.
    """
    return list(ACCURACY_DESCRIPTIONS.keys())[
        list(ACCURACY_DESCRIPTIONS.values()).index(description)
    ]
