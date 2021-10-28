from discord.ext import tasks, commands
import botTwich
import asyncio
from datetime import datetime

#Discord bot TOken - some secret information!
TOKEN = '***'

#Discord Id's for Guild
GUIDL_ID: int =          1
CHANNEL_EVENTS: int =    2
CHANNEL_GENERAL: int =   3

#Status for piling
STREAM_STATUS: bool = False
STREAM_NAME = 'name'

#Str's
MESSAGE_EVENT: str = 'Стрим онлайн! '
MESSAGE_URL: str = ' https://www.twitch.tv/name'

'''
Implement of part discord bot:

    1. Get token for authentication in init
    2. Await if Streamer is live
        2.a Write status in global VAR
    3. Send respons if streamer is Live 1'st time
        3.a Write status
    4. Check then Srteamer is offline
        4.a Send Respons
        4.b Reduce counter
    5. Go to 2   
'''

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    date = str(datetime.now())
    print(f'{bot.user.name} has connected to Discord! {date}')


@bot.command(name = 'test_1', help = 'I dont now what you want') 
async def test(ctx):
    await ctx.send('Hey, Im BOT!')

'''
TASK 1 - Event discord chat when streamer is live
'''
@tasks.loop(minutes = 2)
async def my_background_task():
    
    global STREAM_STATUS

    result = await botTwich.get_status_streamer_http(STREAM_NAME)

    #If streamer start
    if result['is_live'] and (not STREAM_STATUS):
        #Switch state
        STREAM_STATUS = True
        #Get obj channel
        channel = bot.get_channel(CHANNEL_EVENTS)
        #Check obj channel
        if not channel:
            print('Ups! Channel id is wrong or does not exist.')
            return
        mes = MESSAGE_EVENT + result['title'] + MESSAGE_URL
        await channel.send(mes)
        print(f'Start {datetime.now()}')

    #If streamer stop
    if (not result['is_live']) and STREAM_STATUS:
        #Switch state
        STREAM_STATUS = False
        print(f'Streamer is offline {datetime.now()}')
        
@my_background_task.before_loop
async def before_my_task():
    await bot.wait_until_ready()
    date = str(datetime.now())
    print(f'Task 1 - starting, streamer: {STREAM_NAME}, {date}')
      

if __name__ == '__main__':
    my_background_task.start()
    bot.run(TOKEN)