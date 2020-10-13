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


def get_all_otp(session: Session) -> List[OTP]:
    return session.query(OTP).all()
