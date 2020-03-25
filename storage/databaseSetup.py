import os
from databaseHelper import DBConnection

db_file = os.path.expanduser('~/Telenor/mecs.db')
connection = DBConnection(db_file)

def purge():
    drop_events = 'DROP TABLE IF EXISTS events;'

    connection.execute_statement(drop_events)

def setup():
    create_events = """CREATE TABLE IF NOT EXISTS events (
        id integer PRIMARY KEY,
        time real,
        node text,
        event integer
        level text);"""
    
    connection.execute_statement(create_events)

purge()
setup()