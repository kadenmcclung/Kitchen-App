from db_utils import init_db
import sys


def run_app():
    from kivy.app import App
    from kivy.lang import Builder
    from kivy.uix.screenmanager import ScreenManager
    from screens.home_screen import HomeScreen
    from screens.add_item_screen import AddItemScreen
    from screens.inventory_screen import InventoryScreen
    from screens.shopping_list_screen import ShoppingListScreen
    from screens.templates_screen import TemplatesScreen
    from screens.recipes_screen import RecipesScreen

    class KitchenApp(App):
        def build(self):
            init_db()

            # Load all .kv files once during build
            Builder.load_file('ui/home_screen.kv')
            Builder.load_file('ui/add_item_screen.kv')
            Builder.load_file('ui/inventory_screen.kv')
            Builder.load_file('ui/shopping_list_screen.kv')
            Builder.load_file('ui/templates_screen.kv')
            Builder.load_file('ui/recipes_screen.kv')
            Builder.load_file('ui/main.kv')

            sm = ScreenManager()
            sm.add_widget(HomeScreen(name='home'))
            sm.add_widget(AddItemScreen(name='add_item'))
            sm.add_widget(InventoryScreen(name='inventory'))
            sm.add_widget(ShoppingListScreen(name='shopping_list'))
            sm.add_widget(TemplatesScreen(name='templates'))
            sm.add_widget(RecipesScreen(name='recipes'))

            return sm
    KitchenApp().run()


def run_test_mode():
    print("Container test mode: app imported successfully")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_test_mode()
    else:
        run_app()
