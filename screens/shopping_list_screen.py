from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from db_utils import fetch_shopping_items, insert_shopping_item, delete_shopping_item, update_shopping_item


class ShoppingListScreen(Screen):
    def on_pre_enter(self):
        Clock.schedule_once(self.delayed_populate, 0)

    def delayed_populate(self, dt):
        self.populate_items()

    def populate_items(self):
        self.ids.shopping_list_container.clear_widgets()

        items = fetch_shopping_items()
        for item in items:
            self.add_item_row(item)

    def add_item_row(self, item):
        name, quantity = item

        row = BoxLayout(size_hint_y=None, height=40, spacing=10)

        row.add_widget(Label(text=name, size_hint_x=0.4))
        row.add_widget(Label(text=str(quantity), size_hint_x=0.25))

        edit_button = Button(text='Edit', size_hint_x=0.15)
        edit_button.bind(on_release=lambda instance: self.show_edit_popup(name, quantity))
        row.add_widget(edit_button)

        delete_button = Button(text='Delete', size_hint_x=0.15)
        delete_button.bind(on_release=lambda instance: self.delete_and_refresh(name))
        row.add_widget(delete_button)

        self.ids.shopping_list_container.add_widget(row)

    def delete_and_refresh(self, name):
        delete_shopping_item(name)
        self.populate_items()

    def open_add_popup(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        name_input = TextInput(hint_text="Item Name")
        quantity_input = TextInput(hint_text="Quantity")

        add_btn = Button(text="Add", size_hint_y=None, height=40)

        popup = Popup(title="Add Shopping Item",
                      content=layout,
                      size_hint=(0.8, 0.5))

        def add_and_close(instance):
            name = name_input.text.strip()
            quantity = quantity_input.text.strip()
            if name and quantity:
                insert_shopping_item(name, quantity)
                popup.dismiss()
                self.populate_items()

        add_btn.bind(on_press=add_and_close)

        layout.add_widget(name_input)
        layout.add_widget(quantity_input)
        layout.add_widget(add_btn)

        popup.open()

    def show_edit_popup(self, current_name, current_quantity):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        name_input = TextInput(text=current_name, hint_text='Item Name')
        quantity_input = TextInput(text=current_quantity, hint_text='Quantity')

        save_button = Button(text='Save')

        popup = Popup(title=f'Edit "{current_name}"', content=popup_layout, size_hint=(0.8, 0.5))

        save_button.bind(
            on_release=lambda instance: self.save_edited_item(current_name, name_input.text, quantity_input.text, popup)
        )

        popup_layout.add_widget(name_input)
        popup_layout.add_widget(quantity_input)
        popup_layout.add_widget(save_button)

        popup.open()

    def save_edited_item(self, old_name, new_name, new_quantity, popup):
        update_shopping_item(old_name, new_name, new_quantity)
        popup.dismiss()
        self.populate_items()



