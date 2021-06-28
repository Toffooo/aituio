from datetime import datetime

from aiogram.types import CallbackQuery

from aitu_data_extractors.site import get_jobs_image
from settings import ABS_PATH


class BaseScenario:
    def __init__(self, dialog, setup_methods) -> None:
        self.dialog = dialog
        self._setup, self._setup_callback = setup_methods
        self.ctx = None
        self.bot = None
        self.user = None

    async def _class_setup(self, user_id: int):
        self.ctx = self._setup()
        self.bot, self.user = self._setup_callback(user_id)

    async def back_to_welcome(self, callback_query: CallbackQuery):
        await self._class_setup(callback_query.from_user.id)
        await self.bot.answer_callback_query(callback_query.id)

        context = self.dialog.welcome(self.user.locale)
        message = context.format_lazy(self.user.username)
        markup = context.get_markup()

        await self.bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=message,
            reply_markup=markup,
        )


class DocsScenario(BaseScenario):
    async def get_docs_handler(self, callback_query: CallbackQuery):
        await self._class_setup(callback_query.from_user.id)
        await self.bot.answer_callback_query(callback_query.id)

        with open(f"{ABS_PATH}/agbot/Resources/docs.jpg", "rb") as photo:
            await self.bot.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=photo,
            )


class AETResultsScenario(BaseScenario):
    async def get_aet_resutls_handler(self, callback_query: CallbackQuery):
        await self._class_setup(callback_query.from_user.id)
        await self.bot.answer_callback_query(callback_query.id)

        aet_links = self.ctx["orm"].aet.get_results_as_string()

        context = self.dialog.aet_results()
        message = context.format_lazy(aet_links)
        markup = context.get_markup()

        await self.bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=message,
            reply_markup=markup,
        )


class ImportantDatesScenario(BaseScenario):
    async def get_important_dates_handler(self, callback_query: CallbackQuery):
        await self._class_setup(callback_query.from_user.id)
        await self.bot.answer_callback_query(callback_query.id)

        important_dates = self.ctx["orm"].dates.get()

        dates = (
            "Something went wrong. Try this feature later."
            if important_dates is None
            else important_dates.descr
        )

        context = self.dialog.job_image()
        message = context.format_lazy(dates)
        markup = context.get_markup()

        await self.bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=message,
            reply_markup=markup,
        )


class JobsImageScenario(BaseScenario):
    async def get_jobs_image_handler(self, callback_query: CallbackQuery):
        await self._class_setup(callback_query.from_user.id)
        await self.bot.answer_callback_query(callback_query.id)

        img_href, _ = get_jobs_image(static=True)
        if img_href is None:
            img_href = "Something went wrong. Please try this funciton later."

        context = self.dialog.job_image()
        message = context.format_lazy(img_href)
        markup = context.get_markup()

        await self.bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=message,
            reply_markup=markup,
        )


class ScolarScenario(BaseScenario):
    async def send_scolar_instr(self, callback_query: CallbackQuery):
        await self._class_setup(callback_query.from_user.id)
        await self.bot.answer_callback_query(callback_query.id)

        context = self.dialog.scolar()
        message = context.format_lazy()
        markup = context.get_markup()

        await self.bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=message,
            reply_markup=markup,
        )


class ENTScenario(BaseScenario):
    async def send_past_year_ent_results(self, callback_query: CallbackQuery):
        await self._class_setup(callback_query.from_user.id)
        await self.bot.answer_callback_query(callback_query.id)

        data = self.ctx["orm"].ent.match_by_categories()
        context = self.dialog.ent()
        message = context.format_lazy(datetime.now().year - 1)
        markup = context.get_markup()

        _string = "\n\n"
        prev_category = None

        for item in data:
            if prev_category is None:
                _string += f"{item.category} \n"
            elif prev_category != item.category:
                _string += f"\n{item.category} \n"

            prev_category = item.category
            _string += f"{item.faculty}: {item.score}\n"

        await self.bot.edit_message_text(
            message_id=callback_query.message.message_id,
            chat_id=callback_query.message.chat.id,
            text=message + _string,
            reply_markup=markup,
        )
