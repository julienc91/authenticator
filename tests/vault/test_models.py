# -*- coding: utf-8 -*-

from datetime import datetime

import pytest
from freezegun import freeze_time

from authenticator.vault.models import OTP, OTPAlgorithms, OTPTypes


@pytest.fixture()
def patch_time():
    with freeze_time(datetime(2020, 10, 6, 20, 55, 37)):
        yield


@pytest.mark.parametrize(
    "parameters, expected",
    [
        ({}, "otpauth://totp/?secret=SeCrEt&algorithm=SHA1"),
        ({"label": "foo@bar"}, "otpauth://totp/foo%40bar?secret=SeCrEt&algorithm=SHA1"),
        (
            {"issuer": "foo"},
            "otpauth://totp/foo:?secret=SeCrEt&issuer=foo&algorithm=SHA1",
        ),
        (
            {"algorithm": OTPAlgorithms.SHA512},
            "otpauth://totp/?secret=SeCrEt&algorithm=SHA512",
        ),
        ({"digits": 8}, "otpauth://totp/?secret=SeCrEt&algorithm=SHA1&digits=8"),
        ({"interval": 50}, "otpauth://totp/?secret=SeCrEt&algorithm=SHA1&period=50"),
    ],
)
def test_OTP_create_uri(parameters, expected):
    base_parameters = {"secret": "SeCrEt", "type_": OTPTypes.TOTP}
    base_parameters.update(parameters)
    res = OTP.create_uri(**base_parameters)
    assert res == expected


@pytest.mark.parametrize("issuer", [None, "foo"])
@pytest.mark.parametrize("label", [None, "bar"])
@pytest.mark.parametrize("digits", [6, 8])
@pytest.mark.parametrize("interval", [30, 45])
@pytest.mark.parametrize("algorithm", OTPAlgorithms)
def test_OTP_properties(issuer, label, digits, interval, algorithm):
    base_parameters = {"secret": "SeCrEt", "type_": OTPTypes.TOTP}
    parameters = {
        "issuer": issuer,
        "label": label,
        "digits": digits,
        "interval": interval,
        "algorithm": algorithm,
    }
    base_parameters.update(parameters)
    uri = OTP.create_uri(**base_parameters)
    otp = OTP(uri=uri)
    for key, value in parameters.items():
        assert getattr(otp, key) == value, key
    assert otp.type is base_parameters["type_"]


@pytest.mark.parametrize(
    "parameters, expected",
    [
        ({}, "884141"),
        ({"interval": 427}, "507832"),
        ({"algorithm": OTPAlgorithms.SHA256}, "373407"),
    ],
)
def test_OTP_generate(patch_time, parameters, expected):
    base_parameters = {"secret": "ABCDEFGHIJKLMNOP", "type_": OTPTypes.TOTP}
    base_parameters.update(parameters)
    uri = OTP.create_uri(**base_parameters)
    totp = OTP(uri=uri)
    assert totp.generate() == expected
