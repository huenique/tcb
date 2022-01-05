from loguru import logger
from telethon.errors.rpcerrorlist import MessageIdInvalidError
from telethon.sync import TelegramClient, events

SESSION_NAME = "session"
API_ID = 1647211
API_HASH = "aa39d54c42eee84a40a0084743546433"
ENTITY = "@Litecoin_click_bot"


class Client:
    client: TelegramClient
    _wait = "please stay"
    _done = "sorry, there are no new ads available"
    _earn = "you earned"
    _new_site = "there is a new site"

    async def claim_reward(self) -> None:
        try:
            messages = await self.client.get_messages(ENTITY)
            message = messages[0]

            if self._done in (msg := message.message.lower()):
                logger.error(msg)
                return

            if self._new_site in msg:
                logger.info(msg)
                await self.client.send_message(ENTITY, "/visit")
                return

            if self._earn in msg:
                logger.success(msg)

            # send url to self
            url = message.reply_markup.rows[0].buttons[0].url
            await self.client.send_message("me", url)

        except MessageIdInvalidError as msg_err:
            logger.warning(msg_err)
        except AttributeError:
            pass

    async def handler(self, event):
        await self.claim_reward()

    def start(self):
        with TelegramClient("session", API_ID, API_HASH) as self.client:
            assert isinstance(self.client, TelegramClient)
            self.client.add_event_handler(self.handler, events.NewMessage)
            self.client.run_until_disconnected()
