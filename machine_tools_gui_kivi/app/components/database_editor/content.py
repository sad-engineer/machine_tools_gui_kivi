#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна ввода данных, наследующий от шаблонного окна.
"""
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

from machine_tools_gui_kivi.app.components.database_editor.left_column import \
    LeftColumn
from machine_tools_gui_kivi.app.components.searchbar import SearchBar
from machine_tools_gui_kivi.app.components.database_editor.right_column import \
    RightColumn


class TemplateDatabaseEditor(BoxLayout):
    """
    Шаблон-контейнер для окна редактирования базы данных с двумя колонками.
    """

    def __init__(self, screen_manager=None, debug_mode=False, on_technical_requirements_change=None, on_technical_requirement_name_change=None, **kwargs):
        super().__init__(
            orientation="horizontal", spacing=10, padding=[5, 5, 5, 5], **kwargs
        )
        self.screen_manager = screen_manager
        self.debug_mode = debug_mode
        self.on_technical_requirements_change = on_technical_requirements_change
        self.on_technical_requirement_name_change = on_technical_requirement_name_change

        # Создаем шаблон поиска
        self.search_bar = SearchBar(
            input_hint="Введите название станка",
            button_text="Поиск",
            input_ratio=0.8,
            height=35,
            debug_mode=self.debug_mode,
        )
        self.search_bar.size_hint = (1, None)
        self.search_bar.pos_hint = {"top": 1}

        self._init_content()

    def _init_content(self):
        """Инициализирует контент окна."""
        content = BoxLayout(
            orientation="horizontal",
            spacing=5,
        )

        # Создаем колонки
        self.left_col = LeftColumn(debug_mode=self.debug_mode)
        self.right_col = RightColumn(
            debug_mode=self.debug_mode,
            on_property_change=self._on_property_change,
            on_property_name_change=self._on_property_name_change
        )

        # Добавляем колонки в основной контейнер
        content.add_widget(self.left_col)
        content.add_widget(self.right_col)
        self.add_widget(content)

        # Привязываем отладочные обновления
        content.bind(
            pos=self._update_template_content_debug,
            size=self._update_template_content_debug,
        )
        self.left_col.bind(
            pos=self._update_template_content_debug,
            size=self._update_template_content_debug,
        )
        self.right_col.bind(
            pos=self._update_template_content_debug,
            size=self._update_template_content_debug,
        )

    def _fill_right_column(self):
        """Наполняет правую колонку виджетами."""
        right_col = BoxLayout(orientation="vertical")
        right_col.bind(
            pos=self._update_right_col_debug, size=self._update_right_col_debug
        )
        return right_col

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

    def _on_property_change(self, property_name, value):
        """
        Обработчик изменения значения свойства в правой колонке.
        
        Args:
            property_name: Название свойства
            value: Новое значение
        """
        if self.on_technical_requirements_change:
            self.on_technical_requirements_change(property_name, value)
        # Здесь можно обновить соответствующие поля в левой колонке
        # Например:
        if property_name == "Мощность":
            self.left_col.power_input.input_field.text = value
        elif property_name == "КПД":
            self.left_col.efficiency_input.input_field.text = value
        # Добавьте обработку других свойств по необходимости

    def _on_property_name_change(self, old_name, new_name):
        """
        Обработчик изменения названия свойства в правой колонке.
        
        Args:
            old_name: Старое название свойства
            new_name: Новое название свойства
        """
        if self.on_technical_requirement_name_change:
            self.on_technical_requirement_name_change(old_name, new_name)
