# -*- coding: utf-8 -*-


class EncryptionKeyManager:
    def __init__(self):
        self._key = "foo"

    def __call__(self):
        return self._key


key_manager = EncryptionKeyManager()


def get_encryption_key():
    return key_manager()
