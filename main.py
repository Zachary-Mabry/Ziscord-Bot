"""
This class is the main class responsible for functions of the bot
"""
import opus
import configs
import discord
import decrequest
import prawbot
import memetype
import songs
import asyncio
import urllib.parse
import urllib.request
import bs4
import pafy
from discord.ext.commands import Bot

'''
Globals
'''
# TODO: possibly handle globals better
player = None
current = ""
count = 0
main_queue = []
auto = []
voice = None
skipsong = False
opts = {
    'default_search':'auto',
    'quiet': True,
}

'''
Initializing stuff
'''
VOICE_CHANNEL_ID = configs.VOICE_CHANNEL_ID
bot = Bot(command_prefix=configs.COMMAND_PREFIX)  # sets the prefix to each command (e.g. !hello)
token = configs.BOT_TOKEN  # Token used by Discord for the bot
opus.load_opus_lib()
async def load_voice_channel():
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    voice = await bot.join_voice_channel(voice_channel)
    print('Bot joined voice channel. ID: {}'.format(VOICE_CHANNEL_ID))


'''
Post-initialization behavior
'''
@bot.event
async def on_ready():
    print("Client logged in")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    await load_voice_channel()
    await load_auto_playlist()
    await start_player()


'''
Loads the automatic playlist from "auto-playlist.txt"
'''
async def load_auto_playlist():
    global auto
    with open("auto-playlist.txt") as list:
        content = list.readlines()
    auto = [x.strip() for x in content]\


'''
Fun text modifier that turns the input into regional indicator emoji
'''
@bot.command(pass_context=True)
async def emoji(args, left):
    msg = memetype.meme(args.message.content[6::])
    for mesg in msg:
        print(len(msg))
        if len(mesg) > 2000:
            await bot.say("Too long, didn't meme.")
        else:
            await bot.say(mesg)


'''
Reddit scraper, returns links to reddit posts

subreddit = the subreddit name (e.g. r/UIUC would be "UIUC")
threshold = the upvote threshold (e.g. 10 returns posts with over 10 upvotes)
number = the number of links to return, which are printed by the bot
'''
@bot.command(pass_context=True)
async def reddit(args, subreddit, threshold, number):
    try:
        msg = prawbot.search(subreddit, threshold, number, False)
        for lines in msg:
            await bot.say(lines)
    except:
        return


'''
Wrapper for the reddit scraper that returns a random post from the top 50 posts of r/dankmemes
'''
@bot.command(pass_context=True)
async def meme(args):
    try:
        msg = prawbot.search("dankmemes", "0", 50, True)
        await bot.say(msg)
    except:
        return


'''
Converts the input into dectalk text-to-speech.
'''
@bot.command(pass_context=True)
async def tts(args):
    await speak(args.message.content[4::])
    await bot.say(":full_moon: :house:")


'''
Wrapper of sorts for the tts command that makes the bot sing a random song
'''
@bot.command(pass_context=True)
async def sing(args):
    song = songs.get_song()
    await speak(song)
    await bot.say(":notes:")


'''
Adds a song to the queue by searching youtube for the input.
'''
@bot.command(pass_context=True)
async def play(args):
    global main_queue
    link = args.message.content[6::]
    result = await search(link)
    print(result)
    print("Searched")
    main_queue.append(result)
    print("Appended")
    info = await get_vid_info(result)
    await bot.say("Added " + info['title'])


'''
Displays information about the current song
'''
@bot.command(pass_context=True)
async def nowplaying(args):
    global current
    info = await get_vid_info(current)
    duration = info['duration']
    time = await get_time_as_string(duration)
    message = "```"
    message += "Now Playing: " + str(info['title']) + "\n"
    message += "Duration:    " + time + "\n"
    message += "Uploaded By: " + str(info['author']) + "\n"
    message += "Uploaded On: " + str(info['date']) + "```"
    await bot.say(message)


'''
Displays the queue of songs ready to be played
'''
@bot.command(pass_context=True)
async def queue(args):
    global main_queue
    message = "```"
    pos = 1
    print(len(main_queue))
    for i in range(0, len(main_queue)):
        info = await get_vid_info(main_queue[i])
        duration = info['duration']
        time = await get_time_as_string(duration)
        message += (str(pos) + ".) " + str(info['title']) + " " + "[" + time + "]" + "\n")
        pos += 1
    message += "```"
    await bot.say(message)


'''
Displays the auto-queue of songs
'''
@bot.command(pass_context=True)
async def auto(args):
    global auto
    message = "```"
    pos = 1
    print(len(auto))
    for i in range(0, len(auto)):
        info = await get_vid_info(auto[i])
        duration = info['duration']
        time = await get_time_as_string(duration)
        message += (str(pos) + ".) " + str(info['title']) + " " + "[" + time + "]" + "\n")
        pos += 1
    message += "```"
    await bot.say(message)

'''
Takes an integer number of seconds, and returns a string to display for the time in hours:minutes:seconds format
'''
async def get_time_as_string(time):
    if time < 3600:
        minutes = str(int(time / 60))
        seconds = str(int(time % 60))
        if int(seconds) <= 9:
            seconds = "0" + seconds
        return minutes + ":" + seconds
    else:
        hours = str(int(time / 3600))
        time = time - 3600*int(hours)
        minutes = str(int(time / 60))
        seconds = str(int(time % 60))
        if seconds <= "9":
            seconds = "0" + seconds
        return hours + ":" + minutes + ":" + seconds


'''
Helper function for tts command that grabs the sound file from a web application
'''
async def speak(script):
    server = discord.Server(id=configs.SERVER_ID)
    voice = bot.voice_client_in(server)
    decrequest.talk(script)
    player = voice.create_ffmpeg_player('dectalk.wav')
    print("HELLO!")
    player.start()


'''
Initializes the music player
'''
async def start_player():
    global player
    global main_queue
    global auto
    global voice
    global current
    before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    server = discord.Server(id=configs.SERVER_ID)
    voice = bot.voice_client_in(server)
    player = await voice.create_ytdl_player(auto[0], ytdl_options=opts, before_options=before_args)
    gname_main = await get_vid_info(auto[0])
    gname = gname_main['title']
    await bot.change_presence(game=discord.Game(name=gname))
    current = auto[0]
    auto.pop(0)
    player.start()


'''
Skips the current song
'''
@bot.command(pass_context=True)
async def skip():
    global player
    global main_queue
    global auto
    global voice
    global opts
    global current
    player.stop()
    player = None
    before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    if not len(main_queue) == 0:
        next = main_queue[0]
        current = next
        main_queue.pop(0)
    elif not len(auto) == 0:
        next = auto[0]
        current = next
        auto.pop(0)
    else:
        next = "https://www.youtube.com/watch?v=O8EzbKWaUpQ"
        current = next
    player = await voice.create_ytdl_player(next, ytdl_options=opts, before_options=before_args)
    gname_main = await get_vid_info(next)
    gname = gname_main['title']
    await bot.change_presence(game=discord.Game(name=gname))
    player.start()


'''
Pauses the current song
'''
@bot.command(pass_context=True)
async def pause():
    global player
    global main_queue
    global auto
    global voice
    player.pause()


'''
Resumes the paused song
'''
@bot.command(pass_context=True)
async def resume():
    global player
    global main_queue
    global auto
    global voice
    player.resume()


'''
Loop that runs once per second to check if the current song has ended, moving on to the next song when necessary
'''
async def check_player():
    global player
    global main_queue
    global auto
    global voice
    global opts
    global count
    global current
    before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    await bot.wait_until_ready()
    while not bot.is_closed:
        if player is not None:
            if player.is_done():
                player.stop()
                player = None
                if not len(main_queue) == 0:
                    next = main_queue[0]
                    current = next
                    main_queue.pop(0)
                elif not len(auto) == 0:
                    next = auto[0]
                    current = next
                    auto.pop(0)
                else:
                    next = "https://www.youtube.com/watch?v=O8EzbKWaUpQ"
                    current = next
                player = await voice.create_ytdl_player(next, ytdl_options=opts, before_options=before_args)
                gname_main = await get_vid_info(next)
                gname = gname_main['title']
                await bot.change_presence(game=discord.Game(name=gname))
                player.start()
        await asyncio.sleep(1)


'''
Searches youtube for the input, returns a link to the video to be played
'''
async def search(search_query):
    query = urllib.parse.quote(search_query)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    find = soup.findAll(attrs={'class':'yt-uix-tile-link'})
    if "googleads" in find[0]['href']:
        return "https://www.youtube.com" + find[1]['href']
    return "https://www.youtube.com" + find[0]['href']


'''
Parses information about the video located at the input link
'''
async def get_vid_info(url):
    video = pafy.new(url)
    info = {}
    info['duration'] = video.length
    info['title'] = video.title
    info['author'] = video.author
    info['date'] = video.published
    return info


'''
Handles errors
'''
@bot.event
async def on_command_error(error, ctx):
    print(error)
    # TODO: print helpful error messages
    # bot.send_message(ctx.message.channel, help.get_help(ctx.invoked_with))

bot.loop.create_task(check_player())
bot.run(token)

