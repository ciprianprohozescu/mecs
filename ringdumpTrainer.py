import json
from databaseHelper import DBConnection

db_file = r'../mecs.db'
connection = DBConnection(db_file)

total_events = 0

def event_query(event):
    sql_query = f"""SELECT * FROM events WHERE event = '{event['event']}' AND node = '{event['node']}';"""
    return connection.execute_query(sql_query)

def event_insert(event):
    sql_insert = f"""INSERT INTO events (event, node, count) VALUES ('{event['event']}', '{event['node']}', 1);"""
    connection.execute_statement(sql_insert)

def event_update(event):
    sql_update = f"""UPDATE events SET count = {event[3] + 1} WHERE event = '{event[1]}' AND node = '{event[2]}';"""
    connection.execute_statement(sql_update)

with open('../ringdump.json', 'r') as ringdump:
    line = ringdump.readline()

    while line and total_events <= 10:
        event = json.loads(line)
        total_events += 1

        db_events = event_query(event)

        if len(db_events) == 0:
            event_insert(event)
        else:
            event_update(db_events[0])

print(connection.execute_query("SELECT * from events;"))
            