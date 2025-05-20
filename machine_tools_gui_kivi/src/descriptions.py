#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools import GROUP_DESCRIPTIONS

# GROUP_DESCRIPTIONS = {
#     1: 'Токарные станки',
#     2: 'Сверлильные и расточные станки',
#     3: 'Шлифовальные, полировальные, доводочные станки',
#     4: 'Комбинированные',
#     5: 'Зубообрабатывающие и резьбообрабатывающие станки',
#     6: 'Фрезерные станки',
#     7: 'Строгальные, долбежные и протяжные станки',
#     8: 'Разрезные станки',
#     9: 'Разные станки',
# }


def get_group_fields_descriptions():
    fields = []
    for group, descriptions in GROUP_DESCRIPTIONS.items():
        descriptions = descriptions.replace(" станки", "")
        field = f"{group}: {descriptions}"
        fields.append(field)
    return fields


GROUP_FIELDS_DESCRIPTIONS = get_group_fields_descriptions()
