# -*- coding: utf-8 -*-

from authenticator.vault import SessionMaker
from authenticator.vault.database import OTP


def test_OTP(monkeypatch):
    uri = "otpauth://totp/test%40authenticator?secret=ThisIsTheSecretKey&issuer=authenticator"
    session = SessionMaker.get()
    created_instance = OTP(uri=uri)

    session.add(created_instance)
    session.commit()

    assert session.query(OTP).count() == 1
    read_instance = session.query(OTP).filter(OTP.uri == uri).first()
    assert read_instance
    assert read_instance.uri == uri

    monkeypatch.setattr("authenticator.vault.encryption.key_manager._key", "bad_key")

    session = SessionMaker.get()
    assert session.query(OTP).count() == 1
    read_instance = session.query(OTP).filter(OTP.uri == uri).first()
    assert not read_instance
