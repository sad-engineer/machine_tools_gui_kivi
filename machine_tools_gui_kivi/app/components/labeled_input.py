#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LabeledInput(BoxLayout):
    def __init__(
        self,
        label_text,
        input_text="",
        units=None,
        height=65,
        spacing=5,
        debug_mode=False,
        **kwargs
    ):
        super().__init__(
            orientation="vertical",
            size_hint=(1, None),
            height=height,
            spacing=spacing,
            **kwargs
        )
        self.debug_mode = debug_mode

        # Лейбл
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
        self.label = label

        # Контейнер для поля ввода и единиц измерения
        input_container = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=30, spacing=5
        )

        # Поле ввода
        input_field = TextInput(
            text=input_text,
            size_hint=(1, None),
            height=30,
            halign="left",

        )
        self.input_field = input_field
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

        self.add_widget(self.label)
        self.add_widget(input_container)

        # DEBUG background
        self.bind(pos=self._update_debug_bg, size=self._update_debug_bg)
        self._update_debug_bg()

    def _update_debug_bg(self, *args):
        """Обновляет фон для отладки"""
        if self.debug_mode:
            self.canvas.before.clear()
            self.padding = [2, 2, 2, 2]
            with self.canvas.before:
                Color(0, 1, 1, 0.2)  # Синий с прозрачностью
                Rectangle(pos=self.pos, size=self.size)
        else:
            self.canvas.before.clear()

    def set_value(self, string):
        """Устанавливает значение поля ввода."""
        self.input_field.text = string
    
    def get_value(self):
        """Возвращает значение поля ввода."""
        return self.input_field.text


if __name__ == "__main__":
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.floatlayout import FloatLayout

    class TestLabeledInputApp(App):
        def build(self):
            Window.size = (400, 120)
            root = FloatLayout()
            
            labeled_input = LabeledInput(
                label_text="Название:",
                input_text="Тестовое значение",
                units="мм",
                height=65,
                pos_hint={"top": 1},
                debug_mode=True,
            )
            root.add_widget(labeled_input)
            return root

    TestLabeledInputApp().run() 