# -*- coding: utf-8 -*-

from typing import List

from sqlalchemy.orm import Session

from .models import OTP


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
