#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools import MachineInfo, MachineFinder

machine_finder = MachineFinder()
MACHINE_TOOL_NAMES = machine_finder.all()


def filter_names(name: str) -> list[str]:
    """Фильтрует список машин по имени."""
    return [machine_name for machine_name in MACHINE_TOOL_NAMES if name in machine_name]


if __name__ == "__main__":
    print(filter_names("16К20"))
