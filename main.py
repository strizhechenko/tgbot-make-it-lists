import asyncio
import logging

from assist_bot.assist import Assist


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    assist = Assist()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(assist.dispatcher.start_polling(assist.bot))
    loop.close()
