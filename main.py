import os
import discord
import requests
from discord.ext import commands
from moviepy.editor import AudioFileClip
import os
from bs4 import BeautifulSoup
import aiohttp
import asyncio

from myserver import server_on

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.typing = False

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

def get_mediafire_direct_link(url):
    try:
        # Download the Mediafire page and extract the real download link
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        download_button = soup.find('a', {'id': 'downloadButton'})
        if download_button:
            return download_button['href']
        else:
            return None
    except Exception as e:
        return None

async def download_gif(gif_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(gif_url) as response:
            if response.status == 200:
                with open('temp.gif', 'wb') as f:
                    f.write(await response.read())
                return 'temp.gif'
            else:
                return None

@bot.command(name='convert')
async def convert(ctx, format_type: str = None, file_url: str = None):
    # If no format_type is provided, send a help message
    if format_type is None:
        await ctx.author.send("Usage: `!convert <format> [file_url]`\nAvailable formats: `mp3`, `wav`, `ogg`.\nExample: `!convert mp3 [file_url]` or attach an MP4 file.")
        return

    # Validate format_type input
    valid_formats = ['mp3', 'wav', 'ogg']
    if format_type not in valid_formats:
        await ctx.author.send(f"Invalid format. Please choose from: {', '.join(valid_formats)}")
        return

    mp4_path = None

    # Handle file attachment
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
        
        if attachment.filename.endswith('.mp4'):
            mp4_path = f"./{attachment.filename}"
            await attachment.save(mp4_path)

    # Handle file URL (support for Mediafire links)
    elif file_url:
        if 'mediafire.com' in file_url:
            # Extract direct link from Mediafire
            direct_link = get_mediafire_direct_link(file_url)
            if direct_link:
                mp4_path = "./downloaded_sound.mp4"
                try:
                    response = requests.get(direct_link)
                    with open(mp4_path, 'wb') as file:
                        file.write(response.content)
                except Exception as e:
                    await ctx.author.send(f"Failed to download the file from the provided Mediafire link: {e}")
                    return
            else:
                await ctx.author.send("Failed to extract the download link from Mediafire. Please check the link.")
                return
        elif file_url.endswith('.mp4'):
            mp4_path = "./downloaded_sound.mp4"
            try:
                response = requests.get(file_url)
                with open(mp4_path, 'wb') as file:
                    file.write(response.content)
            except Exception as e:
                await ctx.author.send(f"Failed to download the file from the provided link: {e}")
                return

    # If neither an attachment nor a valid URL is provided
    if mp4_path is None:
        await ctx.author.send("Please provide an MP4 file by uploading or using a valid URL ending with `.mp4` or a valid Mediafire link.")
        return

    # Notify user that conversion has started and send a GIF in DM
    await ctx.author.send("Starting the conversion process...")
    gif_path = await download_gif("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzYwMzlpb21sNXU4MG00djN4dmtraG81dHN0bmozMXVwcGxhcTBnbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xThuWu82QD3pj4wvEQ/giphy.gif")
    
    if gif_path:
        await ctx.author.send(file=discord.File(gif_path))
    else:
        await ctx.author.send("Failed to download the GIF.")

    try:
        # Convert MP4 to the selected format
        audio_clip = AudioFileClip(mp4_path)
        audio_path = mp4_path.replace('.mp4', f'.{format_type}')
        audio_clip.write_audiofile(audio_path)
        audio_clip.close()

        # Notify user of completion and send the converted file in DM
        await ctx.author.send(f"Conversion to {format_type.upper()} complete! Here's your file:", 
                              file=discord.File(audio_path))
        
        # Clean up the local files
        os.remove(mp4_path)
        os.remove(audio_path)
        os.remove(gif_path)  # Clean up the GIF file
        
    except Exception as e:
        await ctx.author.send(f"An error occurred during the conversion: {e}")

server_on()

bot.run(os.getenv('TOKEN'))
