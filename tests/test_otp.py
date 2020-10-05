# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
from freezegun import freeze_time

from authenticator.otp import TOTP


@pytest.fixture(autouse=True)
def patch_time():
    with freeze_time(datetime(2020, 10, 6, 20, 55, 37)):
        yield


@pytest.mark.parametrize("config, expected", [
    ({}, "884141"),
    ({"interval": 427}, "507832"),
    ({"algorithm": "SHA256"}, "373407"),
    ({"digits": 9}, "939884141")
])
def test_TOTP(config, expected):
    totp = TOTP("ABCDEFGHIJKLMNOP", **config)
    assert totp.generate() == expected
