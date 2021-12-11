import os
import discord
import random
from dadjokes import Dadjoke

client = discord.Client()

usage = '''\
Welcome to the NoHarm bot!

Available commands:
    -hello 
    -dadjoke
'''.format(length='multi-line', ordinal='second')

def coinToss():
    flip = random.randint(0, 1)
    if (flip == 0):
        return "Heads"
    else:
        return "Tails"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('-dadjoke'):
        dadjoke = Dadjoke()
        await message.channel.send(dadjoke.joke)
        print(dadjoke.joke)
        dadjoke = None
    if message.content.startswith('-help'):
        await message.channel.send(usage)

    if message.content.startswith('-coinflip'):
        await message.channel.send(coinToss())

token = os.getenv('NOHARM_TOKEN')
if token:
  client.run(token)
else:
  print("NOHARM_TOKEN environment variable required")

