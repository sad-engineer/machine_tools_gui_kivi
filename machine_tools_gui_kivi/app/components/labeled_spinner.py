#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner, SpinnerOption


class CustomSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        row_height = kwargs.pop("row_height", 100)
        super().__init__(**kwargs)
        self.height = row_height
        self.valign = "middle"
        self.halign = "left"
        self.padding = [10, 0, 0, 0]
        self.bind(size=self._update_text_size)
        self._update_text_size()

    def _update_text_size(self, *args):
        """Обновляет text_size при изменении размера виджета"""
        self.text_size = (
            self.width - self.padding[0] - self.padding[2],
            self.height - self.padding[1] - self.padding[3],
        )


class LabeledSpinner(BoxLayout):
    def __init__(
        self, label_text, values, spinner_text=None, height=65, spacing=5, debug_mode=False, row_height=30, **kwargs
    ):
        super().__init__(orientation="vertical", size_hint=(1, None), height=height, spacing=spacing, **kwargs)
        self.debug_mode = debug_mode
        # Лейбл
        label = Label(
            text=label_text,
            size_hint=(1, None),
            height=30,
            halign="left",
            valign="middle",
        )
        label.bind(size=lambda *x: setattr(label, "text_size", (label.width, label.height)))
        self.label = label
        # Выпадающий список
        spinner = Spinner(
            text=spinner_text if spinner_text else (values[0] if values else ""),
            values=values,
            size_hint=(1, 1),
            halign="left",
            valign="middle",
            padding=[10, 0, 0, 0],
            option_cls=lambda **opt_kwargs: CustomSpinnerOption(row_height=row_height, **opt_kwargs),
        )
        spinner.bind(
            size=lambda *x: setattr(
                spinner,
                "text_size",
                (
                    spinner.width - spinner.padding[0] - spinner.padding[2],
                    spinner.height - spinner.padding[1] - spinner.padding[3],
                ),
            )
        )
        self.spinner = spinner

        self.add_widget(self.label)
        self.add_widget(self.spinner)

        # DEBUG background
        self.bind(pos=self._update_debug_bg, size=self._update_debug_bg)
        self._update_debug_bg()

    def on_touch_down(self, touch):
        """Обработка нажатия мыши"""
        if self.collide_point(*touch.pos):
            if touch.button == "right":
                self.spinner.text = ""
                return True
        return super().on_touch_down(touch)

    def _update_debug_bg(self, *args):
        """Обновляет фон для отладки"""
        if self.debug_mode:
            self.canvas.before.clear()
            self.padding = [2, 2, 2, 2]
            with self.canvas.before:
                Color(1, 1, 0, 0.2)
                Rectangle(pos=self.pos, size=self.size)
        else:
            self.canvas.before.clear()

    def set_value(self, substring):
        """Устанавливает значение спинера по тексту"""
        for description in self.spinner.values:
            if substring in description:
                self.spinner.text = description
                return True
        return False

    def get_value(self):
        """Возвращает значение спинера."""
        return self.spinner.text


if __name__ == "__main__":
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.floatlayout import FloatLayout

    class TestLabeledSpinnerApp(App):
        def build(self):
            Window.size = (400, 120)
            root = FloatLayout()
            # Пример значений
            values = [
                "Токарные станки",
                "Фрезерные станки",
                "Шлифовальные станки",
                "Комбинированные",
                "Разные станки",
            ]
            labeled_spinner = LabeledSpinner(
                label_text="Группа станка:",
                values=values,
                # size_hint=(1, None),
                height=65,
                pos_hint={"top": 1},
                debug_mode=True,
            )
            root.add_widget(labeled_spinner)
            return root

    TestLabeledSpinnerApp().run()
