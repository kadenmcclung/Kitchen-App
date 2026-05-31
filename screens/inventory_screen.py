from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from db_utils import fetch_items, delete_item
from screens.home_screen import EditPopup
from datetime import datetime

from db_utils import (
    fetch_items_expiring_soon
)


def format_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%m-%d-%Y')
        except ValueError:
            return date_str
    return ""


def unformat_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, '%m-%d-%Y').strftime('%Y-%m-%d')
        except ValueError:
            return None
    return None


class InventoryScreen(Screen):
    def on_pre_enter(self):
        Clock.schedule_once(self.delayed_populate, 0)

    def delayed_populate(self, dt):
        self.populate_items()

    def populate_items(self, filters=None):
        self.ids.item_list.clear_widgets()

        items = fetch_items()

        if filters:
            if filters.get("category"):
                items = [i for i in items if i[4].lower() == filters["category"].lower()]
            if filters.get("search"):
                items = [i for i in items if filters["search"].lower() in i[0].lower()]

        for item in items:
            self.add_item_row(item)

    def add_item_row(self, item):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label

        row = BoxLayout(size_hint_y=None, height=40)

        row.add_widget(Label(text=item[0], size_hint_x=0.25))  # Name
        row.add_widget(Label(text=str(item[1]), size_hint_x=0.15))  # Qty
        row.add_widget(Label(text=format_date(item[2]), size_hint_x=0.25))  # Expiration
        row.add_widget(Label(text=item[4], size_hint_x=0.15))  # Category

        edit_btn = Button(text="Edit", size_hint_x=0.1)
        delete_btn = Button(text="Delete", size_hint_x=0.1)

        edit_btn.bind(on_press=lambda _, i=item: self.open_edit_popup(i))
        delete_btn.bind(on_press=lambda _, name=item[0]: self.delete_and_refresh(name))

        row.add_widget(edit_btn)
        row.add_widget(delete_btn)

        self.ids.item_list.add_widget(row)

    def delete_and_refresh(self, name):
        delete_item(name)
        self.populate_items()

    def open_edit_popup(self, item):
        popup = EditPopup(item, on_save=self.populate_items)
        popup.open()

    def apply_filters(self):
        category = self.ids.category_filter.text.strip()
        search = self.ids.search_input.text.strip()
        self.populate_items(filters={"category": category, "search": search})

    def show_expiring_soon(self):
        self.ids.item_list.clear_widgets()
        items = fetch_items_expiring_soon()
        for item in items:
            self.add_item_row(item)


