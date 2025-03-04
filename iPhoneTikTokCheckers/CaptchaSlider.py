import os
import re
import wda
import base64
import threading
from PIL import Image
from time import sleep
from cprint import cprint
from requests import post, get
import io

def CaptchaSlider(d, udid):
    try:
        for _ in range(20):
            not_solved = 0
            # Ждём появления капчи
            d(name='captcha_whirl_title', visible=True).wait(10)

            # Снимаем скриншот в формате Pillow
            full_screenshot = d.screenshot("pillow")

            # Получаем координаты элемента капчи
            x1, y1, width, height = d(name='captcha_whirl_title', visible=True).get().bounds
            x2 = x1 + width
            y2 = y1 + height

            # Обрезаем изображение до капчи
            captcha_image = full_screenshot.crop((x1 * 3, y1 * 3, x2 * 3, y2 * 3))

            # Конвертируем в Base64
            buffer = io.BytesIO()
            captcha_image.save(buffer, format="PNG")
            encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Отправляем изображение на распознавание
            key = '0965042b2aae41d087a290faa95175ff'
            data = {
                'textinstructions': 'slider',
                'click': 'geetest',
                'json': '1',
                'key': key,
                'method': 'base64',
                'body': encoded_image
            }
            response = post("https://api.cap.guru/in.php", data=data)
            rt = response.json()['request']
            sleep(2)

            # Получаем координаты из решения капчи
            url = f'http://api.cap.guru/res.php?key={key}&id={rt}&json=1'
            result_response = get(url)
            coord = re.findall(r'x=(\d*)', result_response.json()['request'])
            coord = int(int(coord[0]) / 3)

            # Ищем элемент для перетаскивания
            drag_element = d(xpath='//XCUIElementTypeImage', visible=True).find_elements()
            x, y = drag_element[-1].bounds.center

            # Выполняем перетаскивание
            d.drag(x - 1, y, coord + x / 2, y, 1.5)

            # Проверяем, решена ли капча
            for _ in range(20):
                sleep(0.1)
                if d(name='Unable to verify. Please try again.').exists:
                    cprint.fatal(f'[{udid}] || Captcha slider not solving!')
                    not_solved = 1
                    break
            if d(name='Drag the puzzle piece into place').exists: continue
            if not_solved == 0:
                cprint.info(f'[{udid}] || Captcha slider solved!')
                break
    except Exception: d(name='Close').click_exists()