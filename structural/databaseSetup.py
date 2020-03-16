from databaseHelper import DBConnection

db_file = r'../../mecs.db'
connection = DBConnection(db_file)

def purge():
    drop_properties = 'DROP TABLE IF EXISTS properties;'
    drop_property_relations = 'DROP TABLE IF EXISTS property_relations'

    connection.execute_statement(drop_properties)
    connection.execute_statement(drop_property_relations)

def setup():
    create_properties = """CREATE TABLE IF NOT EXISTS properties (
        type text NOT NULL,
        value text NOT NULL,
        PRIMARY KEY (type, value));"""
    create_property_relations = """CREATE TABLE IF NOT EXISTS property_relations (
        cause integer,
        effect integer,
        count integer NOT NULL,
        time_average integer NOT NULL,
        PRIMARY KEY (cause, effect));"""
    
    connection.execute_statement(create_properties)
    connection.execute_statement(create_property_relations)

purge()
setup()