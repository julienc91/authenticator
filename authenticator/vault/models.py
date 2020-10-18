# -*- coding: utf-8 -*-

import time
from enum import Enum
from urllib.parse import parse_qsl, ParseResult, unquote, urlparse

import pyotp
from pyotp.utils import build_uri
from sqlalchemy import Column, Integer
from sqlalchemy.orm import validates
from sqlalchemy_utils.types.encrypted.encrypted_type import (
    AesEngine,
    StringEncryptedType,
)

from .database import Base
from .encryption import get_encryption_key


class OTPTypes(Enum):
    TOTP = "totp"


class OTPAlgorithms(Enum):
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA512 = "SHA512"


DEFAULT_DIGITS = 6
DEFAULT_INTERVAL = 30
DEFAULT_ALGORITHM = OTPAlgorithms.SHA1


class OTP(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True)
    uri = Column(
        StringEncryptedType(key=get_encryption_key, engine=AesEngine, padding="pkcs5")
    )

    @classmethod
    def create_uri(
        cls,
        type_: OTPTypes,
        secret: str,
        label: str = None,
        issuer: str = None,
        interval: int = DEFAULT_INTERVAL,
        algorithm: OTPAlgorithms = DEFAULT_ALGORITHM,
        digits: int = DEFAULT_DIGITS,
    ):
        label = label or ""
        initial_count = None if type_ is OTPTypes.TOTP else 0
        return build_uri(
            secret, label, initial_count, issuer, algorithm.value, digits, interval
        )

    @classmethod
    def is_uri_valid(cls, uri: str) -> bool:
        try:
            pyotp.parse_uri(uri)
        except ValueError:
            return False
        return True

    def __repr__(self):
        return f"<OTP {self.id} - {self.issuer}:{self.label}>"

    def __str__(self):
        return f"<OTP {self.issuer}:{self.label}>"

    @validates("uri")
    def validate_uri(self, _, value):
        if not self.is_uri_valid(value):
            raise ValueError("invalid URI")
        return value

    @property
    def _parsed_uri(self) -> ParseResult:
        return urlparse(self.uri)

    @property
    def _parsed_parameters(self) -> dict:
        return dict(parse_qsl(self._parsed_uri.query))

    @property
    def __secret(self) -> str:
        return self._parsed_parameters["secret"]

    @property
    def type(self) -> OTPTypes:
        return OTPTypes(self._parsed_uri.netloc)

    @property
    def issuer(self) -> str:
        return self._parsed_parameters.get("issuer") or None

    @property
    def label(self) -> str:
        return unquote(self._parsed_uri.path.lstrip("/").split(":", 1)[-1]) or None

    @property
    def interval(self) -> int:
        return int(self._parsed_parameters.get("period") or DEFAULT_INTERVAL)

    @property
    def algorithm(self) -> OTPAlgorithms:
        try:
            return OTPAlgorithms[self._parsed_parameters["algorithm"]]
        except KeyError:
            return DEFAULT_ALGORITHM

    @property
    def digits(self) -> int:
        return int(self._parsed_parameters.get("digits") or DEFAULT_DIGITS)

    @property
    def _builder(self) -> pyotp.TOTP:
        config = {
            "interval": self.interval,
            "digest": self.algorithm.value,
            "digits": self.digits,
        }
        return pyotp.TOTP(self.__secret, **config)

    def generate(self) -> str:
        return self._builder.now()

    def get_next_change_timeout(self) -> float:
        timestamp = time.time()
        interval = self.interval
        return interval - (timestamp % interval)
