#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class DropdownList(ScrollView):
    """Выпадающий список с прокруткой.

    Args:
    on_select - функция, выполняемая при выборе значения из списка вариантов
    height - высота списка
    item_height - высота элемента списка
    item_spacing - отступ между элементами списка
    bar_width - ширина полосы прокрутки
    item_cols - количество колонок в списке
    """

    def __init__(
        self,
        on_select=None,
        height=200,
        item_height=30,
        item_spacing=2,
        bar_width=10,
        item_cols=1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.bar_width = bar_width
        self.scroll_type = ["bars", "content"]
        self.on_select = on_select
        self.dropdown_height = height
        self.btn_item_height = item_height
        self.btn_item_spacing = item_spacing

        # Создаем сетку для элементов списка
        self.grid = GridLayout(
            cols=item_cols, spacing=self.btn_item_spacing, size_hint_y=None
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.add_widget(self.grid)

    def update_items(self, items):
        """Обновляет элементы списка."""
        self.grid.clear_widgets()
        if items:
            for item in items:
                btn = Button(
                    text=item,
                    size_hint_y=None,
                    height=self.btn_item_height,
                )
                btn.bind(on_release=lambda btn, item=item: self._on_item_select(item))
                self.grid.add_widget(btn)
            height = (
                len(items) * (self.btn_item_height + self.btn_item_spacing)
                - self.btn_item_spacing
            )
            self.height = min(self.dropdown_height, height)
            self.opacity = 1
        else:
            self.height = 0
            self.opacity = 0

    def _on_item_select(self, value):
        """Обработчик выбора значения из списка."""
        print(value)
        if self.on_select:
            self.on_select(value)


if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.widget import Widget

    class TestDropdownApp(App):
        def build(self):
            root = FloatLayout()
            # Поле ввода — фиксируем по ширине и позиции
            self.input = TextInput(
                size_hint=(0.5, None),
                height=40,
                pos_hint={"top": 0.95, "center_x": 0.5},
            )

            root.add_widget(self.input)

            # Выпадающий список — изначально скрыт, позиционируем под полем ввода
            self.dropdown = DropdownList(
                size_hint=(0.5, None),
                height=200,
                pos_hint={
                    "top": 0.95 - 40 / root.height,
                    "center_x": 0.5,
                },  # top чуть ниже input
                opacity=0,
            )
            root.add_widget(self.dropdown)

            self.input.bind(text=self.on_text, focus=self.on_focus)
            return root

        def on_text(self, instance, value):
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
            if filtered and self.input.focus:
                self.dropdown.opacity = 1
                # Позиционируем dropdown под input
                self.dropdown.pos = (self.input.x, self.input.y - self.dropdown.height)
            else:
                self.dropdown.opacity = 0

        def on_focus(self, instance, value):
            if not value:
                self.dropdown.opacity = 0

    TestDropdownApp().run()
