from random import randint
import praw
def search(subreddit, threshold, number, is_random):
    reddit = praw.Reddit(user_agent='',
                         client_id='',
                         client_secret='',
                         username='', password='')

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
