import json
import collections

with open('routes.json') as json_file:
    with open('1.json') as set_1:
        with open('2.json') as set_2:
            data = json.load(json_file)

            data = data['ArrayOfArea']['Area']

            first_set = json.load(set_1)
            second_set = json.load(set_2)

            new_set = first_set + second_set
