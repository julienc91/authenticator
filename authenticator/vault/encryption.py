# -*- coding: utf-8 -*-

import uuid

from sqlalchemy_utils.types.encrypted.padding import InvalidPaddingError

from authenticator.vault.session import SessionMaker
from authenticator.vault.utils import SingletonMetaClass


class EncryptionKeyManager(metaclass=SingletonMetaClass):
    __key = None

    def unlock(self, key: str):
        self.__key = key
        if not self.__check_key():
            self.__key = None
            raise VaultLockedException

    def lock(self):
        self.__key = None

    def is_locked(self) -> bool:
        return not self.__key

    def __check_key(self) -> bool:
        from authenticator.vault.models import Config

        if self.is_locked():
            return False

        session = SessionMaker()
        if session.query(Config).count() > 1:
            session.query(Config).order_by("id")[1:].delete()

        try:
            config = session.query(Config).first()
        except InvalidPaddingError:
            # invalid key
            return False

        if config:
            return config.clear_check == config.encrypted_check

        # first run
        check_value = str(uuid.uuid4())
        config = Config(clear_check=check_value, encrypted_check=check_value)
        session.add(config)
        session.commit()
        return True

    def get_key(self) -> str:
        if not self.__key:
            raise VaultLockedException
        return self.__key


def get_encryption_key() -> str:
    return EncryptionKeyManager().get_key()


class VaultLockedException(Exception):
    pass
