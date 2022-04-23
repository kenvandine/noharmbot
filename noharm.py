import os
import discord
from discord.ext import commands
import random
from dadjokes import Dadjoke
from discordLevelingSystem import DiscordLevelingSystem, RoleAward, LevelUpAnnouncement

bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), intents=discord.Intents(messages=True, guilds=True, members=True))

usage = '''\
Welcome to the NoHarm bot!

Available commands:
    -hello 
    -dadjoke
'''.format(length='multi-line', ordinal='second')

main_guild_id = 918622667211415602 # server ID

my_awards = {
    main_guild_id : [
        RoleAward(role_id=831672678586777601, level_requirement=1, role_name='Rookie'),
        RoleAward(role_id=831672730583171073, level_requirement=2, role_name='Associate'),
        RoleAward(role_id=831672814419050526, level_requirement=3, role_name='Legend')
    ]
}

announcement = LevelUpAnnouncement(f'{LevelUpAnnouncement.Member.mention} just leveled up to level {LevelUpAnnouncement.LEVEL} 😎')

# DiscordLevelingSystem.create_database_file(r'.') # database file already created
lvl = DiscordLevelingSystem(rate=1, per=60.0, awards=my_awards, bot=bot, level_up_announcement=announcement)
lvl.connect_to_database_file(r'./DiscordLevelingSystem.db')

def coinToss():
    flip = random.randint(0, 1)
    if (flip == 0):
        return "Heads"
    else:
        return "Tails"

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(
	help="Uses come crazy logic to determine if pong is actually the correct value or not.",
	brief="Prints pong back to the channel."
)
async def ping(ctx):
	await ctx.channel.send("pong")

@bot.command()
async def rank(ctx):
    print('rank')
    data = await lvl.get_data_for(ctx.author)
    await ctx.send(f'You are level {data.level} and your rank is {data.rank}')

@bot.command()
async def leaderboard(ctx):
    print('leaderboard')
    print(ctx.guild)
    data = await lvl.each_member_data(ctx.guild, sort_by='rank')
    # show the leaderboard whichever way you'd like
    print(data)
    embed = discord.Embed(title=str(ctx.guild) + ' Leaderboard', color=discord.Color.blue())
    for d in data:
        name = ""
        if d.rank == 1:
            name = '🥇 '
        elif d.rank == 2:
            name = '🥈 '
        elif d.rank == 3:
            name = '🥉 '
        name = name + ' ' + str(d.name)
        value = 'Level: ' + str(d.level) + '\nTotal XP: ' + str(d.total_xp)
        embed.add_field(name=name, value=value)
    await ctx.send(embed=embed)

@bot.command()
async def dadjoke(ctx):
    dadjoke = Dadjoke()
    await ctx.channel.send(dadjoke.joke)
    print(dadjoke.joke)
    dadjoke = None

@bot.command()
async def cointoss(ctx):
    await ctx.channel.send(coinToss())

@bot.event
async def on_message(message):
    if message.author == "GitHub#0000":
        print ("GitHub")
        print(str(message.embeds))
        for e in message.embeds:
            print (e.author)
            print ("name: " + e.author.name)
            print ("title: " + e.title)
            #print ("description: " + e.description)
            print (e.type)
            print ("type: " + e.type)
    await lvl.award_xp(amount=15, message=message)
    await bot.process_commands(message)

token = os.getenv('NOHARM_TOKEN')
if token:
  bot.run(token)
else:
  print("NOHARM_TOKEN environment variable required")

