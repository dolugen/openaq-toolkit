#!/usr/bin/env python3

import sys
import json
from datetime import datetime

'''
A sample line:
{
  "date": {
    "utc": "2020-06-05T23:30:00.000Z",
    "local": "2020-06-06T04:00:00+04:30"
  },
  "parameter": "pm25",
  "value": 22,
  "unit": "µg/m³",
  "averagingPeriod": {
    "value": 1,
    "unit": "hours"
  },
  "location": "US Diplomatic Post: Kabul",
  "city": "Kabul",
  "country": "AF",
  "coordinates": {
    "latitude": 34.535812,
    "longitude": 69.190514
  },
  "attribution": [
    {
      "name": "EPA AirNow DOS",
      "url": "http://airnow.gov/index.cfm?action=airnow.global_summary"
    }
  ],
  "sourceName": "StateAir_Kabul",
  "sourceType": "government",
  "mobile": false
}
'''

measurement_name = 'aq_measurement'
tagset_headers = 'location,city,country,parameter,unit'.split(',')
fieldset_headers = 'value'.split(',')

# Note: Similar to csv2lineprotocol but slightly different
# because JSON contains nested fields like date and coordinates
for line in sys.stdin:
    row = json.loads(line)
    tagset = []
    fieldset = []
    for tag_name in tagset_headers:
        tag_value = row[tag_name].replace(' ', '\ ')
        tagset.append(f'{tag_name}={tag_value}')
    for field_name in fieldset_headers:
        fieldset.append(f'{field_name}={row[field_name]}')

    timestamp = datetime.strptime(row['date']['utc'], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
    timestamp = int(timestamp) * 1_000_000_000  # to nanoseconds

    line = f'{measurement_name},{",".join(tagset)} {",".join(fieldset)} {timestamp}'
    print(line)