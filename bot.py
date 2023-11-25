import signal
import logging
import logging.config
import asyncio
from typing import Union, Optional, AsyncGenerator
from pyrogram import Client, types

# Add your missing imports
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN
from utils import temp

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

name = """
██████╗ ██████╗ ██╗███╗   ███╗███████╗██╗  ██╗██╗   ██╗██████╗ 
██╔══██╗██╔══██╗██║████╗ ████║██╔════╝██║  ██║██║   ██║██╔══██╗
██████╔╝██████╔╝██║██╔████╔██║█████╗  ███████║██║   ██║██████╔╝
██╔═══╝ ██╔══██╗██║██║╚██╔╝██║██╔══╝  ██╔══██║██║   ██║██╔══██╗
██║     ██║  ██║██║██║ ╚═╝ ██║███████╗██║  ██║╚██████╔╝██████╔╝
╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ 
"""

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=500,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start_bot(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        self._link = None
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(name)

    async def stop_bot(self):
        await super().stop()
        logging.info("Bot stopped. Bye.")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1
app = Bot()
async def signal_handler():
    await app.stop_bot()

signal.signal(signal.SIGTERM, signal_handler)


async def main():
    try:
        await app.start_bot()

    except KeyboardInterrupt:
        logging.info("Bot interrupted by user.")
        pass
    finally:
        await app.stop_bot()
        await loop.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
