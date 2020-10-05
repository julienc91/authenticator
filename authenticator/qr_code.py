# -*- coding: utf-8 -*-

import cv2
import qrcode
from PIL import Image


def read(path: str) -> str:
    """
    Read the content of a QR Code
    :param path: path to the QR Code image file
    :return: the QR Code content
    """
    image = cv2.imread(path)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)
    return data


def write(data: str) -> Image:
    """
    Create a new QR Code as an Image, containing the given data
    :param data: the data to write in the QR Code
    :return: the created Image object
    """
    builder = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_H)
    builder.add_data(data)
    return builder.make_image(fill_color="black", back_color="white").convert("RGB")
