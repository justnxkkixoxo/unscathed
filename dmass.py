import discord
from discord.ext import commands
import asyncio
import colorsys
import random
import os

# Initialize the bot client (v1.7.3 syntax)
client = commands.Bot(command_prefix='-', case_insensitive=True)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} (ID: {client.user.id})')
    print('--------')
    print('CREATED AND HOSTED BY NUZZ')

@client.command()
@commands.has_permissions(kick_members=True)     
async def userinfo(ctx, user: discord.Member):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(
        title=f"{user.name}'s info", 
        description="Here's what I could find.", 
        color=discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=str(user.status), inline=True)
    embed.add_field(name="Highest role", value=user.top_role, inline=True)
    embed.add_field(name="Joined", value=str(user.joined_at), inline=True)
    
    if user.avatar_url:
        embed.set_thumbnail(url=user.avatar_url)
        
    await ctx.send(embed=embed)
    
@client.command()
@commands.has_permissions(administrator=True)
async def send(ctx, *, content: str):
    await ctx.send("Starting Mass DM process... Please wait.")

    for member in ctx.guild.members:
        # Skip bots and yourself
        if member.bot or member == client.user:
            continue
            
        try:
            # Send the DM directly to the member
            await member.send(content)
            await ctx.send(f"✅ DM Sent To : {member.name}")
        except Exception:
            await ctx.send(f"❌ DM Can't Send To : {member.name}")
            
        # ⏱️ THE 5-SECOND TIMER TO PREVENT DISCORD RATE LIMITS
        await asyncio.sleep(5)

    await ctx.send("📢 Mass DM process finished!")

# Run the bot (Heroku uses this environment variable)
token = os.getenv("DISCORD_TOKEN")
if token:
    client.run(token)
else:
    print("Error: DISCORD_TOKEN environment variable not found.")
