import json
from datetime import datetime

parsedRingdump = open('parsedRingdump.txt', 'w+')

with open('ringdump.json', 'r') as ringdump:
    event = ringdump.readline()
    count = 1

    while event:
        parsedEvent = json.loads(event)
        if 'time' in parsedEvent:
            parsedEvent['time'] = datetime.utcfromtimestamp(parsedEvent['time']).strftime('%Y-%m-%d %H:%M:%S')

        for key in parsedEvent:
            parsedRingdump.write(f'{key}: {parsedEvent[key]}\n')
        parsedRingdump.write('\n')

        event = ringdump.readline()
        count += 1

parsedRingdump.close()