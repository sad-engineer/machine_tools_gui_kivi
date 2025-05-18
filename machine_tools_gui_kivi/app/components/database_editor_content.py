#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна ввода данных, наследующий от шаблонного окна.
"""
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.spinner import Spinner

from machine_tools_gui_kivi.app.components.template_window import \
    TemplateWindow
from machine_tools_gui_kivi.src.machine_finder import MACHINE_TOOL_NAMES, filter_names
from machine_tools_gui_kivi.app.components.dropdown_list import DropdownList
from machine_tools_gui_kivi.app.components.searchbar import SearchBar


class TemplateDatabaseEditorContent(BoxLayout):
    """
    Шаблон-контейнер для окна редактирования базы данных с двумя колонками.
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(orientation="horizontal", spacing=10, padding=[5, 5, 5, 5], **kwargs)
        self.screen_manager = screen_manager
        self.debug_mode = debug_mode
        self._init_content()

    def _init_content(self):
        """Инициализирует контент окна."""
        content = BoxLayout(
            orientation="horizontal",
            spacing=5,
        )

        # Создаем колонки
        left_col = self._fill_left_column()
        right_col = self._fill_right_column()

        # Добавляем колонки в основной контейнер
        content.add_widget(left_col)
        content.add_widget(right_col)
        self.add_widget(content)

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

    def _fill_left_column(self):
        """Наполняет левую колонку виджетами."""
        left_col = BoxLayout(orientation="vertical")
        # Добавляем шаблон поиска
        self.search_bar = SearchBar(
            input_hint="Введите название станка",
            button_text="Поиск",
            input_ratio=0.8,
            height=35,
            debug_mode=self.debug_mode,
        )
        self.search_bar.size_hint = (1, None)
        self.search_bar.pos_hint = {'top': 1}

        left_col.add_widget(self.search_bar)
        left_col.add_widget(Widget(size_hint_y=1))

        # Добавляем выпадающий список
        self.search_bar_dropdown = DropdownList(
            size_hint=(0.4, None),
            height=200,
            item_height=30,
            item_spacing=2,
            bar_width=10,
            item_cols=2,
            opacity=0
        )
        # Не добавляем в корневой контейнер. Добавим в контейнер окна и будем пересчитывать координаты там

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


