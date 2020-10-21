import json

with open('routes.json') as json_file:
    data = json.load(json_file)

    data = data['ArrayOfArea']['Area']

    first_set = data[:25]
    second_set = data[25:]

    with open('1.json','w') as outfile:
        json.dump(first_set,outfile)
    with open('2.json','w') as outfile:
        json.dump(second_set,outfile)
