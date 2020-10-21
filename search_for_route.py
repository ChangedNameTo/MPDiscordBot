import json

def traverse_routes(current_area, query_string):
    return_list = []

    # This is an Area list
    if(current_area['SubAreas'] is not None):
        sub_areas = current_area['SubAreas']['Area']

        if(type(sub_areas) is list):
            for sub_area in sub_areas:
                return_list += traverse_routes(sub_area, query_string)
        else:
            return_list += traverse_routes(sub_areas, query_string)

    # This is a Route List
    elif(current_area['Routes'] is not None):
        routes = current_area['Routes']['Route']

        if(type(routes) is list):
            for route in routes:
                if(route['NameForMatch'] is not None):
                    if (route['NameForMatch'].lower().find(query_string.lower()) != -1):
                        return_list.append(route)
        else:
            if(routes['NameForMatch'] is not None):
                if (routes['NameForMatch'].lower().find(query_string.lower()) != -1):
                    return_list.append(routes)
    
    return return_list

def search_for_routes(search_term):
    query_string = ''.join( e for e in search_term if e.isalnum())

    file_1 = open('1.json','r')
    file_2 = open('2.json','r')

    set_1 = json.load(file_1)
    set_2 = json.load(file_2)

    combined_set = set_1 + set_2

    output_list = []
    for area in combined_set:
        output_list += traverse_routes(area, query_string)

    return output_list