import requests
import aiohttp
import sys
import asyncio

if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

'''
Authentication in Twitch, check secure Id, cecret and token
'''

authURL = 'https://id.twitch.tv/oauth2/token'
client_ID = '***'
secret =    '***'

AutParams = {'client_id': client_ID,
             'client_secret': secret,
             'grant_type': 'client_credentials'
             }

AutCall = requests.post(url=authURL, params=AutParams)
access_token = AutCall.json()['access_token']

head = {
    'Client-ID' : client_ID,
    'Authorization' :  "Bearer " + access_token
    }
    
'''
Sync method
'''
def GetStatusStreamer(StreamerName: str) -> dict: 
    URL = "https://api.twitch.tv/helix/search/channels?query={name}&first=1".format(name = StreamerName)
    answ = requests.get(URL, headers = head).json()
    title: str = answ['data'][0]['title']
    isLive: bool = answ['data'][0]['is_live']
    return {'title': title,
            'is_live': isLive}


'''
Async method
'''
async def get_status_streamer_http(StreamerName: str) -> dict: 
    URL = "https://api.twitch.tv/helix/search/channels?query={name}&first=1".format(name = StreamerName)
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers = head) as req:
            if req.status == 200:
                answ = await req.json()
                title: str = answ['data'][0]['title']
                isLive: bool = answ['data'][0]['is_live']
                return {'title': title,
                        'is_live': isLive}
                
if __name__ == '__main__':
    name = 'name'
    print(GetStatusStreamer(name))
    print(asyncio.run(get_status_streamer_http(name)))
