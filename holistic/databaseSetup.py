from databaseHelper import DBConnection

db_file = r'../../mecs.db'
connection = DBConnection(db_file)

def purge():
    drop_events = 'DROP TABLE IF EXISTS events;'
    drop_event_relations = 'DROP TABLE IF EXISTS event_relations'

    connection.execute_statement(drop_events)
    connection.execute_statement(drop_event_relations)

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
    
    connection.execute_statement(create_events)
    connection.execute_statement(create_event_relations)

purge()
setup()