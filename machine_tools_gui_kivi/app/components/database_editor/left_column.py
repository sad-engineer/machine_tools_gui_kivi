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
from machine_tools import Automation, SoftwareControl, Specialization, WeightClass

from machine_tools_gui_kivi.app.components.dropdown_list import DropdownList
from machine_tools_gui_kivi.app.components.labeled_input import LabeledInput
from machine_tools_gui_kivi.app.components.labeled_spinner import LabeledSpinner
from machine_tools_gui_kivi.app.components.searchbar import SearchBar
from machine_tools_gui_kivi.src.descriptions import get_accuracy_fields_descriptions as get_accuracy_fields
from machine_tools_gui_kivi.src.descriptions import get_group_fields_descriptions as get_group_fields
from machine_tools_gui_kivi.src.descriptions import get_specialization_fields_descriptions as get_specialization_fields
from machine_tools_gui_kivi.src.descriptions import get_type_fields_descriptions as get_type_fields


def get_custom_spinner(label_text: str, values: list, debug_mode: bool = False) -> LabeledSpinner:
    """Настраивает спиннер."""
    spinner = LabeledSpinner(
        label_text=label_text,
        values=values,
        height=65,
        debug_mode=debug_mode,
    )
    spinner.size_hint = (1, None)
    spinner.pos_hint = {"top": 1}
    return spinner


def get_custom_input(label_text: str, units: str = None, debug_mode: bool = False) -> LabeledInput:
    """Настраивает поле ввода."""
    input = LabeledInput(
        label_text=label_text,
        units=units,
        debug_mode=debug_mode,
    )
    input.size_hint = (1, None)
    input.pos_hint = {"top": 1}
    return input


class LeftColumn(BoxLayout):
    """
    Класс левой колонки редактора базы данных.
    """

    def __init__(self, debug_mode=False, **kwargs):
        super().__init__(orientation="vertical", size_hint=(1, 1), spacing=5, padding=[5, 5, 5, 5], **kwargs)
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
        fields_container = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=[0, 0, 10, 0])
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
            button_text="Загрузить\nиз БД",
            input_ratio=0.8,
            height=35,
            debug_mode=self.debug_mode,
        )
        self.search_bar.size_hint = (1, None)
        self.search_bar.pos_hint = {"top": 1}
        self.add_widget(self.search_bar)

        # Группа станка
        self.group_spinner = get_custom_spinner("Группа станка:", get_group_fields(), self.debug_mode)
        container.add_widget(self.group_spinner)

        # Тип станка
        self.type_spinner = get_custom_spinner(
            "Тип станка:",
            get_type_fields(self.group_spinner.spinner.text[:1]),
            self.debug_mode,
        )
        container.add_widget(self.type_spinner)

        # Расшифровка типа станка
        self.machine_type_input = get_custom_input("Тип станка (доп.):", debug_mode=self.debug_mode)
        container.add_widget(self.machine_type_input)

        # Автоматизация, Признак ЧПУ  в одну строку
        horizontal_container = BoxLayout(orientation="horizontal", size_hint=(1, None), height=65, spacing=5)
        # Автоматизация
        self.automation_spinner = get_custom_spinner("Автоматизация:", Automation.get_values(), self.debug_mode)
        horizontal_container.add_widget(self.automation_spinner)
        # Признак ЧПУ
        self.software_control_spinner = get_custom_spinner(
            "Наличие ЧПУ:", SoftwareControl.get_values(), self.debug_mode
        )
        horizontal_container.add_widget(self.software_control_spinner)
        container.add_widget(horizontal_container)

        # Мощность, КПД  в одну строку
        horizontal_container = BoxLayout(orientation="horizontal", size_hint=(1, None), height=65, spacing=5)
        # Мощность
        self.power_input = get_custom_input("Мощность:", "кВт", debug_mode=self.debug_mode)
        horizontal_container.add_widget(self.power_input)
        # КПД
        self.efficiency_input = get_custom_input("КПД:", "%", debug_mode=self.debug_mode)
        horizontal_container.add_widget(self.efficiency_input)
        container.add_widget(horizontal_container)

        # Точность станка
        self.accuracy_spinner = get_custom_spinner("Точность станка:", get_accuracy_fields(), self.debug_mode)
        container.add_widget(self.accuracy_spinner)

        # Специализация
        self.specialization_spinner = get_custom_spinner("Специализация:", Specialization.get_values(), self.debug_mode)
        container.add_widget(self.specialization_spinner)

        # Масса и Класс станка по массе в одну строку
        horizontal_container_2 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=65, spacing=5)
        self.mass_input = get_custom_input("Масса:", "кг", debug_mode=self.debug_mode)
        horizontal_container_2.add_widget(self.mass_input)
        self.weight_class_spinner = get_custom_spinner(
            "Класс станка по массе:", WeightClass.get_values(), self.debug_mode
        )
        horizontal_container_2.add_widget(self.weight_class_spinner)
        container.add_widget(horizontal_container_2)

        # Размеры
        label_1 = Label(
            text="Размеры:",
            size_hint=(1, None),
            height=30,
            halign="left",
            valign="middle",
        )
        label_1.bind(size=lambda *x: setattr(label_1, "text_size", (label_1.width, label_1.height)))
        container.add_widget(label_1)
        horizontal_container_2 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=65, spacing=5)
        self.length_input = get_custom_input("Длина:", "мм", debug_mode=self.debug_mode)
        horizontal_container_2.add_widget(self.length_input)
        self.width_input = get_custom_input("Ширина:", "мм", debug_mode=self.debug_mode)
        horizontal_container_2.add_widget(self.width_input)
        self.height_input = get_custom_input("Высота:", "мм", debug_mode=self.debug_mode)
        horizontal_container_2.add_widget(self.height_input)
        container.add_widget(horizontal_container_2)

        # Размеры рабочей зоны
        self.overall_diameter_input = get_custom_input("Размеры рабочей зоны:", "мм", debug_mode=self.debug_mode)
        container.add_widget(self.overall_diameter_input)

        # Город производства
        self.production_city_input = get_custom_input("Город производства:", debug_mode=self.debug_mode)
        container.add_widget(self.production_city_input)

        # Организация-производитель
        self.organization_input = get_custom_input("Организация-производитель:", debug_mode=self.debug_mode)
        container.add_widget(self.organization_input)

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
