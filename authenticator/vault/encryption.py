# -*- coding: utf-8 -*-

import uuid

import keyring
import keyring.errors
from sqlalchemy_utils.types.encrypted.padding import InvalidPaddingError

from authenticator.vault.session import SessionMaker
from authenticator.vault.utils import SingletonMetaClass


class EncryptionKeyManager(metaclass=SingletonMetaClass):
    __keyring_namespace = "julienc91/authenticator"
    __keyring_username = "authenticator"
    __key = None

    def unlock(self, key: str, remember: bool = False):
        self.__key = key
        if not self.__check_key():
            self.__key = None
            raise VaultLockedException
        if remember:
            self.__remember_key()
        else:
            self.__forget_key()

    def lock(self):
        self.__forget_key()
        self.__key = None

    @staticmethod
    def is_setup() -> bool:
        from authenticator.vault.models import Config

        session = SessionMaker()
        return not session.query(Config).count()

    def is_locked(self) -> bool:
        if self.__key:
            return False

        self.__key = self.__get_remembered_key()
        if not self.__check_key():
            self.__key = None

        return not self.__key

    def __get_remembered_key(self) -> str:
        try:
            return keyring.get_password(
                self.__keyring_namespace, self.__keyring_username
            )
        except keyring.errors.KeyringError:
            pass

    def __remember_key(self):
        if self.__key:
            try:
                keyring.set_password(
                    self.__keyring_namespace, self.__keyring_username, self.__key
                )
            except keyring.errors.KeyringError:
                pass

    def __forget_key(self):
        try:
            keyring.delete_password(self.__keyring_namespace, self.__keyring_username)
        except keyring.errors.KeyringError:
            pass

    def __check_key(self) -> bool:
        from authenticator.vault.models import Config

        if not self.__key:
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
        if self.is_locked():
            raise VaultLockedException
        return self.__key


def get_encryption_key() -> str:
    return EncryptionKeyManager().get_key()


class VaultLockedException(Exception):
    pass
