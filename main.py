import asyncio

from bot import MaidKotori

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def main():
    bot = MaidKotori()
    bot.run()

main()
