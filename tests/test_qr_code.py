# -*- coding: utf-8 -*-

from authenticator import qr_code


def test_read():
    res = qr_code.read("tests/data/qrcode.png")
    assert (
        res
        == "otpauth://totp/test%40authenticator?secret=ThisIsTheSecretKey&issuer=authenticator"
    )


def test_write(tmpdir):
    data = "otpauth://totp/test_write%40authenticator?secret=ThisIsTheSecretKey&issuer=authenticator"
    image = qr_code.write(data)
    assert image

    path = str(tmpdir / "qrcode.png")
    image.save(path)

    res = qr_code.read(path)
    assert res == data
