# -*- coding: utf-8 -*-

from typing import List

import pyotp
from sqlalchemy.orm import Session

from authenticator.vault.models import OTP


def is_uri_valid(uri: str) -> bool:
    return OTP.is_uri_valid(uri)


def update_otp(otp: OTP, **kwargs):
    parsed_otp = pyotp.parse_uri(otp.uri)
    for k, v in kwargs.items():
        if k == "issuer":
            parsed_otp.issuer = v
        elif k == "label":
            parsed_otp.name = v
        else:
            raise KeyError(f"Invalid parameter {k}")
    uri = parsed_otp.provisioning_uri()
    otp.uri = uri


def add_otp(uri: str, session: Session) -> OTP:
    otp = OTP(uri=uri)
    session.add(otp)
    return otp


def delete_otp(otp: OTP, session: Session) -> None:
    session.delete(otp)


def get_all_otp(session: Session, search: str = None) -> List[OTP]:
    otps = session.query(OTP).all()
    if search:
        search = search.lower()
        otps = [
            otp
            for otp in otps
            if search in otp.issuer.lower() or search in otp.label.lower()
        ]
    return otps
