# -*- coding: utf-8 -*-

from enum import Enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine, StringEncryptedType

from .encryption import get_encryption_key


Base = declarative_base()


class OTPTypes(Enum):
    TOTP = "totp"


class OTPAlgorithms(Enum):
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA512 = "SHA512"


class OTP(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True)
    uri = Column(StringEncryptedType(key=get_encryption_key, engine=AesEngine, padding="pkcs5"))

    # hybrid attributes for uri parsing?
