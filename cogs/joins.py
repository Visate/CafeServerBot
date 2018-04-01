from discord.ext import commands
import discord

from config import JoinsConfig as config

class Joins:
    """
    Join/leave announcements.
    """

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        channel = member.guild.get_channel(config.channel_id)
        if channel:
            embed = discord.Embed(colour=discord.Colour.blue(),
                    description=f'{member.mention} joined the server.')
            embed.set_author(name=member,
                             icon_url=member.avatar_url_as(size=256))
            await channel.send(config.join_msg,
                               embed=embed)

    async def on_member_remove(self, member):
        channel = member.guild.get_channel(config.channel_id)
        if channel:
            embed = discord.Embed(colour=discord.Colour.orange(),
                    description=f'{member.mention} left the server.')
            embed.set_author(name=member,
                             icon_url=member.avatar_url_as(size=256))
            await channel.send(config.leave_msg,
                               embed=embed)

def setup(bot):
    bot.add_cog(Joins(bot))
