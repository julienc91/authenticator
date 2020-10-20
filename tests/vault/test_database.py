# -*- coding: utf-8 -*-

from authenticator.vault.models import OTP
from authenticator.vault.session import SessionMaker


def test_OTP(monkeypatch, unlock_vault):
    uri = "otpauth://totp/test%40authenticator?secret=ThisIsTheSecretKey&issuer=authenticator"
    session = SessionMaker()
    created_instance = OTP(uri=uri)

    session.add(created_instance)
    session.commit()

    assert session.query(OTP).count() == 1
    read_instance = session.query(OTP).filter(OTP.uri == uri).first()
    assert read_instance
    assert read_instance.uri == uri

    monkeypatch.setattr(
        "authenticator.vault.encryption.EncryptionKeyManager.get_key",
        lambda _: "bad_key",
    )

    session = SessionMaker()
    assert session.query(OTP).count() == 1
    read_instance = session.query(OTP).filter(OTP.uri == uri).first()
    assert not read_instance
