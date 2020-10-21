import discord
import requests

from secrets import mp_key

def create_route_embed(route, requestor):
    # Embed Creation
    title = '{}'.format(route['Name'])

    rating = route['Rating']
    route_id = route['ID']

    r = requests.get("https://www.mountainproject.com/data/get-routes?routeIds={}&key={}".format(route_id, mp_key))
    mp_api_data = r.json()['routes'][0]
    thumbnail = mp_api_data['imgMedium']
    area = ' -> '.join(mp_api_data['location'])
    route_url = mp_api_data['url']

    grade_string = '|'
    for grade in route['Grades']['Grade']:
        grade_string += ' `{}` |'.format(grade['Value'])
    
    route_type = route['Types']['RouteType']
    route_type_text = ', '.join(route_type)

    if type(route_type) is list:
        route_type = route_type[0]

    if route_type == 'Boulder':
        color = 0x109618
    elif route_type == 'Sport':
        color = 0xDC3912
    elif route_type == 'Trad':
        color = 0x3366CC
    elif route_type == 'Toprope':
        color = 0xFF9900
    else:
        color = 0xFFFFFF

    embed = discord.Embed(title=title, color=color, url=mp_api_data['url'])

    embed.add_field(name='Area', value=area, inline=False)
    embed.add_field(name='Grade', value=grade_string, inline=False)
    embed.add_field(name='Type', value=route_type_text, inline=False)
    embed.add_field(name='Rating', value='{}/5'.format(rating), inline=False)
    embed.set_author(name=requestor)
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text='Type `?route <name>` to search for routes')

    return embed

def create_selection_embed(route_name, routes, requestor):
    # Embed Creation
    title = 'Results for {}'.format(route_name)
    color = 0xFFFFFF

    embed = discord.Embed(title=title, color=color)


    route_ids = ','.join([route['id'] for route in routes])
    print(route_id)

    r = requests.get("https://www.mountainproject.com/data/get-routes?routeIds={}&key={}".format(route_ids, mp_key))
    
    embed.set_author(name=requestor)
    embed.set_footer(text='Use the reactions to select the route')

    return embed