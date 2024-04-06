from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from os import remove
from qrcode import make as qr_make

from asyncio import run as async_run


class QRCodeBot(Bot):

    def __init__(self):
        super().__init__(
            token="TOKEN"
        )


class Dp(Dispatcher):

    def __init__(self):
        super().__init__()


dp = Dp()
bot = QRCodeBot()


@dp.message(Command("gen_qr_code"))
async def gen_qr_code(msg: types.Message, command: CommandObject) -> None:
    code = qr_make(command.args)
    code.save(f"cache/{msg.from_user.username}.png")

    await msg.reply_photo(photo=types.BufferedInputFile.from_file(path=f"cache/{msg.from_user.username}.png"))

    remove(f"cache/{msg.from_user.username}.png")


@dp.message()
async def echo(msg: types.Message):
    if "https://" not in msg.text and "/gen_qr_code" in msg.text:
        await msg.reply("Для команды /gen_qr_code необходимо указать url, который должен хранить QR код.")
    else:
        await msg.reply("Что?")


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    async_run(main())
