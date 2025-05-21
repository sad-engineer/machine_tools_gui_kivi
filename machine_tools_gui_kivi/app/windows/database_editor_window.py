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
from kivymd.app import MDApp
from machine_tools import Automation, Dimensions, Location, MachineInfo, Specialization, WeightClass
from machine_tools import info_by_name as get_info_by_name

from machine_tools_gui_kivi.app.components.database_editor import TemplateDatabaseEditor
from machine_tools_gui_kivi.app.components.template_window import TemplateWindow
from machine_tools_gui_kivi.src.descriptions import ACCURACY_DESCRIPTIONS, get_accuracy_by_description
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
        self.template_window = TemplateWindow(screen_manager=screen_manager, debug_mode=debug_mode)

        # Добавляем контент
        self.content_widget = TemplateDatabaseEditor(
            screen_manager=screen_manager,
            debug_mode=debug_mode,
            on_technical_requirements_change=self._on_technical_requirements_change,
            on_technical_requirement_name_change=self._on_technical_requirement_name_change,
        )
        self.template_window.content.add_widget(self.content_widget)
        self.add_widget(self.template_window)
        self.add_widget(self.content_widget.left_col.search_bar_dropdown)

        self.content_widget.left_col.search_bar.button.bind(on_release=self.on_search_machine)
        self.content_widget.left_col.search_bar.input.bind(text=self.on_search_input_changed)
        self.content_widget.left_col.search_bar_dropdown.on_select = self.on_dropdown_select

        # Переопределяем имя и функцию button1
        self.template_window.button1.text = "Сохранить"
        self.template_window.button1.bind(on_release=self.save_data)

    def _on_technical_requirements_change(self, property_name, value):
        """
        Обработчик изменения технических требований.

        Args:
            property_name: Название свойства
            value: Новое значение
        """
        if self.old_data and self.old_data.technical_requirements is not None:
            if self.old_data.technical_requirements.get(property_name) != value:
                self.old_data.technical_requirements[property_name] = value
                print(f"Обновлено техническое требование: {property_name} = {value}")

    def _on_technical_requirement_name_change(self, old_name, new_name):
        """
        Обработчик изменения названия технического требования.

        Args:
            old_name: Старое название требования
            new_name: Новое название требования
        """
        if self.old_data and self.old_data.technical_requirements is not None:
            if old_name in self.old_data.technical_requirements:
                # Создаем новый словарь с сохранением порядка
                new_requirements = {}
                for key, value in self.old_data.technical_requirements.items():
                    if key == old_name:
                        new_requirements[new_name] = value
                    else:
                        new_requirements[key] = value
                self.old_data.technical_requirements = new_requirements
                print(f"Переименовано техническое требование: {old_name} -> {new_name}")

    def on_search_machine(self, instance):
        """Обрабатывает событие нажатия на кнопку поиска."""
        # Получаем текст из поля ввода
        self.model = self.content_widget.left_col.search_bar.input.text
        print(f"Выбран станок модели: {self.model}")
        self.old_data = get_info_by_name(self.model)
        self.new_data = copy.deepcopy(self.old_data)
        self.set_widget_data(self.old_data)

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
                dropdown.x = searchbar.input.to_window(searchbar.input.x, searchbar.input.y)[0]
                dropdown.y = searchbar.input.to_window(searchbar.input.x, searchbar.input.y)[1] - dropdown.height
            else:
                dropdown.opacity = 0
        else:
            dropdown.opacity = 0

    def on_dropdown_select(self, value):
        """Обрабатывает событие выбора станка из списка."""
        self.content_widget.left_col.search_bar.input.text = value
        self.content_widget.left_col.search_bar_dropdown.opacity = 0

    def clear_widgets(self):
        """Очищает все виджеты."""
        self.content_widget.left_col.group_spinner.set_value("")
        self.content_widget.left_col.type_spinner.set_value("")
        self.content_widget.left_col.machine_type_input.set_value("")
        self.content_widget.left_col.power_input.set_value("")
        self.content_widget.left_col.efficiency_input.set_value("")
        self.content_widget.left_col.accuracy_spinner.set_value("")
        self.content_widget.left_col.automation_spinner.set_value("")
        self.content_widget.left_col.specialization_spinner.set_value("")
        self.content_widget.left_col.mass_input.set_value("")
        self.content_widget.left_col.weight_class_spinner.set_value("")
        self.content_widget.left_col.production_city_input.set_value("")
        self.content_widget.left_col.organization_input.set_value("")
        self.content_widget.left_col.length_input.set_value("")
        self.content_widget.left_col.width_input.set_value("")
        self.content_widget.left_col.height_input.set_value("")
        self.content_widget.left_col.overall_diameter_input.set_value("")

    def set_widget_data(self, data: MachineInfo):
        """Устанавливает данные в виджеты."""
        if isinstance(data, MachineInfo):
            self.content_widget.left_col.group_spinner.set_value(str(int(data.group)))
            self.content_widget.left_col.type_spinner.set_value(str(int(data.type)))
            self.content_widget.left_col.machine_type_input.set_value(str(data.machine_type))
            self.content_widget.left_col.power_input.set_value(str(data.power))
            self.content_widget.left_col.efficiency_input.set_value(str(data.efficiency))
            self.content_widget.left_col.accuracy_spinner.set_value(ACCURACY_DESCRIPTIONS[data.accuracy.value])
            self.content_widget.left_col.automation_spinner.set_value(data.automation.value)
            self.content_widget.left_col.specialization_spinner.set_value(data.specialization.value)
            self.content_widget.left_col.mass_input.set_value(str(data.weight))
            self.content_widget.left_col.weight_class_spinner.set_value(data.weight_class.value)
            self.content_widget.left_col.production_city_input.set_value(data.location.city)
            self.content_widget.left_col.organization_input.set_value(data.location.manufacturer)
            self.content_widget.left_col.length_input.set_value(str(data.dimensions.length))
            self.content_widget.left_col.width_input.set_value(str(data.dimensions.width))
            self.content_widget.left_col.height_input.set_value(str(data.dimensions.height))
            self.content_widget.left_col.overall_diameter_input.set_value(str(data.dimensions.overall_diameter))
            self.content_widget.right_col.update_properties(data.technical_requirements)
            print(f"Данные станка: {data}")

    def get_data_from_widgets(self):
        """Получает данные из виджетов."""
        machine_info = MachineInfo(
            name=self.content_widget.left_col.search_bar.input.text,
            group=self.content_widget.left_col.group_spinner.get_value().split(" ")[0],
            type=self.content_widget.left_col.type_spinner.get_value().split(" ")[0],
            power=self.content_widget.left_col.power_input.get_value(),
            efficiency=self.content_widget.left_col.efficiency_input.get_value(),
            accuracy=get_accuracy_by_description(self.content_widget.left_col.accuracy_spinner.get_value()),
            automation=Automation(self.content_widget.left_col.automation_spinner.get_value()),
            specialization=Specialization(self.content_widget.left_col.specialization_spinner.get_value()),
            weight=self.content_widget.left_col.mass_input.get_value(),
            weight_class=WeightClass(self.content_widget.left_col.weight_class_spinner.get_value()),
            dimensions=Dimensions(
                length=self.content_widget.left_col.length_input.get_value(),
                width=self.content_widget.left_col.width_input.get_value(),
                height=self.content_widget.left_col.height_input.get_value(),
                overall_diameter=self.content_widget.left_col.overall_diameter_input.get_value(),
            ),
            location=Location(
                city=self.content_widget.left_col.production_city_input.get_value(),
                manufacturer=self.content_widget.left_col.organization_input.get_value(),
            ),
            machine_type=self.content_widget.left_col.machine_type_input.get_value(),
        )

        return machine_info

    def save_data(self, instance):
        """Сохраняет данные в базу данных."""
        data = self.get_data_from_widgets()
        print(f"Данные из виджетов: {data}")
        print(f"Данные старого станка: {self.old_data}")


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
