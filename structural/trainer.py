import json
from datetime import datetime
from databaseHelper import DBConnection

#SQL stuff
db_file = r'../../mecs.db'
connection = DBConnection(db_file)

def property_query(property):
    sql_query = f"""SELECT ROWID, * FROM properties WHERE type = '{property['type']}' AND value = '{property['value']}';"""
    return connection.execute_query(sql_query)

def property_insert(property):
    sql_insert = f"""INSERT INTO properties (type, value) VALUES ('{property['type']}', '{property['value']}');"""
    connection.execute_statement(sql_insert)

def relation_query(property1, property2):
    sql_query = f"""SELECT * FROM property_relations WHERE cause = {property1['id']} AND effect = {property2['id']}"""
    return connection.execute_query(sql_query)

def relation_insert(property1, property2):
    time_dif = int(property2['time'] - property1['time'])

    sql_insert = f"""INSERT INTO property_relations (cause, effect, count, time_average) VALUES ({property1['id']}, {property2['id']}, 1, {time_dif})"""
    connection.execute_statement(sql_insert)

def relation_update(property1, property2, relation):
    count = relation[2]
    time_average = relation[3]

    time_dif = int(property2['time'] - property1['time'])
    time_average = time_average / (count + 1) * count + time_dif / (count + 1)
    count += 1

    relation_update = f"""UPDATE property_relations SET count = {count}, time_average = {time_average} WHERE cause = {property1['id']} AND effect = {property2['id']};"""
    connection.execute_statement(relation_update)

ringdump = open('../../ringdump.json', 'r')

#read the first event
line = ringdump.readline()
event = json.loads(line)
while ('time' not in event):
    line = ringdump.readline()
    event = json.loads(line)
    continue

total_events = 1
last_properties = []

for key in event:
    if key in ['time', '_id']:
        continue

    property = {
        'type': key,
        'value': event[key],
        'time': float(event['time'])
    }

    properties = property_query(property)
    if len(properties) == 0:
        property_insert(property)
        properties = property_query(property)

    property['id'] = properties[0][0]

    last_properties.append(property)

line = ringdump.readline()

while line and (total_events <= 1000):
    event = json.loads(line)

    #if event is incomplete, ignore it
    if ('time' not in event):
        line = ringdump.readline()
        continue

    total_events += 1
    current_properties = []

    for key in event:
        if key in ['time', '_id']:
            continue

        property = {
            'type': key,
            'value': event[key],
            'time': float(event['time'])
        }

        #insert or fetch property
        properties = property_query(property)
        if len(properties) == 0:
            property_insert(property)
            properties = property_query(property)

        property['id'] = properties[0][0]

        for last_property in last_properties:
            if last_property['type'] == property['type']:
                #insert or update relation between this property and the last
                relations = relation_query(last_property, property)
                if len(relations) == 0:
                    relation_insert(last_property, property)
                else:
                    relation_update(last_property, property, relations[0])
                break

        current_properties.append(property)

    last_properties = current_properties
    line = ringdump.readline()

ringdump.close()
            