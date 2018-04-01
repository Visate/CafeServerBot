"""
Moderation commands module.
Some portions are sourced from RoboDanny/mod.py
"""
from discord.ext import commands
import discord
import asyncio

from .utils.utility import get_discord_object
from config import ModsConfig as config

def is_elevated():
    def predicate(ctx):
        return bool([True for role in ctx.author.roles
                     if role.id == config.admin_active_id or
                        role.id == config.mods_active_id])
    return commands.check(predicate)

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f'{argument} is not a valid member or member ID.') from None
        else:
            can_execute = ctx.author.id == ctx.bot.owner_id or \
                          ctx.author == ctx.guild.owner or \
                          ctx.author.top_role > m.top_role

            if not can_execute:
                raise commands.BadArgument('You cannot do this action on this user due to role hierarchy.')
            return m.id

class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        ban_list = await ctx.guild.bans()
        try:
            member_id = int(argument, base=10)
            entity = discord.utils.find(lambda u: u.user.id == member_id, ban_list)
        except ValueError:
            entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument('Not a valid previously-banned member.')
        return entity

class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = f'{ctx.author} (ID: {ctx.author.id}): {argument}'

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return ret

class Mods:
    """
    Moderation style commands for cafe server
    """

    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.admin_role = None
        self.admin_active_role = None
        self.mods_role = None
        self.mods_active_role = None
        self.initialize()
                                         
    def initialize(self, ctx=None):
        """
        Runs the first time a command is called
        Stores guild and roles so they aren't constantly being searched for.
        
        Not sure if this is good practice or not but screw it I'm doing it.
        """
        if ctx is not None:
            guilds = ctx.bot.guilds
        else:
            guilds = self.bot.guilds

        self.guild = get_discord_object(guilds, config.guild_id)

        if self.guild:
            self.admin_role = get_discord_object(
                                   self.guild.roles,
                                   config.admin_id)
                                   
            self.admin_active_role = get_discord_object(
                                          self.guild.roles,
                                          config.admin_active_id)

            self.mods_role = get_discord_object(
                                  self.guild.roles,
                                  config.mods_id)

            self.mods_active_role = get_discord_object(
                                         self.guild.roles,
                                         config.mods_active_id)

    async def __local_check(self, ctx):
        if not self.guild:
            self.initialize(ctx)

        guild = ctx.guild
        if guild is None or guild.id != config.guild_id:
            return False
        
        member_roles = ctx.author.roles

        if (self.admin_role in member_roles or
            self.mods_role in member_roles):
            return True

        return False
    
    @commands.command(hidden=True)
    async def elevate(self, ctx, mod: str=''):
        """
        Toggles moderation mode.

        If admin, can pass "mod" to the command in order to elevate to mod
        instead of admin.

        If any moderation roles are present, they will be removed if the
        command is run.
        """
        member_roles = ctx.author.roles
        success = False
        if (self.mods_active_role in member_roles or
            self.admin_active_role in member_roles):
            success = True
            await ctx.author.remove_roles(self.mods_active_role,
                                          self.admin_active_role,
                                          reason='Removing elevated role.')

        else:
            role = None
            msg = None

            if self.admin_role in member_roles:
                if 'mod' in mod.lower():
                    role = self.mods_active_role
                    msg = 'Elevating to Mod.'
                else:
                    role = self.admin_active_role
                    msg = 'Elevating to Admin.'

            elif self.mods_role in member_roles:
                role = self.mods_active_role
                msg = 'Elevating to Mod.'

            if role is not None and role not in member_roles:
                success = True
                await ctx.author.add_roles(role, reason=msg)
            
        if success:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')
            await asyncio.sleep(2)
            await ctx.message.delete()
    
    @commands.command(hidden=True)
    @is_elevated()
    async def kick(self, ctx, member: MemberID,
                   *, reason: ActionReason=None):
        """
        Kicks a member from the server.

        Must be elevated to use this command.
        """

        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await ctx.guild.kick(discord.Object(id=member), reason=reason)
        await ctx.message.add_reaction('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @is_elevated()
    async def softban(self, ctx, member: MemberID, 
                      *, reason: ActionReason=None):
        """
        Soft bans a member from the server.

        Softbanning bans the member from the server, but immediately unbans
        them. This is used to basically kick a member while removing their
        messages as well.

        Must be elevated to use this command.
        """
        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        obj = discord.Object(id=member)
        await ctx.guild.ban(obj, reason=reason)
        ban_list = await ctx.guild.bans()
        banned_user = [entry.user for entry in ban_list
                       if entry.user.id == member]
        if banned_user:
            await ctx.guild.unban(obj, reason=reason)
            await ctx.message.add_reaction('\N{OK HAND SIGN}')
        else:
            await ctx.message.add_reaction('\N{FACE WITH NO GOOD GESTURE}')

    @commands.command(hidden=True)
    @is_elevated()
    async def ban(self, ctx, member: MemberID, *, reason: ActionReason=None):
        """
        Bans a member from the server.

        ID may be used to ban as well. Also works for users not in the server.

        Must be elevated to use this command.
        """
        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'

        await ctx.guild.ban(discord.Object(id=member), reason=reason)
        ban_list = await ctx.guild.bans()
        banned_user = [entry.user for entry in ban_list
                       if entry.user.id == member]
        if banned_user:
            await ctx.message.add_reaction('\N{OK HAND SIGN}')
        else:
            await ctx.message.add_reaction('\N{FACE WITH NO GOOD GESTURE}')

    @commands.command(hidden=True)
    @is_elevated()
    async def unban(self, ctx, member: BannedMember,
                    *, reason: ActionReason=None):
        """
        Unbans a member from the server.

        ID can be given or the Name#Discriminator of the user.
        It is best to use ID if you can help it.

        Must be elevated to use this command.
        """
        if reason is None:
            reason = f'Action done by {ctx.author} (ID: {ctx.author.id})'
        
        await ctx.guild.unban(member.user, reason=reason)
        if member.reason:
            await ctx.send((f'Unbanned {member.user} (ID: {member.user.id}), '
                            f'previously banned for {member.reason}.'))
        else:
            await ctx.send(f'Unbanned {member.user} (ID: {member.user.id}).')

def setup(bot):
    bot.add_cog(Mods(bot))
