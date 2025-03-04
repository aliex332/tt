import os
import re
import wda
import base64
import threading
import numpy as np
from PIL import Image
from time import sleep
from requests import post, get
import io

def CaptchaObjects(d, udid):
    try:
        # Получаем координаты элемента
        x1, y1, width, height = d(type='XCUIElementTypeImage', visible=True, enabled=True).get().bounds
        x2 = x1 + width
        y2 = y1 + height

        # Снимаем скриншот в формате Pillow
        full_screenshot = d.screenshot("pillow")

        # Обрезаем изображение до элемента капчи
        element_screenshot = full_screenshot.crop((x1 * 3, y1 * 3, x2 * 3, y2 * 3))

        # Конвертируем обрезанное изображение в Base64
        buffer = io.BytesIO()
        element_screenshot.save(buffer, format="PNG")
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Отправляем изображение на распознавание
        key = 'iN91TtBYMH9oe41w'
        data = {"cap_type": "3d", "image_base64": f"{encoded_image}"}
        r = post(f"http://147.45.135.70:6247/solve/{key}", json=data)

        # Извлекаем координаты для кликов
        x2 = int(x1 + (r.json()['x2']) / 3)
        x1 = int(x1 + (r.json()['x1']) / 3)
        y_one = int(y1 + (r.json()['y1']) / 3)
        y_two = int(y1 + (r.json()['y2']) / 3)

        # Выполняем клики по полученным координатам
        d.click(x1, y_one)
        d.click(x2, y_two)

        # Снимаем новый скриншот после кликов
        full_screenshot = d.screenshot("pillow")

        # Проверка на совпадения пикселей
        image = np.array(full_screenshot)
        matches = np.all(image[:, :, :3] == (253, 44, 84), axis=-1)
        if len(np.argwhere(matches)) > 0:
            center_y, center_x = np.argwhere(matches).mean(axis=0)
            center_x //= 3
            center_y //= 3
            d.click(int(center_x), int(center_y))

    except Exception: d(name='Close').click_exists()