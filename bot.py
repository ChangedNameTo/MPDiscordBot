import discord
import json
import random
import requests
import sys, traceback
import os

from datetime import timedelta, datetime
from discord.ext import commands

from excuses import excuses

from search_for_route import search_for_routes

description = 'A bot for use in the Climbing discord'
bot = commands.Bot(command_prefix='?', description=description)
bot_name = 'MP Discord Bot#9416'

from secrets import token, mp_key
# mp_key = os.environ['mp_key']
# token = os.environ['token']

embed_dict = {}
ALLOWED_SYSTEMS = ['Hueco', 'Fontainebleau', 'YDS', 'British', 'French']

@bot.event
async def on_ready():
    print('Bot is ready and live')
    print('=====================')

@bot.command(description='Lists a route', help="Takes a route name as the argument and prints out the route with the matching name")
async def route(ctx, route_name):
    # Let them know this is workin
    await ctx.message.add_reaction('\U000023F3')

    print('Route Name: {}, Requester: {}'.format(route_name, ctx.author))
    print('Searching for route')

    routes = search_for_routes(route_name)
    found = len(routes)
    print('Found: {}'.format(found))

    if(found == 0):
        await ctx.send('Did not find any routes with that name.')
        return
    elif(found == 1):
        route = routes[0]

        # Embed Creation
        title = '{}'.format(route['Name'])

        rating = route['Rating']
        route_id = route['ID']

        r = requests.get("https://www.mountainproject.com/data/get-routes?routeIds={}&key={}".format(route_id, mp_key))

        mp_api_data = r.json()['routes'][0]
        thumbnail = mp_api_data['imgMedium']
        area = ' -> '.join(mp_api_data['location'])
        route_url = mp_api_data['url']
        pitches = mp_api_data['pitches']

        # Pulls the grade info
        grade_string = '|'
        grades = route['Grades']['Grade']
        if type(grades) is list:
            for grade in grades:
                if grade['System'] in ALLOWED_SYSTEMS:
                    grade_string += ' `{}` |'.format(grade['Value'])
        else:
            grade_string = '| `{}`| '.format(grades['Value'])

        route_type = route['Types']['RouteType']
        if type(route_type) is list:
            route_type_text = ', '.join(route_type)
        else:
            route_type_text = '| `{}` | '.format(route_type)

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

        # Removes the hourglass
        await ctx.message.clear_reactions()

        embed = discord.Embed(title=title, color=color, url=mp_api_data['url'], timestamp=datetime.now().replace(microsecond=0))

        embed.add_field(name='Area', value=area, inline=False)
        embed.add_field(name='Grade', value=grade_string, inline=False)
        embed.add_field(name='Type', value=route_type_text, inline=False)
        if(pitches):
            embed.add_field(name='Pitches', value=pitches, inline=False)
        embed.add_field(name='Rating', value='{}/5'.format(rating), inline=False)
        embed.set_author(name=ctx.author)
        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text='Type `?route "<name>"` to search for routes')

        await ctx.send(content=None, embed=embed)

    # User needs to pick
    else:
        # Removes the hourglass
        await ctx.message.clear_reactions()

        # Embed Creation
        title = 'Results for {} (Showing {} of {})'.format(route_name, 10, len(routes))
        color = 0xFFFFFF

        # Slices the list since pagination is hard
        routes = routes[:10]

        embed = discord.Embed(title=title, color=color, timestamp=datetime.now().replace(microsecond=0))

        route_ids = ','.join([route['ID'] for route in routes])
        r = requests.get("https://www.mountainproject.com/data/get-routes?routeIds={}&key={}".format(route_ids, mp_key))
        mp_api_data = r.json()['routes']

        # Creates the emoji list
        emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(0, len(routes))]

        # We need to add in the MP data so that as soon as a route is selected, we can print the route data
        for ind, route in enumerate(routes):
            route['image'] = mp_api_data[ind]['imgMedium']
            route['area'] = ' -> '.join(mp_api_data[ind]['location'])
            route['url'] = mp_api_data[ind]['url']
            route['pitches'] = mp_api_data[ind]['pitches']

            route_text = '[{} ({})]({})\n'.format(route['Name'], route['area'], route['url'])

            embed.add_field(name='{}'.format(emojis[ind]), value=route_text, inline=False)

        # Set the implicit fields
        embed.set_author(name=ctx.author)
        embed.set_footer(text='Use the reactions to select the route. The developer sucks so this cuts off at 10 results.')

        # Sends the embed
        message = await ctx.send(content=None, embed=embed)

        # Stores the timestamp so I can check against it later
        embed_dict[embed.timestamp] = routes

        # Attaches the emojis
        for emoji in emojis:
            await message.add_reaction(emoji)


@bot.command(description='Gives you an excuse', help='Punt easier than ever before')
async def punt(ctx):
    await ctx.send(random.choice(excuses))

# Pagination for the embeds
@bot.event
async def on_reaction_add(reaction, user):
    # Is this an embed?
    if(len(reaction.message.embeds) == 0):
        return

    # We only care if this embed is a route selection embed
    # These are all cached in the embed_dict
    embed = reaction.message.embeds[0]

    # Pull the route list from the embed dictionary
    if(embed.timestamp not in embed_dict.keys()):
        return

    # If this isn't one of the selection embeds, it should have exited by now

    routes = embed_dict[embed.timestamp]

    reactants = [(i.name+'#'+i.discriminator) for i in await reaction.users().flatten()]

    if embed.author.name in reactants:
        index = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in range(0, len(routes))].index(reaction.emoji)

        # Did they add a valid reaction?
        if index == -1:
            await reaction.remove(user)
            return

        route = routes[index]

        # Embed Creation
        title = '{}'.format(route['Name'])

        rating = route['Rating']
        route_id = route['ID']

        grade_string = '|'
        grades = route['Grades']['Grade']

        if type(grades) is list:
            for grade in grades:
                if grade['System'] in ALLOWED_SYSTEMS:
                    grade_string += ' `{}` |'.format(grade['Value'])
        else:
            grade_string = '| `{}` | '.format(grades['Value'])

        # Pulls the route type information
        route_type = route['Types']['RouteType']
        if type(route_type) is list:
            route_type_text = ', '.join(route_type)
        else:
            route_type_text = '| `{}` | '.format(route_type)

        if type(route_type) is list:
            route_type = route_type[0]

        # Changes the embed color based on route type
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

        embed = discord.Embed(title=title, color=color, url=route['url'], timestamp=datetime.now().replace(microsecond=0))
        embed.clear_fields()

        embed.add_field(name='Area', value=route['area'], inline=False)
        embed.add_field(name='Grade', value=grade_string, inline=False)
        embed.add_field(name='Type', value=route_type_text, inline=False)
        if(route['pitches']):
            embed.add_field(name='Pitches', value=route['pitches'], inline=False)
        embed.add_field(name='Rating', value='{}/5'.format(rating), inline=False)
        embed.set_thumbnail(url=route['image'])
        embed.set_footer(text='Type `?route "<name>"` to search for routes')

        await reaction.message.clear_reactions()
        await reaction.message.edit(embed=embed)
    else:
        if(user.name+'#'+user.discriminator != bot_name):
            await reaction.remove(user)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.DisabledCommand):
        await ctx.send(ctx.message.author, "I'm Sorry. This command is disabled and it can't be used.")
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(ctx.message.channel, "It seems you are trying to use a command that does not exist.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("It seems you are missing required argument(s). Try again if you have all the arguments needed.")
    elif isinstance(error, KeyError):
        await ctx.send("This is a KeyError cause @TheAlpacalypse#8105 is an idiot.")

# Run the bot
bot.run(token)
