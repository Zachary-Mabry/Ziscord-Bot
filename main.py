"""
This class is the main class responsible for functions of the bot
"""
import os
import glob
import configs
import opus
import prawbot
import memetype
import songs
import asyncio
import aiohttp
import urllib.parse
import urllib.request
import bs4
import pafy
import dice
import discord
import decrequest
import subprocess
import stream_check
from random import shuffle
from discord.ext.commands import Bot

'''
Globals
'''
# TODO: possibly handle globals better
player = None
auto_file = "default.txt"
streamer_file = "streamers.txt"
current = ""
count = 0
main_queue = []
auto = []
voice = None
skipsong = False
pp = False
started = False
total_time = 0
time_since = 0
state = "NULL"
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
    global voice
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
Loads the current active automatic playlist
'''
async def load_auto_playlist():
    global auto
    global auto_file
    with open(auto_file) as list:
        content = list.readlines()
        auto = [x.strip() for x in content]
        shuffle(auto)
        list.close()

'''
Checks that the given user can use the command
'''
async def check_permissions(user, is_admin_cmd):
    rids = [role.id for role in user.roles]
    for user_role_id in rids:
        if user_role_id == configs.ADMIN_ROLE_ID:
            return True
        if is_admin_cmd:
            continue
        for rid in configs.WHITELISTED_ROLE_LIST:
            if user_role_id == rid:
                return True
    return False
'''
Add to an auto list
'''
@bot.command(pass_context=True)
async def add(args, file, line):
    if await check_permissions(args.message.author, True) is False:
        return
    index = 6 + len(file)
    filename = file + ".txt"
    with open(filename, "a+") as playlist:
        content = args.message.content[index::]
        link = await search(content)
        if os.stat(filename).st_size == 0:
            playlist.write(link)
        else:
            playlist.write("\n" + link)
        playlist.close()
    await bot.say("Added song to playlist")

'''
Remove an autoplaylist
'''
@bot.command(pass_context=True)
async def remove(args, file):
    if await check_permissions(args.message.author, True) is False:
        return
    filename = file + ".txt"
    if os.path.isfile(filename):
        os.remove(filename)
        await bot.say("Removed the " + file + " playlist.")
    else:
        await bot.say("Playlist does not exist.")

'''
Switch current auto-playlist
'''
@bot.command(pass_context=True)
async def switch(args, playlist):
    if await check_permissions(args.message.author, True) is False:
        return
    global auto_file
    auto_file = playlist + ".txt"
    await load_auto_playlist()
    await bot.say("Switched to " + playlist + " playlist")

'''
Fetch all existing playlists
'''
@bot.command(pass_context=True)
async def playlists(args):
    if await check_permissions(args.message.author, False) is False:
        return
    message = ""
    num = 1
    for file in glob.glob("*.txt"):
        message += (str(num) + ".)" + "   " + file.replace(".txt", "") + "  " + "-  " + await get_playlist_size(file) + " songs" + "\n")
        num += 1
    embed = discord.Embed(title="", type="rich", description=message, color=discord.Colour.green())
    footer = str(num) + " playlists  |  " + await get_total_song_amount() + " total songs"
    embed.set_footer(text=footer, icon_url="http://www.clker.com/cliparts/b/5/e/d/12161808711279956059jean_victor_balin_icon_graphics.svg.hi.png")
    auth = "Playlists"
    embed.set_author(name=auth, icon_url="https://images.vexels.com/media/users/3/131548/isolated/preview/9e36529b6e31cc4bae564fc2d14a8d0f-music-note-circle-icon-by-vexels.png")
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)

# TODO: END OF BLOCK OF CODE UNDER ABOVE TODO

'''
Get the total songs across all auto playlists
'''
async def get_total_song_amount():
    total = 0
    for file in glob.glob("*.txt"):
        with open(file) as lines:
            for x in lines:
                total += 1
    return str(total)

'''
Change the volume
'''
@bot.command(pass_context=True)
async def volume(args, volume):
    if await check_permissions(args.message.author, True) is False:
        return
    global player
    if not volume.isnumeric():
        await bot.say("Volume must be a number between 0 and 200")
    elif int(volume) < 0 or int(volume) > 200:
        await bot.say("Volume must be a number between 0 and 200")
    else:
        player.volume = int(volume) / 200
        await bot.say("Volume set to " + volume + "%.")

'''
Gets the number of songs in the given playlist
'''
async def get_playlist_size(playlist):
    size = 0
    with open(playlist) as lines:
        for x in lines:
            size += 1
    return str(size)


'''
Gets the names of all commands
'''
@bot.command(pass_context=True)
async def commands(args):
    if await check_permissions(args.message.author, False) is False:
        return
    cmd = False
    cmds = []
    with open("main.py") as lines:
        for x in lines:
            if cmd is True:
                idx = x.find("(", 0, len(x) - 1)
                cmds.append(x[10:idx])
            if x.startswith("@bot.command"):
                cmd = True
            else:
                cmd = False
        lines.close()
    cmds.sort()
    message = "Current commands are:" + "\n"
    for command in cmds:
        message += "    " + command + "\n"
    embed = discord.Embed(title="", type="rich", description=message, color=discord.Colour.green())
    footer = str(len(cmds)) + " commands"
    embed.set_footer(text=footer,
                     icon_url="http://www.clker.com/cliparts/b/5/e/d/12161808711279956059jean_victor_balin_icon_graphics.svg.hi.png")
    auth = "Commands"
    embed.set_author(name=auth,
                     icon_url="https://images.vexels.com/media/users/3/131548/isolated/preview/9e36529b6e31cc4bae564fc2d14a8d0f-music-note-circle-icon-by-vexels.png")
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)


'''
Fun text modifier that turns the input into regional indicator emoji
'''
@bot.command(pass_context=True)
async def emoji(args, left):
    if await check_permissions(args.message.author, False) is False:
        return
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
    if await check_permissions(args.message.author, False) is False:
        return
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
    if await check_permissions(args.message.author, False) is False:
        return
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
    if await check_permissions(args.message.author, True) is False:
        return
    await speak(args.message.content[4::])
    await bot.say(":full_moon: :house:")


'''
Wrapper of sorts for the tts command that makes the bot sing a random song
'''
@bot.command(pass_context=True)
async def sing(args):
    if await check_permissions(args.message.author, True) is False:
        return
    song = songs.get_song()
    await speak(song)
    await bot.say(":notes:")


'''
Adds a song to the queue by searching youtube for the input.
'''
@bot.command(pass_context=True)
async def play(args):
    global main_queue
    global total_time
    if await check_permissions(args.message.author, False) is False:
        return
    if args.message.channel.id != configs.TEXT_CHANNEL_ID:
        return
    link = args.message.content[6::]
    result = await search(link)
    main_queue.append(result)
    info = await get_vid_info(result)
    time = await get_time_as_string(total_time)
    total_time += info['duration']
    title = "**" + "[" + info['title'] + "]" + "(" + current + ")" + "**"
    desc = title + "\n" + "Added by " + args.message.author.name + " | Will play in about " + time
    embed = discord.Embed(type="rich", description=desc, color=discord.Colour.green())
    img = info['thumb']
    embed.set_thumbnail(url=img)
    auth = "Song Queued At Position #"+str(len(main_queue))
    embed.set_author(name=auth, icon_url="https://images.vexels.com/media/users/3/131548/isolated/preview/9e36529b6e31cc4bae564fc2d14a8d0f-music-note-circle-icon-by-vexels.png")
    footer = str("{:,}".format(info['views'])) + " views | " + info['length']
    embed.set_footer(text=footer, icon_url="http://www.clker.com/cliparts/b/5/e/d/12161808711279956059jean_victor_balin_icon_graphics.svg.hi.png")
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)


'''
Displays information about the current song
'''
@bot.command(pass_context=True)
async def nowplaying(args):
    global current
    if await check_permissions(args.message.author, False) is False:
        return
    if args.message.channel.id != configs.TEXT_CHANNEL_ID:
        return
    info = await get_vid_info(current)
    embed = discord.Embed(title=info['title'], type="rich", color=discord.Colour.green())
    img = info['thumb']
    embed.set_thumbnail(url=img)
    auth = "Now Playing"
    embed.set_author(name=auth, icon_url="https://images.vexels.com/media/users/3/131548/isolated/preview/9e36529b6e31cc4bae564fc2d14a8d0f-music-note-circle-icon-by-vexels.png")
    footer = str("{:,}".format(info['views'])) + " views | " + info['length']
    embed.set_footer(text=footer, icon_url="http://www.clker.com/cliparts/b/5/e/d/12161808711279956059jean_victor_balin_icon_graphics.svg.hi.png")
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)


'''
Displays the queue of songs ready to be played
'''
@bot.command(pass_context=True)
async def queue(args):
    global main_queue
    global total_time
    if await check_permissions(args.message.author, False) is False:
        return
    if args.message.channel.id != configs.TEXT_CHANNEL_ID:
        return
    message = ""
    pos = 1
    for i in range(0, len(main_queue)):
        info = await get_vid_info(main_queue[i])
        duration = info['duration']
        time = await get_time_as_string(duration)
        message += (str(pos) + ".) " + str(info['title']) + " " + "[" + time + "]" + "\n")
        pos += 1
    total = await get_time_as_string(total_time)
    embed = discord.Embed(title="", type="rich", description=message, color=discord.Colour.green())
    auth = "Queue"
    embed.set_author(name=auth, icon_url="https://images.vexels.com/media/users/3/131548/isolated/preview/9e36529b6e31cc4bae564fc2d14a8d0f-music-note-circle-icon-by-vexels.png")
    footer = str(len(main_queue)) + " videos queued | Time remaining is " + total
    embed.set_footer(text=footer,
                     icon_url="http://www.clker.com/cliparts/b/5/e/d/12161808711279956059jean_victor_balin_icon_graphics.svg.hi.png")
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)


'''
Displays the auto-queue of songs
'''
@bot.command(pass_context=True)
async def auto(args):
    global auto
    if await check_permissions(args.message.author, False) is False:
        return
    if args.message.channel.id != configs.TEXT_CHANNEL_ID:
        return
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
    global started
    global player
    global main_queue
    global auto
    global voice
    global current
    global total_time
    global state
    before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    server = discord.Server(id=configs.SERVER_ID)
    voice = bot.voice_client_in(server)
    player = await voice.create_ytdl_player(auto[0], ytdl_options=opts, before_options=before_args)
    print(player)
    gname_main = await get_vid_info(auto[0])
    gname = "►"+gname_main['title']
    await bot.change_presence(game=discord.Game(name=gname))
    current = auto[0]
    info = await get_vid_info(current)
    total_time += info['duration']
    auto.pop(0)
    state = "PLAYING"
    player.start()
    started = True


'''
Skips the current song
'''
@bot.command(pass_context=True)
async def skip(args):
    global player
    global main_queue
    global auto
    global voice
    global opts
    global current
    global total_time
    global time_since
    global state
    if await check_permissions(args.message.author, False) is False:
        return
    if args.message.channel.id != configs.TEXT_CHANNEL_ID:
        return
    embed = discord.Embed(type="rich", color=discord.Colour.green())
    embed.set_author(name="Skipping Song...", icon_url="http://www.iconsdb.com/icons/preview/royal-blue/media-step-forward-xxl.png")
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)
    info = await get_vid_info(current)
    time = info['duration'] - time_since
    total_time -= time
    time_since = 0
    player.stop()
    player = None
    state = "SKIPPING"
    await play_next_song()

'''
DEBUG THE FUCK OUT OF IT
'''
@bot.command(pass_context=True)
async def info(args):
    global player
    global main_queue
    global auto
    global voice
    global opts
    global current
    global total_time
    global time_since
    global state
    if await check_permissions(args.message.author, True) is False:
        return

    out = "Player state is: " + state + " | Voice is " + str(voice) + " | Player Obj is " + str(player)
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), out)
    
'''
Pauses the current song
'''
@bot.command(pass_context=True)
async def pause(args):
    if await check_permissions(args.message.author, False) is False:
        return
    await pauseH(args)


async def pauseH(args):
    global player
    global main_queue
    global auto
    global voice
    global current
    global state
    if args is not "auto":
        if args.message.channel.id != configs.TEXT_CHANNEL_ID:
            return
    embed = discord.Embed(type="rich", color=discord.Colour.green())
    if state == "PAUSED":
        embed.set_author(name="Song is already paused.")
    elif state != "PLAYING":
        embed.set_author(name="Player is not currently active.")
    else:
        player.pause()
        state = "PAUSED"
        embed.set_author(name="Song Paused.", icon_url="http://icons.iconarchive.com/icons/custom-icon-design/flatastic-8/512/Pause-icon.png")
        gname_main = await get_vid_info(current)
        gname = "▌▌"+gname_main['title']
        await bot.change_presence(game=discord.Game(name=gname))
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)


async def resumeH(args):
    global player
    global main_queue
    global auto
    global voice
    global current
    global state
    if args is not "auto":
        if args.message.channel.id != configs.TEXT_CHANNEL_ID:
            return
    embed = discord.Embed(type="rich", color=discord.Colour.green())
    if state == "PLAYING":
        embed.set_author(name="Player is already running.")
    elif state != "PLAYING" and state != "PAUSED":
        embed.set_author(name="Player is not currently active.")
    else:
        player.resume()
        state = "PLAYING"
        embed.set_author(name="Song Resumed.",
                         icon_url="https://maxcdn.icons8.com/Share/icon/Media_Controls//circled_play1600.png")
        gname_main = await get_vid_info(current)
        gname = "►" + gname_main['title']
        await bot.change_presence(game=discord.Game(name=gname))
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)


'''
Resumes the paused song
'''
@bot.command(pass_context=True)
async def resume(args):
    if await check_permissions(args.message.author, False) is False:
        return
    await resumeH(args)

'''
Roll away!
'''
@bot.command(pass_context=True)
async def roll(args):
    if await check_permissions(args.message.author, False) is False:
        return
    msg = args.message.content[6:]
    msg = dice.parse_roll(msg)
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), msg)
    
'''
Pat Pat
'''
@bot.command(pass_context=True)
async def pat(args):
    if await check_permissions(args.message.author, False) is False:
        return
    n = args.message.author.name
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), "*pats " + n + ".*")

@bot.command(pass_context=True)
async def reload(args):
    if await check_permissions(args.message.author, True) is False:
        return
    global player
    player.stop()
    player = None
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), "Attempting to restart the player...")

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
    global total_time
    global time_since
    global state
    global pp
    global started
    await bot.wait_until_ready()
    while not bot.is_closed:
        try:
            args = "auto"
            if player is not None:
                server = bot.get_server(configs.SERVER_ID)
                self = server.me
                c = 0
                if c == 10:
                    print(state)
                    c = 0
                else:
                    c += 1
                print(voice.endpoint)
                if len(self.voice.voice_channel.voice_members) == 1 and state is not "PAUSED":
                    await pauseH(args)
                    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), "Voice channel empty. Player has been paused")
                    pp = True
                if state == "PAUSED" and len(self.voice.voice_channel.voice_members) > 1 and pp is True:
                    await resumeH(args)
                    pp = False
                if player.is_done():
                    player.stop()
                    player = None
                    await play_next_song()
                else:
                    if state is "PLAYING":
                        total_time -= 1
                        time_since += 1
                if voice.is_connected is False:
                    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
                    voice = await bot.join_voice_channel(voice_channel)
                    print("VOICE CHANNEL DISCONNECTED, RECONNECTING...")

                if bot.ws is None:
                    bot.connect()
            else:
                if started is True and state is not "SKIPPING":
                    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), "Error Occured with YTDL, retrying.")
                    await start_player()
                    await asyncio.sleep(3)
        except:
            continue
        await asyncio.sleep(1)


'''
Searches youtube for the input, returns a link to the video to be played
'''
async def search(search_query):
    query = urllib.parse.quote(search_query)
    url = "https://www.youtube.com/results?search_query=" + query
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
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
    info['thumb'] = video.thumb
    info['views'] = video.viewcount
    info['length'] = video.duration
    return info


async def play_next_song():
    global current
    global total_time
    global player
    global voice
    global main_queue
    global state
    before_args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    if not len(main_queue) == 0:
        next = main_queue[0]
        current = next
        main_queue.pop(0)
    elif not len(auto) == 0:
        next = auto[0]
        current = next
        print(auto)
        print(current)
        auto.pop(0)
    else:
        next = "https://www.youtube.com/watch?v=O8EzbKWaUpQ"
        current = next
    player = await voice.create_ytdl_player(next, ytdl_options=opts, before_options=before_args)
    gname_main = await get_vid_info(next)
    gname = "►" + gname_main['title']
    await bot.change_presence(game=discord.Game(name=gname))
    #EMBED MESSAGE
    song = ""
    if str(len(main_queue)) == 1:
        song = "song"
    else:
        song = "songs"
    info = await get_vid_info(current)
    title = "**" + "[" + info['title'] + "]" + "(" + current + ")" + "**"
    desc = title + "\n" + str(len(main_queue)) + " " + song + " left in the queue."
    embed = discord.Embed(type="rich", description=desc, color=discord.Colour.green())
    img = info['thumb']
    embed.set_thumbnail(url=img)
    auth = "Playing Song"
    embed.set_author(name=auth, icon_url="https://images.vexels.com/media/users/3/131548/isolated/preview/9e36529b6e31cc4bae564fc2d14a8d0f-music-note-circle-icon-by-vexels.png")
    footer = str("{:,}".format(info['views'])) + " views | " + info['length']
    embed.set_footer(text=footer, icon_url="http://www.clker.com/cliparts/b/5/e/d/12161808711279956059jean_victor_balin_icon_graphics.svg.hi.png")
    await bot.send_message(bot.get_channel(configs.TEXT_CHANNEL_ID), embed=embed, tts=False)
    state = "PLAYING"
    player.start()

async def check_streams():
    global streamer_file
    found = 0
    await asyncio.sleep(10)
    with open(streamer_file) as list:
        content = list.readlines()
        auto = [x.strip() for x in content]
        found = [0 for x in auto]
    while True:
        i = 0
        for name in auto:
            online = stream_check.check_online(name)
            """
            0 = isStreaming
            1 = game
            2 = status
            3 = thumbnail
            """
            if online[0]:
                if found[i] == 0:
                    desc = online[1] + " - " + online[2] + "\nWatch at https://www.twitch.tv/" + name
                    t = name + " is now Streaming!"
                    embed = discord.Embed(type="rich", title=t, description=desc, color=discord.Colour.green())
                    embed.set_thumbnail(url=online[3])
                    await bot.send_message(bot.get_channel("452642460594601984"), embed=embed, tts=False)
                found[i] = 1
                #print(name + " is streaming!")
            else:
                found[i] = 0
                #print(name + " is not streaming!")
            i += 1
        await asyncio.sleep(10)
'''
Handles errors
'''
@bot.event
async def on_command_error(error, ctx):
    print(error)
    # TODO: print helpful error messages
    # bot.send_message(ctx.message.channel, help.get_help(ctx.invoked_with))

bot.loop.create_task(check_player())
bot.loop.create_task(check_streams())
bot.run(token)
