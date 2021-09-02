import discord
import randfacts
from discord.ext import commands

import GetLyrics_ATRS_SelfBot
import GetTime_ATRS_SelfBot
import GetMeaning_ATRS_SelfBot
import GetWeather_ATRS_SelfBot
import praw
import random
from discord import Spotify
import sys
import subprocess


def pip_install(module: str):
    subprocess.run([sys.executable, "-m", "pip", "-q", "--disable-pip-version-check", "install", module])


# ---PIP INSTALLATIONS---
# print("Installing 'googletrans==3.1.0a0'... ")
# pip_install("googletrans==3.1.0a0")
from googletrans import Translator

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="~", self_bot=True, intents=intents)


@bot.event
async def on_ready():
    print("SelfBot is ready. ")


bot.remove_command("help")


@bot.command(pass_context=True)
async def lyrics(ctx, *args):
    await ctx.message.delete()
    track = " ".join(args)
    user = ctx.author
    for activity in user.activities:
        if isinstance(activity, Spotify):
            track = activity.title + " by " + str(activity.artist).split(";")[0]
    if track == "" or track == " " or track.isspace():
        await ctx.send(":question: What track to search? Correct format: `~lyrics [Query]`", delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, searching for `{track}`")
        try:
            search_lyrics = GetLyrics_ATRS_SelfBot.GetLyrics()
            try:
                search_lyrics.musixmatch_lyrics(query=track)
            except TimeoutError:
                search_lyrics.google_lyrics(query=track)
            except:
                search_lyrics.genius_lyrics(query=track,
                                            api_key="API Key")
            embed = discord.Embed(title=search_lyrics.title, description="**" + search_lyrics.artist + "**",
                                  colour=0xffae00)
            lyric = str(str(search_lyrics.lyrics).strip()).split("\n\n")
            for i in lyric:
                embed.add_field(name="​", value=i, inline=False)
            embed.set_footer(text="Source: " + search_lyrics.source)
            try:
                await wait.edit(embed=embed, content="")
            except:
                embed = discord.Embed(title=":x: Something went wrong, can't show lyrics. Click here. ",
                                      url=search_lyrics.url, colour=0xffae00)
                await wait.edit(embed=embed, content="")
        except:
            await wait.edit(content=":x: Something went wrong, can't show lyrics ")


@bot.command(pass_context=True)
async def lyricsg(ctx, *args):
    await ctx.message.delete()
    track = " ".join(args)
    if not args:
        await ctx.send(":question: What track to search? Correct format: `~lyrics [Query]`", delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, searching for `{track}`")
        try:
            search_lyrics = GetLyrics_ATRS_SelfBot.GetLyrics()
            search_lyrics.genius_lyrics(query=track,
                                        api_key="API Key")
            embed = discord.Embed(title=search_lyrics.title, description="**" + search_lyrics.artist + "**",
                                  colour=0xffae00)
            lyric = str(search_lyrics.lyrics.strip()).split("\n\n")
            for i in lyric:
                embed.add_field(name="​", value=i, inline=False)
            embed.set_footer(text="Source: " + search_lyrics.source)
            try:
                await wait.edit(embed=embed, content="")
            except:
                embed = discord.Embed(title="Something went wrong, can't show lyrics. Click here. ",
                                      url=search_lyrics.url, colour=0xffae00)
                await wait.edit(embed=embed, content="")
        except:
            await wait.edit(content=":x: Something went wrong, can't show lyrics ")


@bot.command(pass_context=True)
async def time(ctx, *args):
    await ctx.message.delete()
    location = " ".join(args)
    if not args:
        await ctx.send(":question: Time of where? Correct format: `~time [Location]`", delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, getting time of `{location}`")
        try:
            time_now = GetTime_ATRS_SelfBot.GetTime()
            time_now.current_time(location)
            embed = discord.Embed(title=time_now.time, description="**" + time_now.date + "**\n" + time_now.location,
                                  colour=0xffae00)
            await wait.edit(embed=embed, content="")
        except:
            await wait.edit(content=":x: Something went wrong, can't get time ")


@bot.command(pass_context=True)
async def delete(ctx, amount="None"):
    await ctx.message.delete()
    if amount == "None":
        await ctx.send(":exclamation: Invalid value. Correct format: `~delete [Number of messages to delete]`",
                       delete_after=10)
        return
    try:
        amount = int(amount)
    except:
        await ctx.send(":exclamation: Invalid value, amount must be in integer. Correct format: `~delete [Amount]`",
                       delete_after=10)
        return
    if amount < 1 or amount > 300:
        await ctx.send(":exclamation: Invalid value, amount must be in integer. Correct format: `~delete [Amount]`",
                       delete_after=10)
        return
    try:
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(title="Messages Deleted Successfully", colour=0xffae00)
        await ctx.send(embed=embed)
    except:
        await ctx.send(content=":x: Something went wrong, can't delete messages. Make sure for proper permissions ")


@bot.command(pass_context=True)
async def embed(ctx, *args):
    await ctx.message.delete()
    if not args:
        await ctx.send(":question: What are contents of embed? Correct format: `~embed -author: XYZ "
                       "-title: Title Here -description: Description Here -field: Name Here; Value Here [separated by "
                       ";][Use "
                       "'None' if you want it to remain empty] "
                       "-footer: Footer Here`. Don't use functions which you don't want to add them like if you don't "
                       "want to "
                       "add footer, then don't use `-footer`", delete_after=10)
        return
    try:
        color = 0xffae00
        empty = "​"
        com = " ".join(args)
        coms = com.split("-")
        title = ""
        description = ""
        author = ""
        footer = ""
        for i in coms:
            if i.split(":")[0].strip().lower() == "author":
                author = i.split(":")[1].strip()
            elif i.split(":")[0].strip().lower() == "title":
                title = i.split(":")[1].strip()
            elif i.split(":")[0].strip().lower() == "description":
                description = i.split(":")[1].strip()
            elif i.split(":")[0].strip().lower() == "footer":
                footer = i.split(":")[1].strip()
        embed = discord.Embed(title=title, description=description, colour=color)
        embed.set_footer(text=footer)
        embed.set_author(name=author)
        try:
            for i in coms:
                if i.split(":")[0].strip().lower() == "field":
                    name = i.split(":")[1].split(";")[0].strip()
                    text = i.split(":")[1].split(";")[1].strip()
                    embed.add_field(name=name if name.lower() != "none" else empty,
                                    value=text if text.lower() != "none" else empty, inline=False)
        except:
            await ctx.send(
                content=":x: Something went wrong while adding field. Make sure you used proper format. Use `none` if you want something to be empty. ")
            return
        await ctx.send(embed=embed)
    except:
        await ctx.send(
            ":x: Something went wrong. Correct format: `~embed -author: XYZ "
            "-title: Title Here -description: Description Here -field: Name Here; Value Here [separated by ;][Use "
            "'None' if you want it to remain empty] "
            "-footer: Footer Here`. Don't use functions which you don't want to add them like if you don't want to "
            "add footer, then don't use `-footer`")


@bot.command(pass_context=True)
async def weather(ctx, *args):
    await ctx.message.delete()
    place = " ".join(args)
    if not args:
        await ctx.send(":question: Weather of which place? Correct format: `~weather [Location]`", delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, gathering weather details")
        try:
            try:
                wd = GetWeather_ATRS_SelfBot.GetWeather()
                wd.basic_weather(place)
            except:
                wd = GetWeather_ATRS_SelfBot.GetWeather()
                wd.detailed_weather(place, "API Key")
            temperature = wd.temperature
            des = wd.weather_description
            city = wd.location
            source = wd.source
            embed = discord.Embed(title=temperature, description="**" + des + "**\n" + city + "\n​", colour=0xffae00)
            embed.set_footer(text="Source: " + source)
            await wait.edit(embed=embed, content="")
        except:
            await wait.edit(content=":x: Something went wrong, can't get weather ")


@bot.command(pass_context=True)
async def weatherd(ctx, *args):
    await ctx.message.delete()
    place = " ".join(args)
    if not args:
        await ctx.send(":question: Weather of which place? Correct format: `~weatherd [Location]`", delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, gathering weather details")
        try:
            try:
                wd = GetWeather_ATRS_SelfBot.GetWeather()
                wd.detailed_weather(place, "API Key")
            except:
                await wait.edit(content=":x: Something went wrong, can't get weather ")
                return
            weather_description = wd.weather_description
            temperature = wd.temperature
            feels_like = wd.feels_like
            current_temp_min = wd.current_temp_min
            current_temp_max = wd.current_temp_max
            atmospheric_pressure = wd.atmospheric_pressure
            humidity = wd.humidity
            visibility = wd.visibility
            wind = wd.wind
            wind_gust = wd.wind_gust
            clouds_cover = wd.clouds_cover
            location = wd.location
            source = wd.source
            weather_info = f"""​
            Feels Like: {feels_like}
            Current Maximum Temperature: {current_temp_max}
            Current Minimum Temperature: {current_temp_min}
            ​
            Atmospheric Pressure: {atmospheric_pressure}
            Humidity: {humidity}
            Visibility: {visibility}
            Clouds Cover: {clouds_cover}
            ​
            Wind: {wind}
            Wind Direction: {wd.wind_direction}
            Wind Gust: {wind_gust}
            ​
            """.strip()
            embed = discord.Embed(title=temperature, description="**" + weather_description + "**\n" + location + "\n​",
                                  colour=0xffae00)
            embed.add_field(name="Additional Weather Information: ", inline=False, value=weather_info)
            embed.set_footer(text="Source: " + source)
            await wait.edit(embed=embed, content="")
        except:
            await wait.edit(content=":x: Something went wrong, can't get weather ")


@bot.command(pass_context=True)
async def translate(ctx, language, *args):
    await ctx.message.delete()
    if not args:
        await ctx.send(
            ":question: What to translate? Correct format: `~translate [Dest. Language][Sentence to be translated]`",
            delete_after=10)
        return
    sentence = " ".join(args)
    count = 0
    for i in sentence:
        count += 1
    if count > 900:
        await ctx.send(
            ":x: Cannot translate more than 900 characters. Correct format: `~translate [Dest. Language][Sentence to be translated]`",
            delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, translating")
        try:
            languages = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian',
                         'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian',
                         'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa',
                         'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican',
                         'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english',
                         'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french',
                         'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek',
                         'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew',
                         'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic',
                         'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese',
                         'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean',
                         'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian',
                         'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay',
                         'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian',
                         'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto',
                         'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian',
                         'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho',
                         'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian',
                         'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish',
                         'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian',
                         'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa',
                         'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'}
            translator = Translator()
            result = translator.translate(sentence, dest=language.strip().lower().replace(" ", ""))
            translation = result.text
            origin = result.origin
            destination = result.dest
            source = result.src
            for key, value in languages.items():
                if key == source:
                    source = value.capitalize()
                if key == destination:
                    destination = value.capitalize()
            embed = discord.Embed(title=f"Translation: ", colour=0xffae00)
            embed.add_field(name=source, value=origin, inline=False)
            embed.add_field(name=destination, value=translation, inline=False)
            await wait.edit(content="", embed=embed)
        except:
            await wait.edit(content=":x: Something went wrong, can't translate ")


@bot.command(pass_context=True)
async def transf(ctx, language, *args):
    await ctx.message.delete()
    if not args:
        await ctx.send(
            ":question: What to translate? Correct format: `~transf [Dest. Language][Sentence to be translated]`",
            delete_after=10)
        return
    sentence = " ".join(args)
    count = 0
    for i in sentence:
        count += 1
    if count > 1500:
        await ctx.send(
            ":x: Cannot translate more than 1500 characters. Correct format: `~translate [Dest. Language][Sentence to be translated]`",
            delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, translating")
        try:
            languages = {'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian',
                         'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian',
                         'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa',
                         'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican',
                         'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english',
                         'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french',
                         'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek',
                         'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew',
                         'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic',
                         'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese',
                         'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean',
                         'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian',
                         'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay',
                         'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian',
                         'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto',
                         'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian',
                         'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho',
                         'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian',
                         'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish',
                         'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian',
                         'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa',
                         'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu'}
            translator = Translator()
            result = translator.translate(sentence, dest=language.strip().lower().replace(" ", ""))
            translation = result.text
            destination = result.dest
            for key, value in languages.items():
                if key == destination:
                    destination = value.capitalize()
            embed = discord.Embed(title="", description=translation, colour=0xffae00)
            # embed.set_footer(text="Language: " + destination)
            await wait.edit(content="", embed=embed)
        except:
            await wait.edit(content=":x: Something went wrong, can't translate ")


@bot.command(pass_context=True)
async def image(ctx, *args):
    await ctx.message.delete()
    wait = await ctx.send(f":mag: Please hold on, searching ")
    try:
        if not args:
            url = "https://source.unsplash.com/random/" + str(random.randint(0, 10000000000000))
        else:
            keyword = "%20".join(args)
            url = "https://source.unsplash.com/random/?" + keyword + "%20" + str(random.randint(0, 10000000000000))
        embed = discord.Embed(title="", colour=0xffae00)
        embed.set_image(url=url)
        embed.set_footer(text="Source: Unsplash")
        await wait.edit(content="", embed=embed)
    except:
        await wait.edit(content=":x: Something went wrong, cannot get image ")


memes = []


@bot.command(pass_context=True)
async def meme(ctx):
    await ctx.message.delete()
    wait = await ctx.send(f":mag: Please hold on, searching ")
    try:
        reddit = praw.Reddit(client_id="Client ID",
                             client_secret="Client Secret",
                             username="Username",
                             password="",
                             user_agent="UserAgent",
                             check_for_async=False)
        if not memes:
            subreddit = reddit.subreddit("meme")
            meme = subreddit.top(limit=300)
            for i in meme:
                link = i.url
                if len(link.split('.')[-1]) == 3:
                    memes.append(i)

        send_meme = random.choice(memes)
        memes.remove(send_meme)
        embed = discord.Embed(title=send_meme.title, colour=0xffae00)
        embed.set_image(url=send_meme.url)
        embed.set_footer(text="Source: Reddit")
        await wait.edit(content="", embed=embed)
    except:
        await wait.edit(content=":x: Something went wrong, cannot get meme ")


@bot.command(pass_context=True)
async def fact(ctx):
    await ctx.message.delete()
    wait = await ctx.send(f":mag: Please hold on, searching ")
    randfac = randfacts.getFact()
    try:
        embed_details = discord.Embed(title="Random Fact: ", description=randfac, color=0xffae00)
        await wait.edit(content="", embed=embed_details)
    except:
        await wait.edit(content=":x: Something went wrong, cannot get fact ")


@bot.command(pass_context=True)
async def meaning(ctx, *args):
    await ctx.message.delete()
    if not args:
        await ctx.send(
            ":question: Meaning of what? Correct format: `~meaning [Word]`",
            delete_after=10)
        return
    else:
        wait = await ctx.send(f":mag: Please hold on, searching ")
        try:
            word = args[0]
            meaning = GetMeaning_ATRS_SelfBot.GetMeaning()
            meaning.meaning(word)
            defination = meaning.defination
            part = meaning.part_of_speech
            word = meaning.word
            usage = meaning.use
            embed = discord.Embed(title=word + f" [{part}]", description="**" + defination + "**", color=0xffae00)
            embed.set_footer(text=usage)
            await wait.edit(content="", embed=embed)
        except:
            await wait.edit(content=":x: Something went wrong, cannot get get meaning of this ")


bot.run("Your Token Here", bot=False)
