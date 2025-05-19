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
from machine_tools_gui_kivi.src.machine_finder import filter_names
from machine_tools_gui_kivi.app.components.dropdown_list import DropdownList
from machine_tools_gui_kivi.app.components.database_editor_content import TemplateDatabaseEditorContent
from machine_tools import info_by_name as get_info_by_name, MachineInfo


class DatabaseEditorWindow(Screen):
    """Окно ввода данных, обертка для TemplateWindow."""

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.name = "input_window"
        # Создаем шаблонное окно
        self.template_window = TemplateWindow(
            screen_manager=screen_manager, debug_mode=debug_mode
        )

        # Добавляем контент
        self.content_widget = TemplateDatabaseEditorContent(
            screen_manager=screen_manager,
            debug_mode=debug_mode
        )
        self.template_window.content.add_widget(self.content_widget)
        self.add_widget(self.template_window)
        self.add_widget(self.content_widget.search_bar_dropdown)

        self.content_widget.search_bar.button.bind(on_release=self.on_search_machine)
        self.content_widget.search_bar.input.bind(text=self.on_search_input_changed)
        self.content_widget.search_bar_dropdown.on_select = self.on_dropdown_select

    def on_search_machine(self, instance):
        """Обрабатывает событие нажатия на кнопку поиска."""
        # Получаем текст из поля ввода
        model = self.content_widget.search_bar.input.text
        print(f"Выбран станок модели: {model}")
        self.set_widget_data(model)

    def set_widget_data(self, model: str):
        data = get_info_by_name(model)
        """Устанавливает данные в виджеты."""
        if isinstance(data, MachineInfo):
            print(f"Данные станка: {data}")

    def on_search_input_changed(self, instance, value:str):
        """Обрабатывает событие изменения текста в поле ввода."""
        value = value.upper()
        searchbar = self.content_widget.search_bar
        dropdown = self.content_widget.search_bar_dropdown
        if len(value) > 0:
            filtered = filter_names(value)
            dropdown.update_items(filtered)
            # Показываем список только если есть варианты и поле в фокусе
            if filtered and self.content_widget.search_bar.input.focus:
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
        self.content_widget.search_bar.input.text = value
        self.content_widget.search_bar_dropdown.opacity = 0



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
