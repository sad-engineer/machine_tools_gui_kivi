#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс левой колонки редактора базы данных.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from machine_tools_gui_kivi.app.components.dropdown_list import DropdownList
from machine_tools_gui_kivi.app.components.labeled_spinner import \
    LabeledSpinner
from machine_tools_gui_kivi.app.components.searchbar import SearchBar
from machine_tools_gui_kivi.src.descriptions import \
    get_group_fields_descriptions as get_group_fields
from machine_tools_gui_kivi.src.descriptions import \
    get_type_fields_descriptions as get_type_fields


class LeftColumn(BoxLayout):
    """
    Класс левой колонки редактора базы данных.
    """

    def __init__(self, debug_mode=False, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint=(1, 1),
            spacing=5,
            padding=[5, 5, 5, 5],
            **kwargs
        )
        self.debug_mode = debug_mode
        self._init_content()

    def _init_content(self):
        """Инициализирует контент колонки."""
        # Создаем ScrollView
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=["bars"],
            bar_width=10,
        )

        # Создаем контейнер для полей ввода
        fields_container = GridLayout(
            cols=1, spacing=5, size_hint_y=None, padding=[0, 0, 0, 0]
        )
        fields_container.bind(minimum_height=fields_container.setter("height"))

        # Создаем и добавляем все виджеты
        self._create_widgets(fields_container)

        # Добавляем контейнер с полями в ScrollView
        scroll_view.add_widget(fields_container)
        self.add_widget(scroll_view)

    def _create_widgets(self, container):
        """Создает и добавляет все виджеты в контейнер."""
        # Поле поиска
        self.search_bar = SearchBar(
            input_hint="Введите название станка",
            button_text="Поиск",
            input_ratio=0.8,
            height=35,
            debug_mode=self.debug_mode,
        )
        self.search_bar.size_hint = (1, None)
        self.search_bar.pos_hint = {"top": 1}
        self.add_widget(self.search_bar)

        # Группа станка
        self.group_spinner = LabeledSpinner(
            label_text="Группа станка:",
            values=get_group_fields(),
            height=65,
            debug_mode=self.debug_mode,
        )
        self.group_spinner.size_hint = (1, None)
        self.group_spinner.pos_hint = {"top": 1}
        container.add_widget(self.group_spinner)

        # Тип станка
        self.type_spinner = LabeledSpinner(
            label_text="Тип станка:",
            values=get_type_fields(self.group_spinner.spinner.text[:1]),
            height=65,
            debug_mode=self.debug_mode,
        )
        self.type_spinner.size_hint = (1, None)
        self.type_spinner.pos_hint = {"top": 1}
        container.add_widget(self.type_spinner)

        # Остальные поля
        self._create_label_and_input(
            container, "Тип станка (доп.):", "machine_type_input"
        )
        self._create_label_and_input(container, "Мощность:", "power_input", "кВт")
        self._create_label_and_input(container, "КПД:", "efficiency_input", "%")
        self._create_label_and_input(container, "Точность:", "accuracy_input")
        self._create_label_and_input(container, "Автоматизация:", "automation_input")
        self._create_label_and_input(
            container, "Специализация:", "specialization_input"
        )
        self._create_label_and_input(container, "Масса:", "mass_input", "кг")
        self._create_label_and_input(
            container, "Класс станка по массе:", "mass_class_input"
        )
        self._create_label_and_input(
            container, "Город производства:", "production_city_input"
        )
        self._create_label_and_input(
            container, "Организация-производитель:", "organization_input"
        )

        # Добавляем выпадающий список
        self.search_bar_dropdown = DropdownList(
            size_hint=(0.4, None),
            height=200,
            item_height=30,
            item_spacing=2,
            bar_width=10,
            item_cols=2,
            opacity=0,
        )

    def _create_label_and_input(self, container, label_text, input_name, units=None):
        """Создает пару лейбл + поле ввода и добавляет их в контейнер.

        Args:
            container: Контейнер для виджетов
            label_text: Текст лейбла
            input_name: Имя атрибута для поля ввода
            units: Единицы измерения (опционально)
        """
        # Создаем лейбл
        label = Label(
            text=label_text,
            size_hint=(1, None),
            height=30,
            halign="left",
            valign="middle",
        )
        label.bind(
            size=lambda *x: setattr(label, "text_size", (label.width, label.height))
        )

        # Создаем контейнер для поля ввода и единиц измерения
        input_container = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=30, spacing=5
        )

        # Создаем поле ввода
        input_field = TextInput(size_hint=(1, None), height=30, halign="left")
        input_container.add_widget(input_field)

        # Если есть единицы измерения, добавляем их лейбл
        if units:
            units_label = Label(
                text=units,
                size_hint=(None, None),
                height=30,
                width=30,
                halign="left",
                valign="middle",
            )
            units_label.bind(
                size=lambda *x: setattr(
                    units_label, "text_size", (units_label.width, units_label.height)
                )
            )
            input_container.add_widget(units_label)

        # Добавляем в контейнер
        container.add_widget(label)
        container.add_widget(input_container)

        # Сохраняем ссылку на поле ввода
        setattr(self, input_name, input_field)

    def _create_label_and_spinner(self, container, label_text, spinner_attr, values):
        label = Label(
            text=label_text,
            size_hint=(1, None),
            height=30,
            halign="left",
            valign="middle",
        )
        label.bind(
            size=lambda *x: setattr(label, "text_size", (label.width, label.height))
        )

        spinner = Spinner(
            text=values[0] if values else "",
            values=values,
            size_hint=(1, 1),
            halign="left",
            valign="middle",
        )
        container.add_widget(label)
        container.add_widget(spinner)
        setattr(self, spinner_attr, spinner)

    def _update_debug(self, instance, value):
        """Обновляет отладочную визуализацию."""
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(0, 0, 0, 0.3)  # Черный с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)
