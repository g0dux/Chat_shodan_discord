import os
import re
import json
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.environ.get('you_api_here')

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

intents = discord.Intents.all()  # Carrega todas as intenções
bot = commands.Bot(command_prefix="?", intents=intents)

@bot.command(name="shodan")
async def shodan_command(ctx, args):
    """Searches the Shodan InternetDB for information about a given IP address."""

    if not is_valid_ip(args):
        await ctx.channel.send("Error: Invalid IP Address.")
        return

    # Make a request to the Shodan API
    shodan_result = requests.get("https://internetdb.shodan.io/" + args)

    if shodan_result.status_code != 200:
        await ctx.channel.send("Error: Could not retrieve information from Shodan.")
        return

    # Parse the JSON response from Shodan
    shodan_json = json.loads(shodan_result.content)

    # If there is no information available for the given IP address, send an error message
    if "detail" in shodan_json and shodan_json["detail"] == "No information available":
        await ctx.channel.send("Error: No information available for this IP address.")
        return

    # Create an Embed object to display the Shodan results
    embed = discord.Embed(title="Shodan InternetDB Results For " + args, color=0xdf0000)
    embed.add_field(name="Hostnames", value=shodan_json["hostnames"], inline=False)
    embed.add_field(name="Open Ports", value=shodan_json["ports"], inline=False)
    embed.add_field(name="Tags", value=shodan_json["tags"], inline=False)
    embed.add_field(name="CPEs", value=shodan_json["cpes"], inline=False)
    embed.add_field(name="Vulns", value=shodan_json["vulns"], inline=False)

    # Send the Embed object to the channel
    await ctx.send(embed=embed)

# Start the bot
keep_alive()
bot.run('you_token_here')
