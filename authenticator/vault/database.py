# -*- coding: utf-8 -*-

import os
import os.path

import appdirs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


APP_NAME = "authenticator"


def get_db_path():
    base_path = appdirs.user_data_dir(APP_NAME)
    os.makedirs(base_path, mode=0o700, exist_ok=True)
    return os.path.join(base_path, "authenticator.db")


def create_db():
    engine = create_engine(f"sqlite:///{get_db_path()}")
    Base.metadata.create_all(engine)
    return engine
