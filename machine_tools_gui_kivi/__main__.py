#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Точка входа в приложение.
Запускает GUI приложение для работы с базой данных станков.
"""

import argparse
from machine_tools_gui_kivi.app.app import WorkshopDesignApp


def main():
    """Основная функция запуска приложения."""
    parser = argparse.ArgumentParser(description="Machine Tools GUI Application")
    parser.add_argument("command", choices=["run"], help="Command to execute")
    args = parser.parse_args()

    if args.command == "run":
        WorkshopDesignApp().run()


if __name__ == "__main__":
    main()
