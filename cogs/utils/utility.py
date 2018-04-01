import discord

def get_discord_object(list_, obj_id):
    """
    Given the list of Discord objects, finds the one that matches the ID
    and returns it. Is really just an alias for the discord.utils.find
    function, just made a lot simpler.
    """
    return discord.utils.find(lambda o: o.id == obj_id, list_)
