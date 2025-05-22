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
from machine_tools import update as machine_tool_update

from machine_tools_gui_kivi.app.components.database_editor import TemplateDatabaseEditor
from machine_tools_gui_kivi.app.components.template_window import TemplateWindow
from machine_tools_gui_kivi.src.descriptions import (
    ACCURACY_DESCRIPTIONS,
    get_accuracy_by_description,
    get_type_fields_descriptions,
)
from machine_tools_gui_kivi.src.machine_finder import filter_names


class DatabaseEditorWindow(Screen):
    """Окно ввода данных, обертка для TemplateWindow."""

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.name = "input_window"
        self.model: Optional[str] = None
        self.data_from_database: Optional[MachineInfo] = None  # Старые данные станка (данные из базы данных)
        self.corrected_data: Optional[MachineInfo] = None  # Новые данные станка (данные для изменений)

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

        # Переопределяем имя и функцию кнопок
        self.template_window.button1.text = "Сохранить"
        self.template_window.button1.bind(on_release=self.on_release_save_button)

        self.template_window.button2.text = "Отмена"
        self.template_window.button2.bind(on_release=self.cancel)

        self.clear_widgets()

    def _on_technical_requirements_change(self, property_name, value):
        """
        Обработчик изменения технических требований.

        Args:
            property_name: Название свойства
            value: Новое значение
        """
        if self.corrected_data and self.corrected_data.technical_requirements is not None:
            if self.corrected_data.technical_requirements.get(property_name) != value:
                self.corrected_data.technical_requirements[property_name] = value
                print(f"Обновлено техническое требование: {property_name} = {value}")

    def _on_technical_requirement_name_change(self, old_name, new_name):
        """
        Обработчик изменения названия технического требования.

        Args:
            old_name: Старое название требования
            new_name: Новое название требования
        """
        if self.corrected_data and self.corrected_data.technical_requirements is not None:
            if old_name in self.corrected_data.technical_requirements:
                # Создаем новый словарь с сохранением порядка
                new_requirements = {}
                for key, value in self.corrected_data.technical_requirements.items():
                    if key == old_name:
                        new_requirements[new_name] = value
                    else:
                        new_requirements[key] = value
                self.corrected_data.technical_requirements = new_requirements
                print(f"Переименовано техническое требование: {old_name} -> {new_name}")

    def on_search_machine(self, instance):
        """Обрабатывает событие нажатия на кнопку поиска."""
        # Получаем текст из поля ввода
        text = self.content_widget.left_col.search_bar.input.text
        if text:
            # Удаляем все пробелы и преобразуем в верхний регистр
            self.model = text.upper().replace(" ", "")
            # Получаем данные из базы данных
            self.get_info()
        else:
            print("Не введено название станка")

    def get_info(self):
        """Получаем данные из базы данных"""
        info = get_info_by_name(self.model)
        if info:
            self.data_from_database = info
            self.corrected_data = copy.deepcopy(info)
            self.set_widget_data(info)
            print(f"Выбран станок модели: {self.model}")
        else:
            print(f"Станок модели {self.model} не найден в базе данных.")

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
        self.content_widget.left_col.group_spinner.clear_value()
        self.content_widget.left_col.type_spinner.clear_value()
        self.content_widget.left_col.machine_type_input.clear_value()
        self.content_widget.left_col.power_input.clear_value()
        self.content_widget.left_col.efficiency_input.clear_value()
        self.content_widget.left_col.accuracy_spinner.clear_value()
        self.content_widget.left_col.automation_spinner.clear_value()
        self.content_widget.left_col.specialization_spinner.clear_value()
        self.content_widget.left_col.mass_input.clear_value()
        self.content_widget.left_col.weight_class_spinner.clear_value()
        self.content_widget.left_col.production_city_input.clear_value()
        self.content_widget.left_col.organization_input.clear_value()
        self.content_widget.left_col.length_input.clear_value()
        self.content_widget.left_col.width_input.clear_value()
        self.content_widget.left_col.height_input.clear_value()
        self.content_widget.left_col.overall_diameter_input.clear_value()

    def set_widget_data(self, data: MachineInfo):
        """Устанавливает данные в виджеты."""
        if isinstance(data, MachineInfo):
            #  получаем список типов станков для выпадающего списка по группе выбранного станка
            str_group = str(int(data.group))
            type_fields = get_type_fields_descriptions(str_group)
            #  устанавливаем список типов станков для выпадающего списка типа станка
            self.content_widget.left_col.type_spinner.spinner.values = type_fields
            #  устанавливаем значения для полей по данным из базы данных
            self.content_widget.left_col.group_spinner.set_value(str_group)
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

    def get_data_from_widgets(self):
        """
        Получает данные из виджетов и сохраняет их в объект MachineInfo.
        ВАЖНО! Объект MachineInfo - объект pydantic.BaseModel, поэтому данные обновляются, но не валидируются
        """
        self.corrected_data.name = self.content_widget.left_col.search_bar.input.text
        self.corrected_data.group = int(self.content_widget.left_col.group_spinner.get_value().split(" ")[0])
        self.corrected_data.type = int(self.content_widget.left_col.type_spinner.get_value().split(" ")[0])
        self.corrected_data.power = float(self.content_widget.left_col.power_input.get_value())
        self.corrected_data.efficiency = float(self.content_widget.left_col.efficiency_input.get_value())
        self.corrected_data.accuracy = get_accuracy_by_description(
            self.content_widget.left_col.accuracy_spinner.get_value()
        )
        self.corrected_data.automation = Automation(self.content_widget.left_col.automation_spinner.get_value())
        self.corrected_data.specialization = Specialization(
            self.content_widget.left_col.specialization_spinner.get_value(),
        )
        self.corrected_data.weight = float(self.content_widget.left_col.mass_input.get_value())
        self.corrected_data.weight_class = WeightClass(self.content_widget.left_col.weight_class_spinner.get_value())
        self.corrected_data.dimensions = Dimensions(
            length=int(float(self.content_widget.left_col.length_input.get_value())),
            width=int(float(self.content_widget.left_col.width_input.get_value())),
            height=int(float(self.content_widget.left_col.height_input.get_value())),
            overall_diameter=self.content_widget.left_col.overall_diameter_input.get_value(),
        )
        self.corrected_data.location = Location(
            city=self.content_widget.left_col.production_city_input.get_value(),
            manufacturer=self.content_widget.left_col.organization_input.get_value(),
        )
        self.corrected_data.machine_type = self.content_widget.left_col.machine_type_input.get_value()

    def on_release_save_button(self, instance):
        """Обрабатывает событие нажатия на кнопку сохранения."""
        if not self.corrected_data:
            print("Данные не найдены")
            return
        if not isinstance(self.corrected_data, MachineInfo):
            print("Данные не являются объектом MachineInfo")
            return
        self.get_data_from_widgets()
        if self.corrected_data != self.data_from_database:
            self.save_data(self.corrected_data)
        else:
            print("Измененных данных не найдено.")

    def save_data(self, data: MachineInfo):
        """Сохраняет данные в базу данных."""
        print(f"Данные из базы данных: {self.data_from_database}")
        print(f"Скорректированные данные: {self.corrected_data}")
        print(f"Обновляем данные в БД...")
        result = machine_tool_update(data)
        if result:
            print("Данные успешно обновлены в базе данных.")
        else:
            print("Ошибка при обновлении данных в базе данных.")
        self.get_info()

    @staticmethod
    def cancel(instance):
        """
        Отменяет ввод данных и завершает работу приложения.

        Args:
            instance: Экземпляр кнопки
        """
        # Завершаем работу приложения
        MDApp.get_running_app().stop()


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
