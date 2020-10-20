# -*- coding: utf-8 -*-

from authenticator.vault import interface
from authenticator.vault.session import SessionMaker


def test_add_otp(unlock_vault):
    session = SessionMaker()
    uri = "otpauth://totp/test%40authenticator?secret=ThisIsTheSecretKey&issuer=authenticator"
    otp = interface.add_otp(uri, session)
    assert otp
    assert otp.uri == uri
    assert not otp.id

    session.commit()
    assert otp.id


def test_delete_otp(unlock_vault):
    session1 = SessionMaker()
    otp = interface.add_otp("otpauth://totp/?secret=abc", session1)
    session1.commit()

    interface.delete_otp(otp, session1)
    assert len(interface.get_all_otp(session1)) == 0, interface.get_all_otp(session1)
    assert len(interface.get_all_otp(SessionMaker())) == 1

    session1.commit()
    assert len(interface.get_all_otp(session1)) == 0
    assert len(interface.get_all_otp(SessionMaker())) == 0
