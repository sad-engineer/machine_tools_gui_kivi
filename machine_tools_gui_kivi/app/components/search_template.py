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

from machine_tools_gui_kivi.src.machine_finder import filter_names


class SearchTemplate(BoxLayout):
    """
    Шаблонный класс для поиска с выпадающим списком.

    Attributes:
        search_input: Поле ввода для поиска
        search_spinner: Выпадающий список с результатами
        search_button: Кнопка поиска
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self._update_spinner_trigger = Clock.create_trigger(self._update_spinner_values, 0.5)
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
        # Привязываем обработчик после создания виджета
        self.search_input.bind(text=self._on_search_text_changed)

        # Создаем выпадающий список
        self.search_spinner = Spinner(
            text='Выберите станок',
            values=[],
            size_hint=(0.8, 1),
            pos_hint={'top': 1},
            opacity=0,
            on_text=self._on_spinner_select
        )

        # Создаем кнопку поиска
        self.search_button = Button(
            text="Поиск",
            size_hint=(0.2, 1),
            on_release=self._on_search
        )

        # Добавляем виджеты в контейнер
        search_box.add_widget(self.search_input)
        search_box.add_widget(self.search_button)

        # Создаем контейнер для выпадающего списка
        self.spinner_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=0,
            pos_hint={'top': 1}
        )
        self.spinner_container.add_widget(self.search_spinner)

        # Добавляем контейнеры в основной контейнер
        self.add_widget(search_box)
        self.add_widget(self.spinner_container)
        self.add_widget(Widget(size_hint_y=1))

    def _on_search_text_changed(self, instance, value):
        """Обработчик изменения текста в поле поиска."""
        print(f"Введенный текст: {value}")
        if value:
            self._update_spinner_trigger()
        else:
            self.search_spinner.values = []
            self.search_spinner.text = 'Выберите станок'
            self.search_spinner.opacity = 0
            self.spinner_container.height = 0
            # Закрываем выпадающий список при пустом поле
            self.search_spinner.is_open = False

    def _update_spinner_values(self, dt):
        """Обновляет значения в выпадающем списке."""
        search_text = self.search_input.text
        if search_text:
            filtered_names = filter_names(search_text)
            if filtered_names:
                self.search_spinner.values = filtered_names
                self.search_spinner.text = filtered_names[0]  # Устанавливаем первый элемент как текущий
                self.search_spinner.opacity = 1
                self.spinner_container.height = 35
                # Открываем выпадающий список
                self.search_spinner.is_open = True
            else:
                self.search_spinner.values = []
                self.search_spinner.text = 'Станки не найдены'
                self.search_spinner.opacity = 1
                self.spinner_container.height = 35
                # Закрываем выпадающий список, если нет результатов
                self.search_spinner.is_open = False

    def _on_spinner_select(self, instance, value):
        """Обработчик выбора значения из выпадающего списка."""
        if value != 'Выберите станок' and value != 'Станки не найдены':
            self.search_input.text = value

    def _on_search(self, instance):
        """Обработчик нажатия кнопки поиска."""
        search_text = self.search_input.text
        if search_text and search_text != 'Выберите станок' and search_text != 'Станки не найдены':
            # TODO: Реализовать поиск в БД
            print(f"Поиск станка: {search_text}")


if __name__ == "__main__":
    from kivy.app import App

    class TestApp(App):
        def build(self):
            return SearchTemplate()

    TestApp().run() 