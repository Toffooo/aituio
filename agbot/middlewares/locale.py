from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class LocaleMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self):
        super().__init__()

    async def pre_process(self, obj, data, *args):
        if not hasattr(obj, "from_user"):
            data["locale"] = None
        else:
            locale, _ = data["orm"].user.get_locale(obj.from_user.id)
            data["locale"] = locale

    async def post_process(self, obj, data, *args):
        del data["locale"]
