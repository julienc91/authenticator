# -*- coding: utf-8 -*-

import pyotp


class TOTP:
    def __init__(
        self,
        secret: str,
        issuer: str = None,
        label: str = None,
        interval: int = 30,
        algorithm: str = "SHA1",
        digits: int = 6
    ):
        self.__secret = secret
        self.issuer = issuer
        self.label = label
        self._config = {
            "interval": interval,
            "digest": algorithm,
            "digits": digits
        }
        self._builder = pyotp.TOTP(self.__secret, **self._config)

    def generate(self) -> str:
        return self._builder.now()
