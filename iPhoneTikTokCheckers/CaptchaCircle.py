from PIL import Image, ImageDraw
import io
import requests
import base64
from time import sleep

def CaptchaCircle(d, udid):
    api_key = "881a5c36051375462464d3d808c99036"
    base_url = "http://147.45.135.70:6247/solve/iN91TtBYMH9oe41w"

    def crop_circle_with_inner_hole(img, outer_rect, inner_rect, pixel_plus, pixel_minus):
        """Обрезает изображение до круга с внутренним отверстием."""
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)

        x1, y1, x2, y2 = outer_rect
        x1_inner, y1_inner, x2_inner, y2_inner = inner_rect

        # Внешний круг
        draw.ellipse(
            (x1 - pixel_minus, y1 - pixel_minus, x2 + pixel_minus, y2 + pixel_minus),
            fill=255,
        )
        # Внутреннее отверстие
        draw.ellipse(
            (x1_inner + pixel_plus, y1_inner + pixel_plus, x2_inner - pixel_plus, y2_inner - pixel_plus),
            fill=0,
        )
        # Применяем маску к изображению
        img.putalpha(mask)
        return img.crop(outer_rect)

    def resize_image(img, target_size):
        """Изменяет размер изображения."""
        return img.resize(target_size, Image.ANTIALIAS)

    def convert_to_jpeg_with_white_bg(img):
        """Конвертирует PNG с прозрачным фоном в JPEG с белым фоном."""
        white_bg = Image.new("RGB", img.size, (255, 255, 255))
        white_bg.paste(img, (0, 0), img)
        return white_bg

    def upload_image(img):
        """Загружает изображение на imgbb и возвращает URL."""
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        response = requests.post(
            f"https://api.imgbb.com/1/upload?expiration=600&key={api_key}",
            data={"image": encoded_image},
        )
        if response.status_code == 200:
            return response.json()["data"]["url"]
        return None

    try:
        for _ in range(20):
            # Ожидаем элементы Captcha
            d(xpath='//XCUIElementTypeOther[@name="main"]/XCUIElementTypeImage', visible=True).wait(10)
            sleep(2)
            images = d(xpath='//XCUIElementTypeOther[@name="main"]/XCUIElementTypeImage', visible=True).find_elements()

            # Получаем координаты внешнего и внутреннего кругов
            x, y, width, height = images[0].bounds
            x_inside, y_inside, width_inside, height_inside = images[1].bounds

            outer_rect = (x * 3, y * 3, (x + width) * 3, (y + height) * 3)
            inner_rect = (x_inside * 3, y_inside * 3, (x_inside + width_inside) * 3, (y_inside + height_inside) * 3)

            # Снимаем скриншот в формате Pillow
            img = d.screenshot("pillow")

            # Обрезаем и обрабатываем внешнюю и внутреннюю области
            outer_circle = crop_circle_with_inner_hole(img.copy(), outer_rect, inner_rect, 0, 3)
            inner_circle = crop_circle_with_inner_hole(img.copy(), inner_rect, (0, 0, 0, 0), 0, 5)

            # Изменяем размер изображений
            outer_circle = resize_image(outer_circle, (324, 324))
            inner_circle = resize_image(inner_circle, (217, 217))

            # Конвертируем в JPEG с белым фоном
            outer_jpeg = convert_to_jpeg_with_white_bg(outer_circle)
            inner_jpeg = convert_to_jpeg_with_white_bg(inner_circle)

            # Загружаем изображения на imgbb
            image_url_outer = upload_image(outer_jpeg)
            image_url_inner = upload_image(inner_jpeg)

            if not image_url_outer or not image_url_inner:
                raise Exception("Image upload failed")

            # Отправляем на сервер решение капчи
            response = requests.post(
                base_url,
                json={"url1": image_url_outer, "url2": image_url_inner},
            )
            drag_data = response.json()
            drag_to = drag_data["slider_pixs"]

            # Выполняем перетаскивание
            drag_element = d(xpath='//XCUIElementTypeImage', visible=True).find_elements()
            x_center, y_center = drag_element[-1].bounds.center

            d.drag(x_center, y_center, x_center + drag_to, y_center, duration=1.5)

            if d(name="Unable to verify. Please try again.").exists: continue
            break
    except Exception: d(name="Close").click_exists()