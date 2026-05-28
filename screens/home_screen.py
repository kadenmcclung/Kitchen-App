from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock  # <-- Added
from datetime import datetime

from db_utils import fetch_items, delete_item, update_item  # Only fetch, delete, update


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
            return None  # or return "" depending on your DB expectations
    return None


class EditPopup(Popup):
    def __init__(self, item, on_save, **kwargs):
        super().__init__(**kwargs)
        self.title = "Edit Item"
        self.size_hint = (0.8, 0.6)
        self.auto_dismiss = False
        self.item = item
        self.on_save = on_save

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.name_input = TextInput(text=item[0], hint_text='Name')
        self.quantity_input = TextInput(text=str(item[1]), hint_text='Quantity')
        self.expiration_input = TextInput(text=format_date(item[2]), hint_text='Expiration (MM-DD-YYYY)')
        self.date_entered_input = TextInput(text=format_date(item[3]), hint_text='Date Entered (MM-DD-YYYY)')
        self.category_input = TextInput(text=item[4], hint_text='Category')

        layout.add_widget(self.name_input)
        layout.add_widget(self.quantity_input)
        layout.add_widget(self.expiration_input)
        layout.add_widget(self.date_entered_input)
        layout.add_widget(self.category_input)

        button_box = BoxLayout(size_hint_y=0.3, spacing=10)
        save_button = Button(text='Save')
        cancel_button = Button(text='Cancel')

        save_button.bind(on_press=self.save_item)
        cancel_button.bind(on_press=self.dismiss)

        button_box.add_widget(save_button)
        button_box.add_widget(cancel_button)
        layout.add_widget(button_box)

        self.content = layout

    def save_item(self, _):
        from_name = self.item[0]
        new_name = self.name_input.text
        quantity = self.quantity_input.text.strip()
        expiration = unformat_date(self.expiration_input.text.strip())
        date_entered = unformat_date(self.date_entered_input.text.strip())
        category = self.category_input.text

        update_item(from_name, new_name, quantity, expiration, date_entered, category)
        self.dismiss()
        self.on_save()


class HomeScreen(Screen):

    def delete_and_refresh(self, name):
        delete_item(name)
        self.populate_items()

    def open_edit_popup(self, item):
        popup = EditPopup(item, on_save=self.populate_items)
        popup.open()