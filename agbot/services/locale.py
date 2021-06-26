import json
from dataclasses import dataclass
from typing import Dict, List, Optional

from agbot.models.locale import LOCALE
from settings import ABS_PATH

from aiogram.types import (  # isort:skip
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


@dataclass
class DialogButton:
    text: str
    callback_data: str

    def initialize(self):
        return InlineKeyboardButton(text=self.text, callback_data=self.callback_data)


@dataclass
class DialogItem:
    text: str
    buttons: List[DialogButton]

    @classmethod
    def fill(cls, text: str, buttons: List[Dict[str, str]]):
        return DialogItem(
            text=text,
            buttons=[
                DialogButton(text=bt["text"], callback_data=bt["callback_data"])
                for bt in buttons
            ],
        )

    def get_markup(self):
        buttons = [bt.initialize() for bt in self.buttons]
        return InlineKeyboardMarkup(row_width=1).add(*buttons)

    def format_lazy(self, *args):
        if len(args) == 0:
            return self.text
        return self.text.format(*args)


def cast_locale(locale_string: str):
    if locale_string == "ru_RU":
        return LOCALE.ru
    elif locale_string == "kz_KZ":
        return LOCALE.kz


def get_dialog_dist(locale: LOCALE):
    path = f"{ABS_PATH}/agbot/LOCALE/{locale.value}/dist.json"
    with open(path, "r") as f:
        data = json.load(f)
    return data


class Dialog:
    def __init__(self, locale: Optional[LOCALE] = LOCALE.ru) -> None:
        self.locale = locale
        self._dialog = get_dialog_dist(self.locale)

    def _get_text(self, context):
        return self._dialog[context]["text"] + self._dialog["_add"]["text"]

    def welcome(self, is_have_locale: Optional[LOCALE] = None):
        context = "welcome"
        if is_have_locale is None:
            context = "welcome_wo_locale"

        return DialogItem.fill(
            text=self._get_text(context), buttons=self._dialog[context]["buttons"]
        )

    def ent(self):
        context = "ent_results"
        return DialogItem.fill(
            text=self._get_text(context), buttons=self._dialog[context]["buttons"]
        )

    def scolar(self):
        context = "scolarship_instr"
        return DialogItem.fill(
            text=self._get_text(context), buttons=self._dialog[context]["buttons"]
        )

    def job_image(self):
        context = "jobs_image"
        return DialogItem.fill(
            text=self._get_text(context), buttons=self._dialog[context]["buttons"]
        )

    def important_dates(self):
        context = "important_dates"
        return DialogItem(
            text=self._get_text(context), buttons=self._dialog[context]["buttons"]
        )

    def aet_results(self):
        context = "aet_results"
        return DialogItem.fill(
            text=self._get_text(context), buttons=self._dialog[context]["buttons"]
        )
