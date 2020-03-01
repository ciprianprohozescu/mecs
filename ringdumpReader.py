import json
from datetime import datetime

keys = []
key_names = []
totalEvents = 0

print()
print()

with open('../ringdump.json', 'r') as ringdump:
    line = ringdump.readline()

    while line and totalEvents <= 50000:
        event = json.loads(line)

        for key in event:
            if key == '_id':
                continue
            if key in key_names:
                index = key_names.index(key)
                keys[index]['appearances'] += 1
                if event[key] not in keys[index]['values']:
                    keys[index]['values'].append(event[key])
            else:
                key_names.append(key)
                keys.append({
                    'name': key,
                    'appearances': 1,
                    'values': [event[key]]
                })

        line = ringdump.readline()
        totalEvents += 1

for key in keys:
    percentile = float(key['appearances']) / totalEvents * 100.0
    name = key['name']
    valuesNo = len(key['values'])

    print(f'{name} ({percentile}%): ', end = '')

    if valuesNo > 10:
        print(f'{valuesNo} values')
    else:
        for value in key['values']:
            print(value, end = ' ')
        print()
    print()

print()
print()
