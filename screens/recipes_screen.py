from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp

from db_utils import (
    fetch_recipe_names,
    fetch_items_by_recipe_id,
    insert_recipe_name,
    insert_recipe_item,
    delete_recipe,
    delete_recipe_item,
    insert_shopping_item
)


class RecipesScreen(Screen):
    def on_pre_enter(self):
        Clock.schedule_once(self.delayed_populate)

    def delayed_populate(self, dt):
        self.populate_recipes()

    def populate_recipes(self):
        scroll_view = self.ids.recipes_scrollview
        scroll_y_before = scroll_view.scroll_y if scroll_view else 1

        container = self.ids.recipes_container
        container.clear_widgets()

        recipes = fetch_recipe_names()

        for recipe_id, recipe_name in recipes:
            box = BoxLayout(orientation='vertical', size_hint_y=None)
            box.bind(minimum_height=box.setter('height'))

            # First row: Recipe name label full width
            name_row = BoxLayout(size_hint_y=None, height=40)
            name_row.add_widget(Label(text=recipe_name))
            box.add_widget(name_row)

            # Second row: buttons with fixed widths
            button_row = BoxLayout(size_hint_y=None, height=40)

            edit_btn = Button(text='Edit', size_hint_x=None, width=dp(70))
            edit_btn.bind(on_press=lambda _, rid=recipe_id, rname=recipe_name: self.open_edit_popup(rid, rname))
            button_row.add_widget(edit_btn)

            del_btn = Button(text='Delete', size_hint_x=None, width=dp(70))
            del_btn.bind(on_press=lambda _, rid=recipe_id: self.remove_recipe(rid))
            button_row.add_widget(del_btn)

            add_all_btn = Button(text='Add All to List', size_hint_x=None, width=dp(120))
            add_all_btn.bind(on_press=lambda _, rid=recipe_id: self.add_all_to_shopping_list(rid))
            button_row.add_widget(add_all_btn)

            box.add_widget(button_row)

            items = fetch_items_by_recipe_id(recipe_id)
            for name, quantity in items:
                row = BoxLayout(size_hint_y=None, height=30, spacing=10)
                row.add_widget(Label(text=f"{name} ({quantity})"))

                add_btn = Button(text='+', size_hint_x=0.15)
                add_btn.bind(on_press=lambda _, n=name, q=quantity: self.add_single_item_to_list(n, q))
                row.add_widget(add_btn)

                delete_btn = Button(text='Delete', size_hint_x=0.25)
                delete_btn.bind(
                    on_press=lambda _, rid=recipe_id, n=name, q=quantity: self.remove_recipe_item(rid, n, q))
                row.add_widget(delete_btn)

                box.add_widget(row)

            container.add_widget(box)

        def restore_scroll(dt):
            scroll_view.scroll_y = scroll_y_before

        Clock.schedule_once(restore_scroll, 0)

    def open_add_recipe_popup(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        recipe_input = TextInput(hint_text='Recipe Name', multiline=False)
        item_input = TextInput(hint_text='Item Name', multiline=False)
        quantity_input = TextInput(hint_text='Quantity', multiline=False)
        add_btn = Button(text='Create')

        popup = Popup(title='New Recipe', content=layout, size_hint=(0.8, 0.5))

        def create_recipe(instance):
            name = recipe_input.text.strip()
            item = item_input.text.strip()
            quantity = quantity_input.text.strip()
            if name and item and quantity:
                recipe_id = insert_recipe_name(name)
                insert_recipe_item(recipe_id, item, quantity)
                popup.dismiss()
                self.populate_recipes()

        add_btn.bind(on_press=create_recipe)

        layout.add_widget(recipe_input)
        layout.add_widget(item_input)
        layout.add_widget(quantity_input)
        layout.add_widget(add_btn)

        popup.open()

    def open_edit_popup(self, recipe_id, recipe_name):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        item_input = TextInput(hint_text='Item Name', multiline=False)
        quantity_input = TextInput(hint_text='Quantity', multiline=False)
        add_btn = Button(text='Add')

        popup = Popup(title='Edit Recipe', content=layout, size_hint=(0.8, 0.4))

        def add_item(instance):
            item_name = item_input.text.strip()
            quantity = quantity_input.text.strip()
            if item_name and quantity:
                insert_recipe_item(recipe_id, item_name, quantity)
                popup.dismiss()
                self.populate_recipes()

        add_btn.bind(on_press=add_item)

        layout.add_widget(Label(text=f'Editing: {recipe_name}'))
        layout.add_widget(item_input)
        layout.add_widget(quantity_input)
        layout.add_widget(add_btn)

        popup.open()

    def remove_recipe(self, recipe_id):
        delete_recipe(recipe_id)
        self.populate_recipes()

    def remove_recipe_item(self, recipe_id, item_name, quantity):
        delete_recipe_item(recipe_id, item_name, quantity)
        self.populate_recipes()

    def add_all_to_shopping_list(self, recipe_id):
        items = fetch_items_by_recipe_id(recipe_id)
        for name, quantity in items:
            insert_shopping_item(name, quantity)
        self.populate_recipes()

    def add_single_item_to_list(self, name, quantity):
        insert_shopping_item(name, quantity)
        self.populate_recipes()

