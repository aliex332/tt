import base64
import requests
from time import sleep


def CaptchaSolver(d, udid):
    for _ in range(5):
        if d(nameMatches='Select 2 objects').exists: print(f'[{udid}] || Letters type found. Solving, please wait...')
        if d(nameMatches='Drag the slider').exists: print(f'[{udid}] || Circle type found. Solving, please wait...')
        if d(nameMatches='Drag the puzzle').exists: print(f'[{udid}] || Slider type found. Solving, please wait...')
        if d(nameMatches='Which of these objects').exists: print(f'[{udid}] || Objects type found. Solving, please wait...')

        d.screenshot('pillow')
        image_base64 = base64.b64encode(d.screenshot(format='raw')).decode('utf-8')

        url = "http://217.28.222.220:6777/api/request"
        headers = {
            "Authorization": "iN91TtBYMH9oe41w",
            "Content-Type": "application/json"
        }
        data = {
            "image_type": "base64",
            "base64": image_base64
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 429: print(f'[{udid}] || Too many requests, try again in few seconds, please wait...'); sleep(20); continue
        elif response.status_code == 200: response_data = response.json(); break
        elif response.status_code != 200: print(f'[{udid}] || Captcha service is not available. Please check your internet connection. Try again in few seconds, please wait...'); sleep(2); continue
        else: print(f'[{udid}] || Captcha service is not available. Please check your internet connection. Try again in few seconds, please wait...'); sleep(2); continue

    if response_data.get("action") == "slide":
        x1 = int(response_data.get("x1", 0) / 3)
        x2 = int(response_data.get("x2", 0) / 3)
        y1 = int(response_data.get("y1", 0) / 3)
        y2 = int(response_data.get("y2", 0) / 3)
        d.drag(x1, y1, x2 * 0.89, y1)

    if response_data.get("action") == "click":
        x1 = int(response_data.get("x1", 0) / 3)
        x2 = int(response_data.get("x2", 0) / 3)
        x3 = int(response_data.get("x3", 0) / 3)
        y1 = int(response_data.get("y1", 0) / 3)
        y2 = int(response_data.get("y2", 0) / 3)
        y3 = int(response_data.get("y3", 0) / 3)
        d.click(x1, y1)
        d.click(x2, y2)
        d.click(x3, y3)

    d.visible_button_click_exist('red')