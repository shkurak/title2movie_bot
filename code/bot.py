import argparse
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from utils import handle_request
from messages import MESSAGES


parser = argparse.ArgumentParser()
parser.add_argument("--api_token", type=str)
parser.add_argument("--proxy", type=str, default="http://222.124.2.186:8080")
args = parser.parse_args()

bot = Bot(token=args.api_token, proxy=args.proxy)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", 'help'])
async def send_welcome(message: types.Message):
    await types.ChatActions.typing()
    await bot.send_message(message.chat.id, MESSAGES["hello"])


@dp.message_handler()
async def find_movie(message: types.Message):
    await types.ChatActions.typing()
    media = await handle_request(message.text)
    await bot.send_media_group(message.chat.id, media)


if __name__ == "__main__":
    executor.start_polling(dp)
