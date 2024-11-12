import discord
from discord.ext import commands
from discord import app_commands
import time
import platform
import psutil
import datetime
import asyncio

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(name="hello")
    async def hello_prefix(self, ctx):
        """Says hello (prefix command)"""
        await ctx.send('Hello! I am your 24/7 bot!')

    @app_commands.command(name="hello")
    async def hello_slash(self, interaction: discord.Interaction):
        """Says hello (slash command)"""
        await interaction.response.send_message('Hello! I am your 24/7 bot!')

    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f'🏓 Pong! Latency: {latency}ms')

    @app_commands.command()
    async def stats(self, interaction: discord.Interaction):
        """Shows detailed bot statistics"""
        uptime = str(datetime.timedelta(seconds=int(time.time() - self.start_time)))
        
        embed = discord.Embed(
            title="📊 Bot Statistics",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        
        embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=True)
        
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)), inline=True)
        embed.add_field(name="Users", value=str(sum(g.member_count for g in self.bot.guilds)), inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        
        await interaction.response.send_message(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Clear a specified number of messages"""
        if amount < 1:
            await ctx.send("Please specify a positive number!")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include command message
        msg = await ctx.send(f"🗑️ Deleted {len(deleted) - 1} messages!")
        await asyncio.sleep(3)
        await msg.delete()

    @app_commands.command()
    async def serverinfo(self, interaction: discord.Interaction):
        """Display information about the server"""
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"ℹ️ {guild.name} Info",
            color=discord.Color.blue(),
            timestamp=datetime.datetime.utcnow()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # General info
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Created On", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        
        # Member info
        total_members = guild.member_count
        online_members = len([m for m in guild.members if m.status != discord.Status.offline])
        embed.add_field(name="Total Members", value=total_members, inline=True)
        embed.add_field(name="Online Members", value=online_members, inline=True)
        embed.add_field(name="Boost Level", value=f"Level {guild.premium_tier}", inline=True)
        
        # Channel info
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        embed.add_field(name="Text Channels", value=text_channels, inline=True)
        embed.add_field(name="Voice Channels", value=voice_channels, inline=True)
        embed.add_field(name="Categories", value=categories, inline=True)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        """Display information about a user"""
        member = member or interaction.user
        
        embed = discord.Embed(
            title=f"👤 User Information - {member.name}",
            color=member.color,
            timestamp=datetime.datetime.utcnow()
        )
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name="Bot?", value="Yes" if member.bot else "No", inline=True)
        
        roles = [role.mention for role in reversed(member.roles[1:])]  # Exclude @everyone
        embed.add_field(name=f"Roles [{len(roles)}]", value=" ".join(roles) if roles else "None", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        """Display a user's avatar"""
        member = member or interaction.user
        
        embed = discord.Embed(
            title=f"🖼️ {member.name}'s Avatar",
            color=discord.Color.blue()
        )
        
        if member.avatar:
            embed.set_image(url=member.avatar.url)
            embed.add_field(name="Avatar URL", value=f"[Click Here]({member.avatar.url})")
        else:
            embed.description = "This user has no custom avatar."
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot)) 