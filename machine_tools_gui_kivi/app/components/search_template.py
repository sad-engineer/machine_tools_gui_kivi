#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит шаблонный класс для поиска с выпадающим списком.
"""
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from machine_tools_gui_kivi.src.machine_finder import filter_names


class DropdownList(ScrollView):
    """Выпадающий список с прокруткой."""
    
    def __init__(self, on_select=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, None)
        self.height = 0
        self.opacity = 0
        self.on_select = on_select  # callback для выбора
        
        # Создаем сетку для элементов списка
        self.grid = GridLayout(cols=1, spacing=2, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.add_widget(self.grid)
    
    def update_items(self, items):
        """Обновляет элементы списка."""
        self.grid.clear_widgets()
        if items:
            for item in items:
                btn = Button(
                    text=item,
                    size_hint_y=None,
                    height=40,
                    background_color=(1, 1, 1, 1),
                    color=(0, 0, 0, 1)
                )
                btn.bind(on_release=lambda btn, item=item: self._on_item_select(item))
                self.grid.add_widget(btn)
            self.height = min(200, len(items) * 42)  # 40 + 2 (spacing)
            self.opacity = 1
        else:
            self.height = 0
            self.opacity = 0

    def _on_item_select(self, value):
        if self.on_select:
            self.on_select(value)


class SearchTemplate(BoxLayout):
    """
    Шаблонный класс для поиска с выпадающим списком.

    Attributes:
        search_input: Поле ввода для поиска
        dropdown_list: Выпадающий список с результатами
        search_button: Кнопка поиска
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self._update_list_trigger = Clock.create_trigger(self._update_list_values, 0.1)
        self._init_search_ui()

    def _init_search_ui(self):
        """Инициализирует пользовательский интерфейс поиска."""
        # Создаем контейнер для поля поиска
        search_box = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=50,
            padding=[0, 0, 0, 10],
            spacing=5,
            pos_hint={'top': 1}
        )

        # Создаем поле ввода
        self.search_input = TextInput(
            hint_text="Введите подстроку для поиска",
            multiline=False,
            halign='center',
            size_hint=(0.8, 1)
        )
        self.search_input.bind(text=self._on_search_text_changed)
        # self.search_input.bind(focus=self._on_input_focus)

        # Создаем выпадающий список
        self.dropdown_list = DropdownList(on_select=self._on_dropdown_select)

        # Создаем кнопку поиска
        self.search_button = Button(
            text="Поиск",
            size_hint=(0.2, 1),
            on_release=self._on_search
        )

        # Добавляем виджеты в контейнер
        search_box.add_widget(self.search_input)
        search_box.add_widget(self.search_button)

        # Добавляем контейнеры в основной контейнер
        self.add_widget(search_box)
        self.add_widget(self.dropdown_list)
        self.add_widget(Widget(size_hint_y=1))

    def _on_input_focus(self, instance, value):
        if not value:
            self.dropdown_list.update_items([])  # Скрыть список при потере фокуса

    def _on_search_text_changed(self, instance, value):
        if value and self.search_input.focus:
            self._update_list_trigger()
        else:
            self.dropdown_list.update_items([])

    def _update_list_values(self, dt):
        if self.search_input.focus:
            search_text = self.search_input.text
            if len(search_text) > 1:
                if search_text:
                    filtered_names = filter_names(search_text)
                    self.dropdown_list.update_items(filtered_names)
                else:
                    self.dropdown_list.update_items([])

    def _on_search(self, instance):
        """Обработчик нажатия кнопки поиска."""
        search_text = self.search_input.text
        if search_text:
            # TODO: Реализовать поиск в БД
            print(f"Поиск станка: {search_text}")

    def _on_dropdown_select(self, value):
        self.search_input.text = value
        self.search_input.focus = True  # Вернуть фокус, чтобы событие не блокировалось
        self.dropdown_list.update_items([])  # Скрыть список


if __name__ == "__main__":
    from kivy.app import App

    class TestApp(App):
        def build(self):
            return SearchTemplate()

    TestApp().run() 