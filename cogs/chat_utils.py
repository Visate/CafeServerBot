from discord.ext import commands
import discord

from .utils.utility import get_discord_object
from config import ChatUtilsConfig as config

class ChatUtils:
    """
    General use chat utilities for the server.
    """

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.offtopic_role = None
        self.initialize()
    
    def initialize(self):
        """
        Runs at ready or the first time a command or event is called.
        Stores roles so they aren't constantly searched for.
        """
        self.guild = get_discord_object(self.bot.guilds, config.guild_id)
        self.offtopic_role = get_discord_object(self.guild.roles, 
                                                config.offtopic_id)

    @commands.command()
    async def offtopic(self, ctx):
        """
        Toggles access to the offtopic channel.
        """
        member_roles = ctx.author.roles
        if self.offtopic_role in member_roles:
            await ctx.author.remove_roles(self.offtopic_role, 
                                          reason='Removing offtopic role.')
        
        else:
            await ctx.author.add_roles(self.offtopic_role,
                                       reason='Adding offtopic role.')
        
        await ctx.message.add_reaction('\N{OK HAND SIGN}')

    @commands.command()
    async def serverinfo(self, ctx):
        """
        Displays information and statistics about the server.
        """
        guild = ctx.guild

        if guild:
            desc = (f'**❄ Owner:** {guild.owner} (ID: {guild.owner.id})\n'
                    f'**❄ Members:** {len(guild.members)}\n'
                    f'**❄ Channels:** {len(guild.channels)} '
                    f'({len(guild.categories)} categories,'
                    f' {len(guild.text_channels)} text,'
                    f' {len(guild.voice_channels)} voice)\n'
                    f'**❄ Roles:** {len(guild.roles)}\n'
                    f'**❄ Region:** {guild.region}\n'
                    f'**❄ Created at:** '
                    f'{ctx.guild.created_at.strftime("%d %B %Y %I:%M%p UTC")}')

            embed = discord.Embed(title=f'{guild.name} (ID: {guild.id})',
                                  description=desc,
                                  colour=discord.Colour.from_rgb(255, 95, 255))

            if guild.icon:
                embed.set_thumbnail(url=guild.icon_url)
            if guild.splash:
                embed.set_image(url=guild.splash_url)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ChatUtils(bot))
