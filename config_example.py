bot_key = "..."
owner_id = None
prefix = "!"

initial_cogs = (
    'cogs.chat_utils',
    'cogs.joins',
    'cogs.mods',
    'cogs.owner',
    'cogs.voice'
)

class ChatUtilsConfig:
    guild_id = None
    offtopic_id = None

class JoinsConfig:
    join_msg = ''
    leave_msg = ''
    channel_id = None

class ModsConfig:
    guild_id = None
    admin_id = None
    admin_active_id = None
    mods_id = None
    mods_active_id = None

class VoiceConfig:
    guild_id = None
    voice_id = None
    chat_id = None

