#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *  # Third-party library

db = SqliteDatabase("diary.db")


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    # Timestamp

    class Meta:
        database = db


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def init():
    """Create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """Show the menu"""
    choice = None

    while choice != 'q':
        clear()
        print("Enter 'q' to quit")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


# CRUD
def add_entry():
    """Add entry"""
    print("Enter your entry. Press ctrl+D when finished")
    data = sys.stdin.read().strip()  # sys.stdin - a Python object that represents the standard input stream. In                                       most cases, this will be the keyboard

    if data:
        if input("Save data [Y/n]").lower() != 'n':
            Entry.create(content=data)
            print("Saved succefully")


def view_entries(search_query=None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
    for entry in entries:
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M%p")
        clear()
        print(timestamp)
        print("=" * len(timestamp))
        print(entry.content)
        print("\n\n"+"="*len(timestamp))
        print("n) new entry")
        print("d) delete entry")
        print("q) return to main menu")

        next_action = input("Action: [Ndq] ").lower().strip()
        if next_action == "q":
            break;
        elif next_action == "d":
            delete_entry(entry)  # Entry refers to the current entry


def search_entries():
    """Search entries for a string"""
    view_entries(input("Search query: "))


def delete_entry(entry):
    """Delete entry"""
    if input("Are you sure you want to delete the entry? [Yn]").lower() == "y":
        entry.delete_instance()  # Deletes the instance
        print("Entry was deleted")


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])


if __name__ == "__main__":
    init()
    menu_loop()
