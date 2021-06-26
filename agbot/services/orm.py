from datetime import datetime
from typing import Optional, Tuple

from aiogram.types import Message
from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy_mixins import AllFeaturesMixin
from sqlalchemy_mixins.timestamp import TimestampsMixin

from agbot.models.locale import LOCALE
from agbot.models.role import UserRole
from agbot.services.locale import cast_locale

from .db_conn import base


class BaseModel(base, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)

    def __init__(self, *args, **kwargs):
        pass


class ENTResult(BaseModel):
    __tablename__ = "ent_results"

    category = Column(String(length=255))
    faculty = Column(String(length=255))
    score = Column(Float)
    year = Column(Integer)

    @classmethod
    def match_by_categories(cls):
        cy = int(datetime.now().year)
        data = cls.smart_query(filters={"year": cy - 1}, sort_attrs=["-category"]).all()

        return data


class AETResult(BaseModel):
    __tablename__ = "aet_results"

    title = Column(String(length=255))
    first_exam_link = Column(String(length=255))
    second_exam_link = Column(String(length=255))

    @classmethod
    def truncate(cls):
        [s.delete() for s in cls.all()]

    @classmethod
    def get_results_as_string(cls):
        results = cls.all()
        string = ""

        for item in results:
            string += f"{item.title}\n"
            string += f"1 Модуль: {item.first_exam_link} \n"
            string += f"2 Модуль: {item.second_exam_link} \n\n"

        return string


class Schedule(BaseModel):
    __tablename__ = "schedule"

    descr = Column(String(length=500))

    @classmethod
    def truncate(cls):
        [s.delete() for s in cls.all()]

    @classmethod
    def get(cls):
        match = cls.all()
        return None if len(match) == 0 else match[0]


class User(BaseModel):
    __tablename__ = "users"

    telegram_id = Column(Integer, unique=True)
    username = Column(String(length=255))
    role = Column(String(length=30), default=UserRole.DEFAULT.value)
    active = Column(Boolean, default=True)
    locale = Column(String(length=10), default=None)

    def set_locale(self, locale: LOCALE):
        self.locale = locale.value
        return self.save()

    def cast_locale(self):
        return cast_locale(self.locale) if self.locale is not None else None

    @classmethod
    def get(cls, telegram_id: int):
        user = cls.where(telegram_id=telegram_id).all()
        return None if len(user) == 0 else user[0]

    @classmethod
    def get_locale(cls, telegram_id: int) -> Tuple[Optional["User"], bool]:
        user = cls.get(telegram_id=telegram_id)
        if user is None:
            return None, False
        return cast_locale(user.locale), True

    @classmethod
    def add_from_tg_message(
        cls, data: Message, role: Optional[UserRole] = UserRole.DEFAULT
    ) -> "User":
        instance = cls.create(
            telegram_id=data.chat.id, username=data.chat.username, role=role.value
        )
        return instance

    @classmethod
    def get_or_add_from_tg_message(
        cls, data: Message, role: Optional[UserRole] = UserRole.DEFAULT
    ) -> Tuple["User", bool]:
        is_created = False
        instance = cls.get(telegram_id=data.from_user.id)

        if instance is None:
            instance = cls.create(
                telegram_id=data.from_user.id,
                username=data.from_user.username,
                role=role.value,
            )
            is_created = True

        return instance, is_created
