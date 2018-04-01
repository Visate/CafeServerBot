from discord.ext import commands
import discord

from .utils.utility import get_discord_object
from config import VoiceConfig as config

class Voice:
    """
    Voice channels utilities
    """

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.voice_role = None
        self.chat_role = None
        self.initialize()

    def initialize(self):
        """
        Runs at ready or the first time a command or event is called.
        Stores the channels so they aren't constantly searched for.

        Not sure if this is good practice or not but screw it I'm doing it.
        """
        self.guild = get_discord_object(self.bot.guilds, config.guild_id)

        if self.guild:
            self.voice_role = get_discord_object(self.guild.roles, config.voice_id)
            self.chat_role = get_discord_object(self.guild.roles, config.chat_id)

    async def on_voice_state_update(self, member, before, after):
        """
        If member is joining the voice channel, assign the voice role to them
        If member is leaving the voice channel, remove the voice from from them
        """
        if before.channel is None and after.channel is not None:
            await member.add_roles(self.voice_role)

        elif after.channel is None and before.channel is not None:
            await member.remove_roles(self.voice_role)

    @commands.command(aliases=['showvc'], name='showvoicechat')
    async def show_voice_chat(self, ctx):
        """
        Toggles the voice visible (👀) role,
        which keeps the voice chat lounges visible at all times.
        """
        member_roles = ctx.author.roles
        if self.chat_role in member_roles:
            await ctx.author.remove_roles(self.chat_role, 
                                          reason='Removing voice visible role.')
        
        else:
            await ctx.author.add_roles(self.chat_role,
                                       reason='Adding voice visible role.')
        
        await ctx.message.add_reaction('\N{OK HAND SIGN}')

    # @commands.command(alias=['createvc'], name='createvoicechannel')
    # @is_elevated
    # async def create_voice_channel(self, ctx, *, name: str):
    #     pass
        
def setup(bot):
    bot.add_cog(Voice(bot))
