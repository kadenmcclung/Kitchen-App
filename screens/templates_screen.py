from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp

from db_utils import (
    fetch_template_names,
    fetch_items_by_template_id,
    insert_template_name,
    insert_template_item,
    delete_template,
    delete_template_item,
    insert_shopping_item
)


class TemplatesScreen(Screen):
    def on_pre_enter(self):
        Clock.schedule_once(self.delayed_populate)

    def delayed_populate(self, dt):
        self.populate_templates()

    def populate_templates(self):
        scroll_view = self.ids.templates_scrollview
        scroll_y_before = scroll_view.scroll_y if scroll_view else 1

        container = self.ids.templates_container
        container.clear_widgets()

        templates = fetch_template_names()

        for template_id, template_name in templates:
            box = BoxLayout(orientation='vertical', size_hint_y=None)
            box.bind(minimum_height=box.setter('height'))

            # First row: template name label full width
            name_row = BoxLayout(size_hint_y=None, height=40)
            name_row.add_widget(Label(text=template_name))
            box.add_widget(name_row)

            # Second row: buttons with fixed widths
            button_row = BoxLayout(size_hint_y=None, height=40)

            edit_btn = Button(text='Edit', size_hint_x=None, width=dp(70))
            edit_btn.bind(on_press=lambda _, tid=template_id, tname=template_name: self.open_edit_popup(tid, tname))
            button_row.add_widget(edit_btn)

            del_btn = Button(text='Delete', size_hint_x=None, width=dp(70))
            del_btn.bind(on_press=lambda _, tid=template_id: self.remove_template(tid))
            button_row.add_widget(del_btn)

            add_all_btn = Button(text='Add All to List', size_hint_x=None, width=dp(120))
            add_all_btn.bind(on_press=lambda _, tid=template_id: self.add_all_to_shopping_list(tid))
            button_row.add_widget(add_all_btn)

            box.add_widget(button_row)

            items = fetch_items_by_template_id(template_id)
            for item in items:
                row = BoxLayout(size_hint_y=None, height=30, spacing=10)
                row.add_widget(Label(text=item))

                add_btn = Button(text='+', size_hint_x=0.15)
                add_btn.bind(on_press=lambda _, i=item: self.add_single_item_to_list(i))
                row.add_widget(add_btn)

                delete_btn = Button(text='Delete', size_hint_x=0.25)
                delete_btn.bind(on_press=lambda _, tid=template_id, i=item: self.remove_template_item(tid, i))
                row.add_widget(delete_btn)

                box.add_widget(row)

            container.add_widget(box)

        def restore_scroll(dt):
            scroll_view.scroll_y = scroll_y_before

        Clock.schedule_once(restore_scroll, 0)

    def open_add_template_popup(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        template_input = TextInput(hint_text='Template Name', multiline=False)
        item_input = TextInput(hint_text='First Item', multiline=False)
        add_btn = Button(text='Create')

        popup = Popup(title='New Template', content=layout, size_hint=(0.8, 0.5))

        def create_template(instance):
            name = template_input.text.strip()
            item = item_input.text.strip()
            if name and item:
                template_id = insert_template_name(name)
                insert_template_item(template_id, item)
                popup.dismiss()
                self.populate_templates()

        add_btn.bind(on_press=create_template)

        layout.add_widget(template_input)
        layout.add_widget(item_input)
        layout.add_widget(add_btn)

        popup.open()

    def open_edit_popup(self, template_id, template_name):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        item_input = TextInput(hint_text='Add New Item', multiline=False)
        add_btn = Button(text='Add')

        popup = Popup(title='Edit Template', content=layout, size_hint=(0.8, 0.4))

        def add_item(instance):
            item_name = item_input.text.strip()
            if item_name:
                insert_template_item(template_id, item_name)
                popup.dismiss()
                self.populate_templates()

        add_btn.bind(on_press=add_item)

        layout.add_widget(Label(text=f'Editing: {template_name}'))
        layout.add_widget(item_input)
        layout.add_widget(add_btn)

        popup.open()

    def remove_template(self, template_id):
        delete_template(template_id)
        self.populate_templates()

    def remove_template_item(self, template_id, item_name):
        delete_template_item(template_id, item_name)
        self.populate_templates()

    def add_all_to_shopping_list(self, template_id):
        items = fetch_items_by_template_id(template_id)
        for item in items:
            insert_shopping_item(item, "")
        self.populate_templates()

    def add_single_item_to_list(self, item):
        insert_shopping_item(item, "")
        self.populate_templates()


