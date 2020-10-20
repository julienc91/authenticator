# -*- coding: utf-8 -*-

import pytest

from authenticator.vault.encryption import EncryptionKeyManager
from authenticator.vault.models import OTP
from authenticator.vault.session import SessionMaker


@pytest.fixture(autouse=True)
def patch_db_file(monkeypatch, tmpdir):
    db_path = str(tmpdir / "test.db")
    monkeypatch.setattr("authenticator.vault.database.get_db_path", lambda: db_path)


@pytest.fixture(autouse=True)
def cleanup_db(patch_db_file):
    session = SessionMaker()
    session.query(OTP).delete()
    session.commit()


@pytest.fixture()
def unlock_vault():
    EncryptionKeyManager().unlock("foo")
    yield
    EncryptionKeyManager().lock()
