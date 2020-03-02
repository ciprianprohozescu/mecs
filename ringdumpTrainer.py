import sqlite3
from sqlite3 import Error

connection = None

def create_connection(db_file):
    global connection

    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

def execute_statement(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)

def execute_query(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
    except Error as e:
        print(e)
    return cursor.fetchall()

def purge():
    drop_events = 'DROP TABLE IF EXISTS events;'
    drop_event_relations = 'DROP TABLE IF EXISTS event_relations'

    execute_statement(drop_events)
    execute_statement(drop_event_relations)

def setup():
    create_events = """CREATE TABLE IF NOT EXISTS events (
        id integer PRIMARY KEY AUTOINCREMENT,
        event text NOT NULL,
        node text NOT NULL,
        count integer NOT NULL);"""
    create_event_relations = """CREATE TABLE IF NOT EXISTS event_relations (
        cause integer,
        effect integer,
        count integer NOT NULL,
        time_average integer NOT NULL,
        PRIMARY KEY (cause, effect));"""
    
    execute_statement(create_events)
    execute_statement(create_event_relations)

create_connection(r'../mecs.db')
purge()
setup()