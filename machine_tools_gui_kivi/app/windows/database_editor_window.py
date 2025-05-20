#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна ввода данных, наследующий от шаблонного окна.
"""
import copy
from typing import Optional

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivymd.app import MDApp
from machine_tools import MachineInfo
from machine_tools import info_by_name as get_info_by_name

from machine_tools_gui_kivi.app.components.database_editor import \
    TemplateDatabaseEditor
from machine_tools_gui_kivi.app.components.dropdown_list import DropdownList
from machine_tools_gui_kivi.app.components.template_window import \
    TemplateWindow
from machine_tools_gui_kivi.src.machine_finder import filter_names


class DatabaseEditorWindow(Screen):
    """Окно ввода данных, обертка для TemplateWindow."""

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.name = "input_window"
        self.model: Optional[str] = None
        self.old_data: Optional[MachineInfo] = None  # Старые данные станка
        self.new_data: Optional[MachineInfo] = None  # Новые данные станка

        # Создаем шаблонное окно
        self.template_window = TemplateWindow(
            screen_manager=screen_manager, debug_mode=debug_mode
        )

        # Добавляем контент
        self.content_widget = TemplateDatabaseEditor(
            screen_manager=screen_manager, debug_mode=debug_mode
        )
        self.template_window.content.add_widget(self.content_widget)
        self.add_widget(self.template_window)
        self.add_widget(self.content_widget.left_col.search_bar_dropdown)

        self.content_widget.left_col.search_bar.button.bind(
            on_release=self.on_search_machine
        )
        self.content_widget.left_col.search_bar.input.bind(
            text=self.on_search_input_changed
        )
        self.content_widget.left_col.search_bar_dropdown.on_select = (
            self.on_dropdown_select
        )

    def on_search_machine(self, instance):
        """Обрабатывает событие нажатия на кнопку поиска."""
        # Получаем текст из поля ввода
        self.model = self.content_widget.left_col.search_bar.input.text
        print(f"Выбран станок модели: {self.model}")
        self.old_data = get_info_by_name(self.model)
        self.new_data = copy.deepcopy(self.old_data)
        self.set_widget_data(self.old_data)

    def set_widget_data(self, data: MachineInfo):
        """Устанавливает данные в виджеты."""
        if isinstance(data, MachineInfo):
            self.content_widget.left_col.group_input.text = str(data.group)
            self.content_widget.left_col.type_input.text = str(data.type)
            self.content_widget.left_col.machine_type_input.text = str(
                data.machine_type
            )
            self.content_widget.left_col.power_input.text = str(data.power)
            self.content_widget.left_col.efficiency_input.text = str(data.efficiency)
            self.content_widget.left_col.accuracy_input.text = str(data.accuracy.value)
            self.content_widget.left_col.automation_input.text = str(
                data.automation.value
            )
            self.content_widget.left_col.specialization_input.text = str(
                data.specialization.value
            )
            self.content_widget.left_col.mass_input.text = str(data.weight)
            self.content_widget.left_col.mass_class_input.text = str(
                data.weight_class.value
            )
            self.content_widget.left_col.production_city_input.text = str(
                data.location.city
            )
            self.content_widget.left_col.organization_input.text = str(
                data.location.manufacturer
            )
            print(f"Данные станка: {data}")

    def clear_widgets(self):
        """Очищает все виджеты."""
        self.content_widget.left_col.group_input.text = ""
        self.content_widget.left_col.type_input.text = ""
        self.content_widget.left_col.machine_type_input.text = ""
        self.content_widget.left_col.power_input.text = ""
        self.content_widget.left_col.efficiency_input.text = ""
        self.content_widget.left_col.accuracy_input.text = ""
        self.content_widget.left_col.automation_input.text = ""
        self.content_widget.left_col.specialization_input.text = ""
        self.content_widget.left_col.mass_input.text = ""
        self.content_widget.left_col.mass_class_input.text = ""
        self.content_widget.left_col.production_city_input.text = ""
        self.content_widget.left_col.organization_input.text = ""

    def on_search_input_changed(self, instance, value: str):
        """Обрабатывает событие изменения текста в поле ввода."""
        print(value)
        if value != self.model:
            self.clear_widgets()
        value = value.upper()
        searchbar = self.content_widget.left_col.search_bar
        dropdown = self.content_widget.left_col.search_bar_dropdown
        if len(value) > 0:
            filtered = filter_names(value)
            dropdown.update_items(filtered)
            # Показываем список только если есть варианты и поле в фокусе
            if filtered and searchbar.input.focus:
                dropdown.opacity = 1
                # Позиционируем dropdown под searchbar
                dropdown.width = searchbar.input.width
                dropdown.x = searchbar.input.to_window(
                    searchbar.input.x, searchbar.input.y
                )[0]
                dropdown.y = (
                    searchbar.input.to_window(searchbar.input.x, searchbar.input.y)[1]
                    - dropdown.height
                )
            else:
                dropdown.opacity = 0
        else:
            dropdown.opacity = 0

    def on_dropdown_select(self, value):
        """Обрабатывает событие выбора станка из списка."""
        self.content_widget.left_col.search_bar.input.text = value
        self.content_widget.left_col.search_bar_dropdown.opacity = 0


if __name__ == "__main__":

    class TestApp(MDApp):
        """Тестовое приложение для отладки окна."""

        def build(self):
            """Создает и возвращает главное окно приложения."""
            Window.minimum_width = 910
            Window.minimum_height = 600
            window = DatabaseEditorWindow(debug_mode=True)
            return window

    TestApp().run()


# # Добавляем шаблон поиска
#         self.search_bar = SearchBar(
#             input_hint="Введите название станка",
#             button_text="Поиск",
#             input_ratio=0.8,
#             height=35,
#             debug_mode=self.debug_mode,
#         )
#         self.search_bar.size_hint = (1, None)
#         self.search_bar.pos_hint = {'top': 1}
#
#         #Лейбл с надписью "Группа станка"
#         group_label = Label(
#             text="Группа станка",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода группы станка
#         self.group_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Тип станка"
#         type_label = Label(
#             text="Тип станка",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода типа станка
#         self.type_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         self.machine_type_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Мощность"
#         power_label = Label(
#             text="Мощность",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода мощности
#         self.power_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "КПД"
#         efficiency_label = Label(
#             text="КПД",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода КПД
#         self.efficiency_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Точность"
#         accuracy_label = Label(
#             text="Точность",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода точности
#         self.accuracy_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Автоматизация"
#         automation_label = Label(
#             text="Автоматизация",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода автоматизации
#         self.automation_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Специализация    "
#         specialization_label = Label(
#             text="Специализация",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода специализации
#         self.specialization_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Масса"
#         mass_label = Label(
#             text="Масса",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода массы
#         self.mass_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Класс станка по массе    "
#         mass_class_label = Label(
#             text="Класс станка по массе",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода класса станка по массе
#         self.mass_class_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Город производства"
#         production_city_label = Label(
#             text="Город производства",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода города производства
#         self.production_city_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         #Лейбл с надписью "Организация-производитель"
#         organization_label = Label(
#             text="Организация-производитель",
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#         #Поле для ввода организации-производителя
#         self.organization_input = TextInput(
#             size_hint=(1, None),
#             height=30,
#             halign="left"
#         )
#
#         # Добавляем все виджеты в left_col
#         left_col.add_widget(self.search_bar)
#         left_col.add_widget(group_label)
#         left_col.add_widget(self.group_input)
#         left_col.add_widget(type_label)
#         left_col.add_widget(self.type_input)
#         left_col.add_widget(self.machine_type_input)
#         left_col.add_widget(power_label)
#         left_col.add_widget(self.power_input)
#         left_col.add_widget(efficiency_label)
#         left_col.add_widget(self.efficiency_input)
#         left_col.add_widget(accuracy_label)
#         left_col.add_widget(self.accuracy_input)
#         left_col.add_widget(automation_label)
#         left_col.add_widget(self.automation_input)
#         left_col.add_widget(specialization_label)
#         left_col.add_widget(self.specialization_input)
#         left_col.add_widget(mass_label)
#         left_col.add_widget(self.mass_input)
#         left_col.add_widget(mass_class_label)
#         left_col.add_widget(self.mass_class_input)
#         left_col.add_widget(production_city_label)
#         left_col.add_widget(self.production_city_input)
#         left_col.add_widget(organization_label)
#         left_col.add_widget(self.organization_input)

# Добавляем выпадающий список
#         self.search_bar_dropdown = DropdownList(
#             size_hint=(0.4, None),
#             height=200,
#             item_height=30,
#             item_spacing=2,
#             bar_width=10,
#             item_cols=2,
#             opacity=0
#         )
