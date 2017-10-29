import praw
from random import randint

def search(subreddit, threshold, number, is_random):
    reddit = praw.Reddit(user_agent='Reddit2Discord',
                         client_id='HLpsvjgVg0e8Kg',
                         client_secret='gFImjBbEXMQvZvOGdsr-5rbYqL4',
                         username='zekyriah', password='z99293111')

    threshhold = int(threshold)
    out = ""
    outs = []
    submissions = reddit.subreddit(subreddit).hot(limit=50)
    count = 0
    post = randint(0, 49)
    for item in submissions:
        if item.score > threshhold:
            out += item.url + "\n"
            count += 1
        if count % 5 == 0:
            outs.append(out)
            out = ""
        if count == int(number):
            outs.append(out)
            break
        if is_random is True and count == post:
            return "" + item.url
    return outs
