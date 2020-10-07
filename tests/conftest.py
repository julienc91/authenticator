# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(autouse=True)
def patch_db_file(monkeypatch, tmpdir):
    db_path = str(tmpdir / "test.db")
    monkeypatch.setattr("authenticator.vault.get_db_path", lambda: db_path)
