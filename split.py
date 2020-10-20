import json

with open('routes.json') as json_file:
    data = json.load(json_file)
    with open('bama.json','w') as outfile:
        json.dump(data[0],outfile)
