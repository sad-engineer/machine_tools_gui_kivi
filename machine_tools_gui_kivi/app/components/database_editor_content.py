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
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout

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

        # Создаем шаблон поиска
        self.search_bar = SearchBar(
            input_hint="Введите название станка",
            button_text="Поиск",
            input_ratio=0.8,
            height=35,
            debug_mode=self.debug_mode,
        )
        self.search_bar.size_hint = (1, None)
        self.search_bar.pos_hint = {'top': 1}

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
        # Основной контейнер
        left_col = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=5,
            padding=[5, 5, 5, 5]
        )

        # Создаем ScrollView
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=['bars'],
            bar_width=10
        )

        # Создаем контейнер для полей ввода
        fields_container = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None,
            padding=[0, 0, 0, 0]
        )
        fields_container.bind(minimum_height=fields_container.setter('height'))

        # Поле поиска станка по имени
        self.search_bar = SearchBar(
            input_hint="Введите название станка",
            button_text="Поиск",
            input_ratio=0.8,
            height=35,
            debug_mode=self.debug_mode,
        )
        self.search_bar.size_hint = (1, None)
        self.search_bar.pos_hint = {'top': 1}

        # Лейбл с надписью "Группа станка"
        group_label = Label(
            text="Группа станка",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода группы станка
        self.group_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Тип станка"
        type_label = Label(
            text="Тип станка",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода типа станка
        self.type_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        self.machine_type_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Мощность"
        power_label = Label(
            text="Мощность",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода мощности
        self.power_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "КПД"
        efficiency_label = Label(
            text="КПД",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода КПД
        self.efficiency_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Точность"
        accuracy_label = Label(
            text="Точность",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода точности
        self.accuracy_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Автоматизация"
        automation_label = Label(
            text="Автоматизация",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода автоматизации
        self.automation_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Специализация    "
        specialization_label = Label(
            text="Специализация",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода специализации
        self.specialization_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Масса"
        mass_label = Label(
            text="Масса",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода массы
        self.mass_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Класс станка по массе    "
        mass_class_label = Label(
            text="Класс станка по массе",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода класса станка по массе
        self.mass_class_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Город производства"
        production_city_label = Label(
            text="Город производства",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода города производства
        self.production_city_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        #Лейбл с надписью "Организация-производитель"
        organization_label = Label(
            text="Организация-производитель",
            size_hint=(1, None),
            height=30,
            halign="left"
        )
        #Поле для ввода организации-производителя
        self.organization_input = TextInput(
            size_hint=(1, None),
            height=30,
            halign="left"
        )

        # Добавляем все виджеты в left_col
        fields_container.add_widget(self.search_bar)
        fields_container.add_widget(group_label)
        fields_container.add_widget(self.group_input)
        fields_container.add_widget(type_label)
        fields_container.add_widget(self.type_input)
        fields_container.add_widget(self.machine_type_input)
        fields_container.add_widget(power_label)
        fields_container.add_widget(self.power_input)
        fields_container.add_widget(efficiency_label)
        fields_container.add_widget(self.efficiency_input)
        fields_container.add_widget(accuracy_label)
        fields_container.add_widget(self.accuracy_input)
        fields_container.add_widget(automation_label)
        fields_container.add_widget(self.automation_input)
        fields_container.add_widget(specialization_label)
        fields_container.add_widget(self.specialization_input)
        fields_container.add_widget(mass_label)
        fields_container.add_widget(self.mass_input)
        fields_container.add_widget(mass_class_label)
        fields_container.add_widget(self.mass_class_input)
        fields_container.add_widget(production_city_label)
        fields_container.add_widget(self.production_city_input)
        fields_container.add_widget(organization_label)
        fields_container.add_widget(self.organization_input)

        # Добавляем контейнер с полями в ScrollView
        scroll_view.add_widget(fields_container)
        left_col.add_widget(scroll_view)

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

        # Привязываем отладочные обновления
        if self.debug_mode:
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