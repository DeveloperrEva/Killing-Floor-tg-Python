from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import BoundFilter

import config


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in config.admin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
