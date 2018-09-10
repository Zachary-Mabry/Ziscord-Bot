import urllib.request
import json
from twitch import TwitchClient
def check_online(name):
    """
    0 = isStreaming
    1 = game
    2 = status
    3 = thumbnail
    """
    ret = []
    url = 'https://api.twitch.tv/kraken/streams/' + name
    req = urllib.request.Request(url)
    req.add_header("Client-ID", "")
    resp = urllib.request.urlopen(req)
    data = resp.read().decode('utf-8')
    j = json.loads(data)
    if j['stream'] is None:
        ret.append(False)
        return ret
    else:
        ret.append(True)
    ret.append(j['stream']['game'])
    ret.append(j['stream']['channel']['status'])
    ret.append(j['stream']['preview']['large'])
    print(ret)
    return ret
