#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна ввода данных, наследующий от шаблонного окна.
"""
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel

from machine_tools_gui_kivi.app.components.template_window import \
    TemplateWindow


class TemplateDatabaseEditorWindow(TemplateWindow):
    """
    Окно вводаи редактирования данных, наследующее от шаблонного окна.
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(screen_manager=screen_manager, debug_mode=debug_mode, **kwargs)


class DatabaseEditorWindow(Screen):
    """Окно ввода данных, обертка для TemplateInputWindow."""

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.name = "input_window"
        # Создаем и добавляем TemplateInputWindow
        self.template_window = TemplateDatabaseEditorWindow(
            screen_manager=screen_manager, debug_mode=debug_mode
        )
        self.add_widget(self.template_window)


if __name__ == "__main__":

    class TestApp(MDApp):
        """Тестовое приложение для отладки окна."""

        def build(self):
            """Создает и возвращает главное окно приложения."""
            Window.minimum_width = 910
            Window.minimum_height = 500
            window = DatabaseEditorWindow(debug_mode=True)
            return window

    TestApp().run()
