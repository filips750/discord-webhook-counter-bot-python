import discord
import asyncio
from aiohttp import ClientConnectorError
from datetime import datetime

intents = discord.Intents.all()
client = discord.Client(intents=intents)
token = 'YOUR_TOKEN'


def save_to_csv(filename, list_to_save):
    with open(filename, 'w') as handle:
        for element in list_to_save:
            handle.write(element[0][0]+' '+element[0][1] + '\n')
            handle.write(element[1][0]+' '+element[1][1] + '\n')
            handle.write(element[2][0]+' '+element[2][1] + '\n')
            handle.write(element[3][0]+' '+element[3][1] + '\n')
            handle.write(element[4][0]+' '+element[4][1] + '\n')
            handle.write(element[5][0]+' '+element[5][1] + '\n')
            handle.write(element[6][0]+' '+element[6][1] + '\n')
    print('saved!')


@client.event
async def on_ready():
    prices_to_look_by = ['449 PLN', '453.9 PLN']
    sku = 'NI112N022'
    counter = 0
    channel_id = 0  # YOUR CHANNEL ID HERE
    date1 = '2022-09-31'
    # two lines to check access to the channel
    channel = client.get_channel(channel_id)
    after_date = datetime.fromisoformat(date1)
    messages = [message async for message in channel.history(limit=1500, after=after_date)]
    list_to_return = []
    for msg in messages:
        list_to_append = []
        if msg.reactions and msg.embeds:
            for reaction in msg.reactions:
                if reaction.emoji == '❤️':
                    for one_dict in msg.embeds[0]._fields:
                        to_append = [one_dict.get('name'), one_dict.get('value')]
                        list_to_append.append(to_append)
                    if list_to_append[2][1][:9] == sku:
                        to_check = list_to_append[5][1]  # gets price from list of webhook data
                        if to_check in prices_to_look_by:
                            counter = counter + 1
                        else:
                            print(to_check)
        list_to_return.append(list_to_append)

    print(counter)
    print(len(list_to_return))
    save_to_csv('test.txt', list_to_return)


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(token))
except ClientConnectorError:
    print("Discord connection error try again")
