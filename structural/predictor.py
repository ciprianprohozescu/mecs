import json
import copy
from databaseHelper import DBConnection

current_generation = {}
next_generation = {}

#SQL stuff
db_file = r'../../mecs.db'
connection = DBConnection(db_file)

def property_query(property):
    sql_query = f"""SELECT ROWID, * FROM properties WHERE type = '{property['type']}' AND value = '{property['value']}';"""
    return connection.execute_query(sql_query)

def related_properties_query(property):
    sql_query = f"""SELECT * FROM property_relations
    JOIN properties on property_relations.effect = properties.rowid
    WHERE property_relations.cause = {property['id']}"""
    return connection.execute_query(sql_query)

#retrieve and calculate probabilities for all properties caused by a given property
def predict(property):
    results = []
    total_relations = 0

    related_properties = related_properties_query(property)

    for related_property in related_properties:
        results.append({
            'id': related_property[1],
            'type': related_property[4],
            'value': related_property[5],
            'probability': related_property[2],
            'time': related_property[3]
        })
        total_relations += related_property[2]

    for result in results:
        result['probability'] = property['probability'] * result['probability'] / total_relations

    return results

#read event from test file
testEvent = open('testEvent.json', 'r')
event = json.load(testEvent)

for key in event:
    if key in ['time', '_id']:
        continue
    
    property = {
        'type': key,
        'value': event[key],
        'probability': 1,
        'time': 0
    }
    properties = property_query(property)
    if len(properties) == 0:
        continue
    property['id'] = properties[0][0]
    print(property)
    print()
    print()
    current_generation[key] = [property]

while True:
    for key in current_generation:
        next_generation[key] = []

        for property in current_generation[key]:
            next_generation[key] += predict(property)
        
        print(f"{key}: ")
        for property in next_generation[key]:
            print(f"{property['value']} ({property['probability'] * 100}%, {property['time']} ms)")
        print()
        print()
        print()
    
    current_generation = copy.deepcopy(next_generation)
    user_input = input("write 'y' to continue generating properties ")
    if user_input != 'y':
        break