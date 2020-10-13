# -*- coding: utf-8 -*-

import pytest

from authenticator.vault import OTP, SessionMaker


@pytest.fixture(autouse=True)
def patch_db_file(monkeypatch, tmpdir):
    db_path = str(tmpdir / "test.db")
    monkeypatch.setattr("authenticator.vault.get_db_path", lambda: db_path)


@pytest.fixture(autouse=True)
def cleanup_db(patch_db_file):
    session = SessionMaker()
    session.query(OTP).delete()
    session.commit()
