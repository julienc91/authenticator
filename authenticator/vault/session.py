# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session, sessionmaker

from authenticator.vault.database import create_db


class SessionMakerBuilder:
    _instance = None

    @classmethod
    def __call__(cls, *args, **kwargs) -> Session:
        if not cls._instance:
            cls._instance = sessionmaker(bind=create_db())
        return cls._instance()


SessionMaker = SessionMakerBuilder()
