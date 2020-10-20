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
                    if (route['NameForMatch'].find(query_string) != -1):
                        return_list.append(route)
        else:
            if(routes['NameForMatch'] is not None):
                if (routes['NameForMatch'].find(query_string) != -1):
                    return_list.append(routes)
    
    return return_list

def search_for_routes(search_term):
    query_string = ''.join( e for e in search_term if e.isalnum())
    
    with open('routes.json') as json_file:
        data = json.load(json_file)

        output_list = []
        for area in data:
            output_list += traverse_routes(area, query_string)

        # with open('search.json','w') as outfile:
        #     json.dump(output_list, outfile)
        return output_list