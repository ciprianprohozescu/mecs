import json
from datetime import datetime
from databaseHelper import DBConnection

#SQL stuff
db_file = r'../../mecs.db'
connection = DBConnection(db_file)

def event_query(event):
    sql_query = f"""SELECT * FROM events WHERE event = '{event['event']}' AND node = '{event['node']}';"""
    return connection.execute_query(sql_query)

def event_insert(event):
    sql_insert = f"""INSERT INTO events (event, node, count) VALUES ('{event['event']}', '{event['node']}', 1);"""
    connection.execute_statement(sql_insert)

def event_update(event):
    sql_update = f"""UPDATE events SET count = {event[3] + 1} WHERE event = '{event[1]}' AND node = '{event[2]}';"""
    connection.execute_statement(sql_update)

def relation_query(event1, event2):
    sql_query = f"""SELECT * FROM event_relations WHERE cause = {event1['id']} AND effect = {event2['id']}"""
    return connection.execute_query(sql_query)

def relation_insert(event1, event2):
    time_dif = int(event2['time'] - event1['time'])
    sql_insert = f"""INSERT INTO event_relations (cause, effect, count, time_average) VALUES ({event1['id']}, {event2['id']}, 1, {time_dif})"""
    connection.execute_statement(sql_insert)

def relation_update(event1, event2, relation):
    count = relation[2]
    time_average = relation[3]

    time_dif = int(event2['time'] - event1['time'])
    time_average = time_average / (count + 1) * count + time_dif / (count + 1)
    count += 1

    sql_update = f"""UPDATE event_relations SET count = {count}, time_average = {time_average} WHERE cause = '{event1['id']}' AND effect = '{event2['id']}';"""
    connection.execute_statement(sql_update)

ringdump = open('../../ringdump.json', 'r')

#read the first event
line = ringdump.readline()
event = json.loads(line)
while ('time' not in event) or ('event' not in event) or ('node' not in event):
    line = ringdump.readline()
    event = json.loads(line)
    continue

total_events = 1

event['time'] = float(event['time'])

db_events = event_query(event)

if len(db_events) == 0:
    event_insert(event)
    db_events = event_query(event)
else:
    event_update(db_events[0])
event['id'] = db_events[0][0]

last_event = event
line = ringdump.readline()

while line and (total_events <= 10000):
    event = json.loads(line)

    #if event is incomplete, ignore it
    if ('time' not in event) or ('event' not in event) or ('node' not in event):
        line = ringdump.readline()
        continue

    total_events += 1

    #parse time from exponential format
    event['time'] = float(event['time'])

    #insert or update event
    events = event_query(event)
    if len(events) == 0:
        event_insert(event)
        events = event_query(event)
    else:
        event_update(events[0])
    event['id'] = events[0][0]

    #insert or update relation between this event and the last
    relations = relation_query(last_event, event)
    if len(relations) == 0:
        relation_insert(last_event, event)
    else:
        relation_update(last_event, event, relations[0])

    last_event = event
    line = ringdump.readline()

ringdump.close()
            