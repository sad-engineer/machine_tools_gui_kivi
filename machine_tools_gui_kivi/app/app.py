#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль с основным классом приложения.
"""

from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from machine_tools_gui_kivi.app.windows import DatabaseEditorWindow

Config.set("input", "mouse", "mouse, multitouch_on_demand")


class MainScreen(Screen):
    """Главный экран приложения."""

    pass


class WorkshopDesignApp(MDApp):
    """
    Основной класс приложения.

    Attributes:
        theme_cls: Класс для управления темой приложения
    """

    def __init__(self, theme: str = "Dark", **kwargs):
        """
        Инициализирует приложение.

        Args:
            config: Конфигурация приложения
            **kwargs: Дополнительные аргументы
        """
        super().__init__(**kwargs)

        # Устанавливаем тему
        self.theme_cls.theme_style = theme

        # Устанавливаем размер окна
        Window.minimum_width = 910
        Window.minimum_height = 500

        # Устанавливаем цветовую схему по умолчанию
        self.theme_cls.primary_palette = "Blue"  # Основной цвет
        self.theme_cls.accent_palette = "Amber"  # Акцентный цвет
        self.theme_cls.material_style = "M3"  # Использовать Material Design 3

    def build(self) -> MDScreen:
        """
        Создает и возвращает корневой виджет приложения.

        Returns:
            MDScreen: Корневой виджет приложения
        """
        # Устанавливаем название приложения
        self.title = "Станки"
        # Создаем менеджер экранов
        self.screen_manager = ScreenManager()
        # Создаем и добавляем окно ввода
        database_editor = DatabaseEditorWindow(screen_manager=self.screen_manager)
        self.screen_manager.add_widget(database_editor)

        # Устанавливаем размер окна
        Window.size = (910, 600)

        return self.screen_manager

    def toggle_theme(self, instance):
        """Переключает между светлой и темной темой."""
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def show_settings(self, instance):
        """Показывает окно настроек."""
        self.screen_manager.current = "settings"


if __name__ == "__main__":
    WorkshopDesignApp().run()
