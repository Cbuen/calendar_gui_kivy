import json

with open('september.json', 'r') as file:
    calendar_data = json.load(file)


print(calendar_data['busy_days'])