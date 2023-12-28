import discord
from discord.ext import commands
from googleapiclient.discovery import build

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True

bot_token = "Bot_Tocken"
youtube_api_key = "youtube_API"

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx, *, query):
    youtube_api_key = 'AIzaSyAMl4j-F0EtP6y2r4hYq41zho6ys0I5XTI'

    youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    search_response = youtube.search().list(
        q=query,
        part='id',
        maxResults=1
    ).execute()

    if 'items' in search_response and search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'

        voice_channel = ctx.author.voice.channel
        vc = await voice_channel.connect()

        vc.play(discord.FFmpegPCMAudio(video_url, options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
    else:
        await ctx.send("Keine Suchergebnisse gefunden.")

@bot.command()
async def leave(ctx):
    voice_channel = ctx.author.voice.channel
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await vc.disconnect()

bot.run(bot_token)
