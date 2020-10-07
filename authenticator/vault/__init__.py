# -*- coding: utf-8 -*-

import os.path

import appdirs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import Base


APP_NAME = "authenticator"


def get_db_path():
    return os.path.join(appdirs.user_data_dir(APP_NAME), "authenticator.db")


def create_db():
    engine = create_engine(f"sqlite:///{get_db_path()}")
    Base.metadata.create_all(engine)
    return engine


class SessionMaker:
    _instance = None

    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = sessionmaker(bind=create_db())
        return cls._instance()


__all__ = [SessionMaker]
