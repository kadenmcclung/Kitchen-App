import sqlite3
import os
from datetime import datetime, timedelta


def init_db():
    if not os.path.exists('db'):
        os.makedirs('db')
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity TEXT,
            expiration TEXT,
            date_entered TEXT,
            category TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS shopping_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS template_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_name TEXT NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS template_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (template_id) REFERENCES template_names(id) ON DELETE CASCADE
        )
    ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS recipe_names (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_name TEXT NOT NULL UNIQUE
            )
        ''')

    c.execute('''
            CREATE TABLE IF NOT EXISTS recipe_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                quantity TEXT,
                FOREIGN KEY (recipe_id) REFERENCES recipe_names(id) ON DELETE CASCADE
            )
        ''')

    conn.commit()
    conn.close()


def insert_item(name, quantity, expiration, date_entered, category):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO items (name, quantity, expiration, date_entered, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, quantity, expiration, date_entered, category))
    conn.commit()
    conn.close()


def update_item(old_name, new_name, quantity, expiration, date_entered, category):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('''
        UPDATE items
        SET name = ?, quantity = ?, expiration = ?, date_entered = ?, category = ?
        WHERE name = ?
    ''', (new_name, quantity, expiration, date_entered, category, old_name))
    conn.commit()
    conn.close()


def delete_item(name):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE name = ?', (name,))
    conn.commit()
    conn.close()


def fetch_items():
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('SELECT name, quantity, expiration, date_entered, category FROM items')
    items = c.fetchall()
    conn.close()
    return items


def insert_shopping_item(name, quantity):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO shopping_list (name, quantity)
        VALUES (?, ?)
    ''', (name, quantity))
    conn.commit()
    conn.close()


def update_shopping_item(old_name, new_name, quantity):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('''
        UPDATE shopping_list
        SET name = ?, quantity = ?
        WHERE name = ?
    ''', (new_name, quantity, old_name))
    conn.commit()
    conn.close()


def delete_shopping_item(name):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('DELETE FROM shopping_list WHERE name = ?', (name,))
    conn.commit()
    conn.close()


def fetch_shopping_items():
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute('SELECT name, quantity FROM shopping_list')
    items = c.fetchall()
    conn.close()
    return items


def insert_template_name(template_name):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("INSERT INTO template_names (template_name) VALUES (?)", (template_name,))
    conn.commit()
    template_id = c.lastrowid
    conn.close()
    return template_id


def insert_template_item(template_id, item_name):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("INSERT INTO template_items (template_id, name) VALUES (?, ?)", (template_id, item_name))
    conn.commit()
    conn.close()


def fetch_template_names():
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("SELECT id, template_name FROM template_names")
    templates = c.fetchall()
    conn.close()
    return templates


def fetch_items_by_template_id(template_id):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("SELECT name FROM template_items WHERE template_id = ?", (template_id,))
    items = [row[0] for row in c.fetchall()]
    conn.close()
    return items


def delete_template(template_id):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("DELETE FROM template_names WHERE id = ?", (template_id,))
    c.execute("DELETE FROM template_items WHERE template_id = ?", (template_id,))
    conn.commit()
    conn.close()


def delete_template_item(template_id, item_name):
    conn = sqlite3.connect('db/app.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM template_items
        WHERE template_id = ? AND name = ?
    ''', (template_id, item_name))
    conn.commit()
    conn.close()


def insert_recipe_name(recipe_name):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("INSERT INTO recipe_names (recipe_name) VALUES (?)", (recipe_name,))
    conn.commit()
    recipe_id = c.lastrowid
    conn.close()
    return recipe_id


def insert_recipe_item(recipe_id, item_name, quantity):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("INSERT INTO recipe_items (recipe_id, name, quantity) VALUES (?, ?, ?)", (recipe_id, item_name, quantity))
    conn.commit()
    conn.close()


def fetch_recipe_names():
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("SELECT id, recipe_name FROM recipe_names")
    recipes = c.fetchall()
    conn.close()
    return recipes


def fetch_items_by_recipe_id(recipe_id):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("SELECT name, quantity FROM recipe_items WHERE recipe_id = ?", (recipe_id,))
    items = c.fetchall()
    conn.close()
    return items


def delete_recipe(recipe_id):
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()
    c.execute("DELETE FROM recipe_names WHERE id = ?", (recipe_id,))
    c.execute("DELETE FROM recipe_items WHERE recipe_id = ?", (recipe_id,))
    conn.commit()
    conn.close()


def delete_recipe_item(recipe_id, item_name, quantity):
    conn = sqlite3.connect('db/app.db')
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM recipe_items
        WHERE recipe_id = ? AND name = ? AND quantity = ?
    ''', (recipe_id, item_name, quantity))
    conn.commit()
    conn.close()


def fetch_items_expiring_soon():
    conn = sqlite3.connect('db/app.db')
    c = conn.cursor()

    today = datetime.now().date()
    two_weeks_later = today + timedelta(days=14)

    c.execute("""
        SELECT name, quantity, expiration, date_entered, category
        FROM items
        WHERE expiration IS NOT NULL AND expiration != ''
        AND date(expiration) BETWEEN date(?) AND date(?)
        ORDER BY expiration ASC
    """, (today.isoformat(), two_weeks_later.isoformat()))

    items = c.fetchall()
    conn.close()
    return items
