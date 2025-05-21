#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс правой колонки редактора базы данных.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class PropertyRow(BoxLayout):
    """Строка свойства с названием и значением."""
    
    def __init__(self, property_name, on_value_change=None, on_name_change=None, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint=(1, None),
            height=30,
            spacing=2,
            **kwargs
        )
        
        self.on_value_change = on_value_change
        self.on_name_change = on_name_change
        self._old_name = property_name
        
        # Название свойства
        self.name_input = TextInput(
            text=property_name,
            size_hint=(0.8, 1),
            multiline=False,
            padding=[2, 2, 2, 2],
        )
        
        # Значение свойства
        self.value_input = TextInput(
            text="",
            size_hint=(0.2, 1),
            multiline=False,
            padding=[2, 2, 2, 2],
        )
        
        # Привязываем обработчики изменения значений
        self.value_input.bind(text=self._on_value_change)
        self.name_input.bind(text=self._on_name_change)
        
        self.add_widget(self.name_input)
        self.add_widget(self.value_input)
    
    def _on_value_change(self, instance, value):
        """Обработчик изменения значения."""
        if self.on_value_change:
            self.on_value_change(self.name_input.text, value)
    
    def _on_name_change(self, instance, value):
        """Обработчик изменения названия."""
        if self.on_name_change and value != self._old_name:
            self.on_name_change(self._old_name, value)
            self._old_name = value
    
    def set_value(self, value):
        """Устанавливает значение свойства."""
        self.value_input.text = str(value) if value is not None else ""
    
    def get_value(self):
        """Получает значение свойства."""
        return self.value_input.text
    
    def get_name(self):
        """Получает название свойства."""
        return self.name_input.text


class RightColumn(BoxLayout):
    """
    Класс правой колонки редактора базы данных.
    Отображает свойства в виде таблицы с двумя колонками.
    """
    
    def __init__(self, debug_mode=False, on_property_change=None, on_property_name_change=None, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint=(1, 1),
            spacing=2,
            padding=[2, 2, 2, 2],
            **kwargs
        )
        self.debug_mode = debug_mode
        self.on_property_change = on_property_change
        self.on_property_name_change = on_property_name_change
        self._property_rows = {}  # Словарь для хранения строк свойств
        self._init_content()
    
    def _init_content(self):
        """Инициализирует контент колонки."""
        # Создаем ScrollView
        self.scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=["bars"],
            bar_width=10,
        )
        
        # Создаем контейнер для строк свойств
        self.properties_container = GridLayout(
            cols=1,
            spacing=2,
            size_hint_y=None,
            padding=[0, 0, 0, 0]
        )
        self.properties_container.bind(minimum_height=self.properties_container.setter("height"))
        
        # Добавляем контейнер в ScrollView
        self.scroll_view.add_widget(self.properties_container)
        self.add_widget(self.scroll_view)
    
    def _on_property_value_change(self, property_name, value):
        """Обработчик изменения значения свойства."""
        if self.on_property_change:
            self.on_property_change(property_name, value)
    
    def _on_property_name_change(self, old_name, new_name):
        """Обработчик изменения названия свойства."""
        if self.on_property_name_change:
            self.on_property_name_change(old_name, new_name)
            # Обновляем ключ в словаре строк
            if old_name in self._property_rows:
                self._property_rows[new_name] = self._property_rows.pop(old_name)
    
    def add_property(self, property_name):
        """
        Добавляет новое свойство в таблицу.
        
        Args:
            property_name: Название свойства
        """
        if property_name not in self._property_rows:
            row = PropertyRow(
                property_name,
                on_value_change=self._on_property_value_change,
                on_name_change=self._on_property_name_change
            )
            self._property_rows[property_name] = row
            self.properties_container.add_widget(row)
    
    def set_property_value(self, property_name, value):
        """
        Устанавливает значение для указанного свойства.
        
        Args:
            property_name: Название свойства
            value: Значение свойства
        """
        if property_name in self._property_rows:
            self._property_rows[property_name].set_value(value)
    
    def get_property_value(self, property_name):
        """
        Получает значение указанного свойства.
        
        Args:
            property_name: Название свойства
            
        Returns:
            str: Значение свойства или None, если свойство не найдено
        """
        if property_name in self._property_rows:
            return self._property_rows[property_name].get_value()
        return None
    
    def get_all_properties(self):
        """
        Получает все свойства в виде словаря.
        
        Returns:
            dict: Словарь {название_свойства: значение}
        """
        return {
            name: row.get_value()
            for name, row in self._property_rows.items()
        }
    
    def clear_properties(self):
        """Очищает все свойства."""
        self._property_rows.clear()
        self.properties_container.clear_widgets()
    
    def update_properties(self, properties_dict):
        """
        Обновляет все свойства из словаря.
        
        Args:
            properties_dict: Словарь {название_свойства: значение}
        """
        self.clear_properties()
        for name, value in properties_dict.items():
            self.add_property(name)
            self.set_property_value(name, value)
    
    def update_technical_requirements(self, requirements):
        """
        Обновляет технические требования.
        
        Args:
            requirements: Словарь технических требований
        """
        self.clear_properties()
        for name, value in requirements.items():
            self.add_property(name)
            self.set_property_value(name, value)


if __name__ == "__main__":
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.floatlayout import FloatLayout
    
    class TestRightColumnApp(App):
        def build(self):
            Window.size = (400, 600)
            root = FloatLayout()
            
            right_column = RightColumn(
                size_hint=(1, 1),
                pos_hint={"top": 1},
                debug_mode=True
            )
            
            # Тестовые данные
            test_properties = {
                "Группа станка": "Токарные станки",
                "Тип станка": "Токарно-винторезный",
                "Мощность": "10 кВт",
                "КПД": "85%",
                "Автоматизация": "Полуавтомат",
                "Точность": "Нормальная",
                "Специализация": "Универсальный",
                "Масса": "1000 кг",
                "Класс по массе": "Средний",
                "Размеры": "1000x500x1500 мм",
                "Город": "Москва",
                "Производитель": "Завод им. Иванова"
            }
            
            right_column.update_properties(test_properties)
            root.add_widget(right_column)
            return root
    
    TestRightColumnApp().run() 