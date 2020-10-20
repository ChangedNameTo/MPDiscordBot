import discord
import json
import random
import requests


from discord.ext import commands

from secrets import token, mp_key
from search_for_route import search_for_routes

description = 'A bot for use in the Climbing discord'
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Bot is ready and live')
    print('=====================')

@bot.command(description='Lists a route', help="Takes a route name as the argument and prints out the route with the matching name")
async def route(ctx, route_name):
    print('Route Name: {}, Requester: {}'.format(route_name,ctx.author))
    print('Searching for route')

    routes = search_for_routes(route_name)
    found = len(routes)
    print('Found: {}'.format(found))

    if(found == 0):
        await ctx.send('Did not find any routes with that name.')
        return 

    # Shortcut
    route = routes[0]

    # Embed Creation
    title = '{}'.format(route['Name'])

    route_type = route['Types']['RouteType']
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

    embed = discord.Embed(title=title, color=color, url=mp_api_data['url'])

    embed.add_field(name='Area', value=area, inline=False)
    embed.add_field(name='Grade', value=grade_string, inline=False)
    embed.add_field(name='Type', value=route_type, inline=False)
    embed.add_field(name='Rating', value='{}/5'.format(rating), inline=False)
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text='Type `?route <name>` to search for routes')

    await ctx.send(content=None, embed=embed)

@bot.command(description='Gives you an excuse', help='Punt easier than ever before')
async def punt(ctx):
    excuses = [
        "Can't send in these condis",
        "It's a high gravity day",
        "I tweaked my finger in the gym",
        "Never can know with those 5.9+ routes at the Gunks",
        "This is sandbagged",
        "v3+ in my gym",
        "This is a 5.12 in yosemite",
        "This is an oldschool area, the grades are sandbagged",
        "This is a 5.13 in RRG",
        "It was too crowded to send",
        "Can’t send with people watching",
        "My skin is too thin",
        "My calluses are too thick",
        "I didn’t get enough sleep last night",
        "A bird laughed at me menacingly",
        "Bell’s Palsy",
        "blew a shoe",
        "bolts are bad",
        "Choss",
        "Dogfight!",
        "forgot rope",
        "Hair tie broke",
        "hangers fell off",
        "hangers made of climbing chalk",
        "Harder then V2",
        "hate roofs",
        "hate slab",
        "hold broke",
        "huh?",
        "I didn't drink enough last night",
        "I didn’t have my protein shake",
        "I didn’t want to get too tired",
        "I didn’t want to polish the holds",
        "I didn’t want to resort to trying hard and swearing profusely",
        "I didn’t want to show up my mate",
        "I don’t climb well on Wednesdays",
        "I drank too much last night",
        "I have too high bone density",
        "I have too low bone density",
        "I got grit rash",
        "I grabbed the wrong pocket",
        "I just slipped",
        "I rested too little yesterday",
        "I wanted to do a practice fall",
        "I wanted to take the big whip",
        "I was wearing too many layers",
        "I’m due to peak in a week’s time",
        "I’m more of a boulderer",
        "I’m more of a trad climber",
        "I’m past my physical prime",
        "I’m too old",
        "I’m too young",
        "It's snowing...",
        "it's too humid",
        "it's too steep",
        "it's way harder 'cause I suck",
        "it's way harder 'cause I'm tall",
        "It’s a high gravity day",
        "magnesium on holds",
        "My arms are too short",
        "My arms are too weak",
        "My belayer farted",
        "My feet are achy",
        "my fingertips were bleeding",
        "My hair blew in my face",
        "My lycra was so bright it dazzled me",
        "My mate put a brick in my chalkbag",
        "My mum told me to come down",
        "My phone rang",
        "My shoes are too old",
        "My shoes were dirty",
        "no chalk",
        "Nor any day ending in a ‘y’",
        "Not a V2",
        "not on my ticklist",
        "not psyched on that style of climbing",
        "People were shouting “Allez!”",
        "project",
        "Rockfax told me to go the wrong way…",
        "route wasn't a gem",
        "Scottland. You know.",
        "shoe lace broke",
        "sketchy",
        "Slopers aren’t my forte",
        "Someone on UKC said it was “tough for the grade.”",
        "split tip",
        "squamish",
        "The ambience wasn’t right",
        "The best climber is the one having most fun…and I wasn’t having fun…",
        "The crag was too busy",
        "The friction coefficient was less than ideal",
        "The light was flat",
        "the perma-draws were manky",
        "The route has clearly changed",
        "The route was rubbish",
        "The route wasn’t in season",
        "The route wasn’t my style",
        "The wind changed direction",
        "There was a bird",
        "There was a spider",
        "There were no holds.",
        "They don't allow dogs at that crag anymore",
        "The tires flat on the rig",
        "I tweaked a finger",
        "I was high"
    ]

    await ctx.send(random.choice(excuses))

# Run the bot
bot.run(token)