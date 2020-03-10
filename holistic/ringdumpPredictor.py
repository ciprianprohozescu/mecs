import json
from databaseHelper import DBConnection

current_generation = []
next_generation = []
threshold = 0.1

#SQL stuff
db_file = r'../../mecs.db'
connection = DBConnection(db_file)

def event_query(event):
    sql_query = f"""SELECT * FROM events WHERE event = '{event['event']}' AND node = '{event['node']}';"""
    return connection.execute_query(sql_query)

def related_events_query(event):
    sql_query = f"""SELECT * FROM event_relations
    JOIN events on event_relations.effect = events.id
    WHERE event_relations.cause = {event['id']}"""
    return connection.execute_query(sql_query)

#retrieve and calculate probabilities for all events caused by a given event
def predict(event):
    global next_generation

    parsed_events = []
    total_count = 0

    related_events = related_events_query(event)
    for related_event in related_events:
        parsed_events.append({
            'id': related_event[1],
            'event': related_event[5],
            'node': related_event[6],
            'time': event['time'] + related_event[3],
            'probability': related_event[2]
        })
        total_count += related_event[2]
    
    for parsed_event in parsed_events:
        parsed_event['probability'] = event['probability'] * parsed_event['probability'] / total_count
        if parsed_event['probability'] >= threshold:
            next_generation.append(parsed_event)

#read events from dump, continue on user input
ringdump = open('../../ringdump.json', 'r')

line = ringdump.readline()
while line:
    event = json.loads(line)
    while ('time' not in event) or ('event' not in event) or ('node' not in event):
        line = ringdump.readline()
        event = json.loads(line)
        continue

    events = event_query(event)
    if len(events) == 0:
        print("Event not found")
    else:
        if events[0][0] < 179:
            line = ringdump.readline()
            continue

        current_generation = [{
            'id': events[0][0],
            'event': event['event'],
            'node': event['node'],
            'time': 0,
            'probability': 1
        }]

        print(current_generation[0])
        print()

        while 1:
            for event in current_generation:
                predict(event)
            current_generation = next_generation
            next_generation = []
            for event in current_generation:
                print(f"{event['probability'] * 100}% {event['event']} at node {event['node']} in {event['time']} ms")
            user_input = input("write 'y' to continue generating events ")
            if user_input != 'y':
                print()
                break

    user_input = input("write 'q' to exit the program ")
    if user_input == 'q':
        break
    
    line = ringdump.readline()

