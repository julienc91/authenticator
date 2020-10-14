# -*- coding: utf-8 -*-

import math

import cv2
import qrcode
import zbar
from PIL import Image


def read(path: str) -> str:
    """
    Read the content of a QR Code
    :param path: path to the QR Code image file
    :return: the QR Code content
    """
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    scanner = zbar.Scanner()
    results = scanner.scan(image)
    if not results:
        return ""

    def perimeter(coordinates) -> float:
        res = 0
        x, y = coordinates[0]
        for x2, y2 in coordinates[1:]:
            res += math.sqrt((x - x2) ** 2 + (y - y2) ** 2)
            x, y = x2, y2
        return res

    results.sort(key=lambda r: (r.quality, perimeter(r.position)), reverse=True)
    return results[0].data.decode()


def write(data: str) -> Image:
    """
    Create a new QR Code as an Image, containing the given data
    :param data: the data to write in the QR Code
    :return: the created Image object
    """
    builder = qrcode.QRCode(error_correction=qrcode.ERROR_CORRECT_H)
    builder.add_data(data)
    return builder.make_image(fill_color="black", back_color="white").convert("RGB")
