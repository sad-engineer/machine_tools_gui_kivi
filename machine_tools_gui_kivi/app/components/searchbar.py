#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class SearchBar(BoxLayout):
    """
    Поиск с выпадающим списком

    Args:
        input_hint (str): Подсказка для поля ввода
        button_text (str): Текст на кнопке
        input_ratio (float): Отношение ширины поля ввода к общей ширине
        on_button_press (function): Функция, вызываемая при нажатии на кнопку
        on_text_changed (function): Функция, вызываемая при изменении текста в поле ввода
        height (int): Высота поля ввода
        debug_mode (bool): Режим отладки
    """

    def __init__(
        self,
        input_hint="Введите текст",
        button_text="Поиск",
        input_ratio=0.8,
        height=35,
        debug_mode=False,
        **kwargs,
    ):
        super().__init__(orientation="vertical", **kwargs)
        self.debug_mode = debug_mode
        self.height = height

        # Горизонтальный контейнер для поля и кнопки
        search_box = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=height, spacing=2
        )

        self.input = TextInput(
            hint_text=input_hint,
            multiline=False,
            halign="center",
            size_hint=(input_ratio, 1),
        )

        self.button = Button(text=button_text, size_hint=(1 - input_ratio, 1))

        search_box.add_widget(self.input)
        search_box.add_widget(self.button)
        self.add_widget(search_box)
        self.bind(pos=self._update_debug_bg, size=self._update_debug_bg)

    def _update_debug_bg(self, *args):
        """Обновляет фон поля ввода для отладки"""
        if self.debug_mode:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(1, 1, 1, 0.7)
                Rectangle(pos=self.pos, size=self.size)
        else:
            self.canvas.before.clear()


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout

    from machine_tools_gui_kivi.app.components.dropdown_list import DropdownList

    class TestSearchBarApp(App):
        def build(self):
            root = FloatLayout()
            self.searchbar = SearchBar(
                input_hint="Поиск фрукта...",
                button_text="Найти",
                input_ratio=0.7,
                height=35,
                debug_mode=False,
            )
            self.searchbar.size_hint = (1, None)
            self.searchbar.pos_hint = {"top": 1}
            root.add_widget(self.searchbar)

            # --- Добавляем выпадающий список ---
            self.dropdown = DropdownList(
                size_hint=(0.7, None),  # ширина совпадает с полем ввода
                height=150,
                item_height=30,
                item_spacing=2,
                bar_width=10,
                item_cols=1,
                opacity=0,  # изначально скрыт
            )
            root.add_widget(self.dropdown)

            # Привязываем обработчики
            self.searchbar.input.bind(focus=self.on_focus)
            self.searchbar.input.bind(text=self.on_print_text)
            self.searchbar.button.bind(on_release=self.on_search)
            self.dropdown.on_select = self.on_dropdown_select

            return root

        def on_print_text(self, instance, value):
            # Фильтрация вариантов
            options = [
                "Apple",
                "Banana",
                "Orange",
                "Grape",
                "Pineapple",
                "Mango",
                "Melon",
                "Lemon",
            ]
            filtered = (
                [opt for opt in options if value.lower() in opt.lower()]
                if value
                else []
            )
            self.dropdown.update_items(filtered)
            # Показываем список только если есть варианты и поле в фокусе
            if filtered and self.searchbar.input.focus:
                self.dropdown.opacity = 1
                # Позиционируем dropdown под searchbar
                self.dropdown.width = self.searchbar.input.width
                self.dropdown.x = self.searchbar.input.to_window(
                    self.searchbar.input.x, self.searchbar.input.y
                )[0]
                self.dropdown.y = (
                    self.searchbar.input.to_window(
                        self.searchbar.input.x, self.searchbar.input.y
                    )[1]
                    - self.dropdown.height
                )
            else:
                self.dropdown.opacity = 0

        def on_focus(self, instance, value):
            if not value:
                self.dropdown.opacity = 0

        def on_dropdown_select(self, value):
            self.searchbar.input.text = value
            self.dropdown.opacity = 0

        def on_search(self, instance):
            value = self.searchbar.input.text
            print(f"Поиск: {value}")

    TestSearchBarApp().run()
