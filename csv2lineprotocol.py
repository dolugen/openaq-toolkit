#!/usr/bin/env python3

import sys
import csv
from datetime import datetime

tagset_headers = 'location,city,country,parameter,unit,latitude,longitude'.split(',')
fieldset_headers = 'value'.split(',')

measurement_name = 'aq_measurement'

reader = csv.DictReader(sys.stdin)
for row in reader:
    tagset = []
    fieldset = []
    for tag_name in tagset_headers:
        tag_value = row[tag_name].replace(' ', '\ ')
        tagset.append(f'{tag_name}={tag_value}')
    for field_name in fieldset_headers:
        fieldset.append(f'{field_name}={row[field_name]}')
    
    timestamp = datetime.strptime(row['utc'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    timestamp = int(timestamp) * 1_000_000_000  # to nanoseconds

    line = f'{measurement_name},{",".join(tagset)} {",".join(fieldset)} {timestamp}'
    print(line)
