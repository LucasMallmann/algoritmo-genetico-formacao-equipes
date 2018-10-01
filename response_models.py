import json

with open('results.json', 'r') as j:
    data = json.load(j)

print(data)
