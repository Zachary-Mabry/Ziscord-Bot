import urllib.request
import shutil
import wavstream
from urllib.parse import quote
from random import randint

def talk(phrase):
    phrase = format_for_url(phrase)
    req = urllib.request.Request(
        'https://talk.moustacheminer.com/api/gen?dectalk=' + phrase,
        data=None,
        headers={
            'User-Agent': getuser()
        }
    )
    with urllib.request.urlopen(req) as response, open('dectalk.wav', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

def format_for_url(phrase):
    phrase = quote(phrase)
    return phrase


def getuser():
    id = randint(0, 9)
    if id == 0:
        return 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    elif id == 1:
        return 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0'
    elif id == 2:
        return 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Media Center PC'
    elif id == 3:
        return 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    elif id == 4:
        return 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1'
    elif id == 5:
        return 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    elif id == 6:
        return 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    elif id == 7:
        return 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    elif id == 8:
        return 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    elif id == 9:
        return 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
