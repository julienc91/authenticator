# -*- coding: utf-8 -*-

import os
import os.path

import appdirs
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .database import Base
from .models import OTP


APP_NAME = "authenticator"


def get_db_path():
    base_path = appdirs.user_data_dir(APP_NAME)
    os.makedirs(base_path, mode=0o700, exist_ok=True)
    return os.path.join(base_path, "authenticator.db")


def create_db():
    engine = create_engine(f"sqlite:///{get_db_path()}")
    Base.metadata.create_all(engine)
    return engine


class SessionMakerBuilder:
    _instance = None

    @classmethod
    def __call__(cls, *args, **kwargs) -> Session:
        if not cls._instance:
            cls._instance = sessionmaker(bind=create_db())
        return cls._instance()


SessionMaker = SessionMakerBuilder()

__all__ = [OTP, SessionMaker]
