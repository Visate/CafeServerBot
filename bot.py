from discord.ext import commands
import discord
import traceback

import config

description = """
Chun chun!~ I am a bot programmed by Visate#7752!
"""

class MaidKotori(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(
                         config.prefix),
                         description=description)

        self.bot_key = config.bot_key

        for cog in config.initial_cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print(f'Failed to load cog {cog}.')
                traceback.print_exc()

    async def on_ready(self):
        print(f'Logged on as {self.user}! (ID: {self.user.id})')
        await self.get_channel(428662180116692992).send("( · 8 · )")
        self.get_cog('Mods').initialize()
        self.get_cog('Voice').initialize()

    async def on_resume(self):
        print('Bot resumed.')

    @property
    def config(self):
        return __import__(config)

    def run(self):
        super().run(self.bot_key, reconnect=True)

if __name__ == "__main__":
    from main import main
    main()
