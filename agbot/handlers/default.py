from aiogram import Bot, Dispatcher
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery, Message

from agbot.services.conversation import (
    AETResultsScenario,
    ENTScenario,
    ImportantDatesScenario,
    JobsImageScenario,
    ScolarScenario,
)
from agbot.services.locale import Dialog, cast_locale
from agbot.services.orm import User

dialog = Dialog()
gl_bot = []


def get_safe_gl_bot():
    if len(gl_bot) == 0:
        return None
    return gl_bot[0]


def _setup():
    META = ctx_data.get()
    dialog.locale = META["locale"]
    return META


def _setup_callback(user_id: int):
    bot = get_safe_gl_bot()
    user = User.get(user_id)
    return bot, user


async def default_start(msg: Message):
    _setup()

    user, _ = User.get_or_add_from_tg_message(data=msg)
    context = dialog.welcome(user.locale)
    message = context.format_lazy(user.username)
    markup = context.get_markup()

    await msg.reply(message, reply_markup=markup)


async def select_locale(callback_query: CallbackQuery):
    _setup()
    bot, user = _setup_callback(callback_query.from_user.id)
    locale = cast_locale(callback_query.data)

    await bot.answer_callback_query(callback_query.id)

    user.set_locale(locale)
    context = dialog.welcome(user.locale)
    message = context.format_lazy(user.username)
    markup = context.get_markup()

    await bot.edit_message_text(
        message_id=callback_query.message.message_id,
        chat_id=callback_query.message.chat.id,
        text=message,
        reply_markup=markup,
    )


def register_default(dp: Dispatcher):
    dp.register_message_handler(
        default_start,
        commands=["start"],
        state="*",
    )


def register_default_callback_handlers(dp: Dispatcher, bot: Bot):
    gl_bot.append(bot)

    _ent = ENTScenario(dialog=dialog, setup_methods=(_setup, _setup_callback))
    _scolar = ScolarScenario(dialog=dialog, setup_methods=(_setup, _setup_callback))
    _jbimg = JobsImageScenario(dialog=dialog, setup_methods=(_setup, _setup_callback))
    _impd = ImportantDatesScenario(
        dialog=dialog, setup_methods=(_setup, _setup_callback)
    )
    _aetsc = AETResultsScenario(dialog=dialog, setup_methods=(_setup, _setup_callback))

    dp.register_callback_query_handler(
        select_locale, lambda c: (c.data == "ru_RU" or c.data == "kz_KZ"), state="*"
    )

    # ENT
    dp.register_callback_query_handler(
        _ent.send_past_year_ent_results, lambda c: c.data == "_ent_ly_res", state="*"
    )

    # Scolar
    dp.register_callback_query_handler(
        _scolar.send_scolar_instr,
        lambda c: c.data.lower() == "_scolar_instr",
        state="*",
    )

    # Jobs image
    dp.register_callback_query_handler(
        _jbimg.get_jobs_image_handler,
        lambda c: c.data.lower() == "_jobs_get",
        state="*",
    )

    # Important dates
    dp.register_callback_query_handler(
        _impd.get_important_dates_handler,
        lambda c: c.data.lower() == "_important_dates",
        state="*",
    )

    # AET results
    dp.register_callback_query_handler(
        _aetsc.get_aet_resutls_handler,
        lambda c: c.data.lower() == "_aet_results",
        state="*",
    )

    # Back
    dp.register_callback_query_handler(
        _ent.back_to_welcome,  # _ent class has taken as one of the option. All other classes have the same .back_to_welcome method
        lambda c: "backtw" in c.data.lower(),
    )
