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
            workers=2000,
            plugins={"root": "plugins"},
            sleep_threshold=10,
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


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run())
except KeyboardInterrupt:
    # Handle KeyboardInterrupt (Ctrl+C) separately if needed
    print("Bot interrupted by user. Exiting...")

except Exception as e:
    # Handle other exceptions as needed
    print(f"An error occurred: {e}")
