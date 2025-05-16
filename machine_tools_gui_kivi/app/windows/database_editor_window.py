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
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

from machine_tools_gui_kivi.app.components.template_window import \
    TemplateWindow
from machine_tools_gui_kivi.src.machine_finder import MACHINE_TOOL_NAMES, filter_names
from machine_tools_gui_kivi.app.components.search_template import SearchTemplate


class TemplateDatabaseEditorWindow(TemplateWindow):
    """
    Окно вводаи редактирования данных, наследующее от шаблонного окна.
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(screen_manager=screen_manager, debug_mode=debug_mode, **kwargs)
        # Инициализируем наш контент
        self._init_content()

    def _init_content(self):
        """Инициализирует контент окна."""
        self.content = self._create_template_content()
        self.root_box.add_widget(self.content)

    def _create_template_content(self):
        """Создает основной контент окна с двумя колонками."""
        # Создаем горизонтальный контейнер для колонок
        content = BoxLayout(
            orientation="horizontal",
            padding=[5, 5, 5, 5],
            spacing=10,
        )

        # Создаем колонки
        left_col = self._fill_left_column()
        right_col = self._fill_right_column()

        # Добавляем колонки в основной контейнер
        content.add_widget(left_col)
        content.add_widget(right_col)

        # Привязываем отладочные обновления
        content.bind(
            pos=self._update_template_content_debug,
            size=self._update_template_content_debug,
        )
        left_col.bind(
            pos=self._update_template_content_debug,
            size=self._update_template_content_debug,
        )
        right_col.bind(
            pos=self._update_template_content_debug,
            size=self._update_template_content_debug,
        )

        return content

    def _fill_left_column(self):
        """Наполняет левую колонку виджетами."""
        left_col = BoxLayout(orientation="vertical")
        # Добавляем шаблон поиска
        search_template = SearchTemplate()
        left_col.add_widget(search_template)
        left_col.bind(pos=self._update_left_col_debug, size=self._update_left_col_debug)
        return left_col

    def _fill_right_column(self):
        """Наполняет правую колонку виджетами."""
        right_col = BoxLayout(orientation="vertical")
        right_col.bind(pos=self._update_right_col_debug, size=self._update_right_col_debug)
        return right_col

    def _update_left_col_debug(self, instance, value):
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 0, 0.3)  # Черный с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)

    def _update_right_col_debug(self, instance, value):
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 1, 0.3)  # Синий с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)

    def _update_template_content_debug(self, instance, value):
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 0, 0.3)  # Черный с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)

    def _init_buttons(self):
        """Инициализирует кнопки управления."""
        # Очищаем существующие кнопки
        self.buttons_box.clear_widgets()

        # Создаем новые кнопки
        calc_btn = Button(
            text='Начать расчет', size_hint=(None, 1), width=self.max_button_width, on_release=self.save_data
        )
        cancel_btn = Button(text='Отмена', size_hint=(None, 1), width=self.max_button_width, on_release=self.cancel)

        # Добавляем кнопки в контейнер
        self.buttons_box.add_widget(calc_btn)
        self.buttons_box.add_widget(cancel_btn)

    def _create_search_field(self):
        """Создает поле поиска станка."""
        # Создаем контейнер для поля поиска
        search_box = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50,
            padding=[0, 0, 0, 10],
            spacing=5,
            pos_hint={'top': 1}  # Привязка к верхнему краю
        )

        # Создаем поле ввода
        self.search_input = TextInput(
            hint_text="Введите название станка для поиска",
            multiline=False,
            halign='center',
            size_hint=(0.8, 1),
            on_text=self._on_search_text_changed
        )

        # Создаем выпадающий список
        self.search_spinner = Spinner(
            text='Выберите станок',
            values=[],
            size_hint=(0.8, 1),
            pos_hint={'top': 1},
            opacity=0  # Используем opacity вместо visible
        )

        # Создаем кнопку поиска
        self.search_button = Button(
            text="Поиск",
            size_hint=(0.2, 1),
            on_release=self._on_search
        )

        # Добавляем виджеты в контейнер
        search_box.add_widget(self.search_input)
        search_box.add_widget(self.search_button)

        # Создаем контейнер для выпадающего списка
        self.spinner_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=0,
            pos_hint={'top': 1}
        )
        self.spinner_container.add_widget(self.search_spinner)

        # Добавляем контейнеры в левую колонку
        left_col = BoxLayout(orientation="vertical")
        left_col.add_widget(search_box)
        left_col.add_widget(self.spinner_container)
        left_col.add_widget(Widget(size_hint_y=1))

        return left_col

    def _on_search_text_changed(self, instance, value):
        """Обработчик изменения текста в поле поиска."""
        if value:
            self._update_spinner_trigger()
        else:
            self.search_spinner.values = []
            self.search_spinner.opacity = 0
            self.spinner_container.height = 0

    def _update_spinner_values(self, dt):
        """Обновляет значения в выпадающем списке."""
        search_text = self.search_input.text
        if search_text:
            filtered_names = filter_names(search_text)
            if filtered_names:
                self.search_spinner.values = filtered_names
                self.search_spinner.opacity = 1
                self.spinner_container.height = 200  # Высота выпадающего списка
            else:
                self.search_spinner.values = []
                self.search_spinner.opacity = 0
                self.spinner_container.height = 0

    def _on_search(self, instance):
        """Обработчик нажатия кнопки поиска."""
        search_text = self.search_input.text
        if search_text:
            # TODO: Реализовать поиск в БД
            print(f"Поиск станка: {search_text}")



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
            Window.minimum_width = 1280
            Window.minimum_height = 720
            window = DatabaseEditorWindow(debug_mode=True)
            return window

    TestApp().run()
