from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from kivy.clock import Clock

from db_utils import insert_item


def unformat_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, '%m-%d-%Y').strftime('%Y-%m-%d')
        except ValueError:
            return date_str
    return None


class AddItemScreen(Screen):
    def on_pre_enter(self):
        Clock.schedule_once(self.update_date_input, 0)

    def update_date_input(self, *args):
        self.ids.date_entered_input.text = str(datetime.today().strftime('%m-%d-%Y'))

    def add_item(self):
        name = self.ids.name_input.text.strip()
        quantity = self.ids.quantity_input.text.strip()
        expiration = self.ids.expiration_input.text.strip()
        date_entered = self.ids.date_entered_input.text.strip()
        category = self.ids.category_input.text.strip()

        if name and quantity and category:
            try:
                insert_item(
                    name,
                    quantity,
                    unformat_date(expiration) if expiration else None,
                    unformat_date(date_entered) if date_entered else None,
                    category
                )
                # Clear fields
                self.ids.name_input.text = ""
                self.ids.quantity_input.text = ""
                self.ids.expiration_input.text = ""
                self.ids.date_entered_input.text = str(datetime.today().strftime('%m-%d-%Y'))
                self.ids.category_input.text = ""

                self.manager.current = 'home'
            except ValueError:
                self.show_error_popup("Quantity must be an integer.")
        else:
            self.show_error_popup("Name, quantity, and category are required.")

    def cancel(self):
        self.manager.current = 'home'

    def show_error_popup(self, message):
        popup = Popup(title="Error", content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()

