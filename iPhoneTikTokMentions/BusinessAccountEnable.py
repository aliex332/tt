import wda
import os
import random
import subprocess
import pytesseract
from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from iPhoneTikTokRegister.api_SMShub import GetNumber, GetSMS
from iPhoneControl.iPhoneControl import iPhone_CopyPhotoVideo

import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def find_text_coordinates(d, udid, target_text, occurrence=1, coordinates=False):
    """
    Функция для поиска текста и возврата средней координаты его нахождения.

    :param image_path: Путь к изображению.
    :param target_text: Строка текста, которую нужно найти (слова разделяются пробелами).
    :return: Центральная координата (x, y) найденной строки, если текст найден. Иначе - None.
    """
    sleep(0.5)
    d.screenshot(f'{udid}.png')
    image_path = f'{udid}.png'
    # Шаг 1: Открываем изображение и улучшаем его
    image = Image.open(image_path).convert('L')
    image = ImageEnhance.Contrast(image).enhance(5).filter(ImageFilter.MedianFilter()).point(lambda p: p > 128 and 255)

    # Шаг 2: Распознаем текст и получаем данные с координатами
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # Преобразуем строку в список слов, разделяя их по пробелам
    target_words = target_text.split()

    # Счётчик найденных совпадений
    found_occurrences = 0

    # Шаг 3: Проходим по всем распознанным словам и ищем совпадение строки
    for i in range(len(data['text']) - len(target_words) + 1):  # Вычитаем длину строки, чтобы не выйти за пределы массива
        # Проверяем наличие всех слов подрядs
        found = True
        for j in range(len(target_words)):
            if data['text'][i + j].strip() != target_words[j]:
                found = False
                break

        if found:
            found_occurrences += 1  # Увеличиваем счётчик найденных вхождений

            if found_occurrences == occurrence:  # Если найденное вхождение совпадает с запрошенным
                # print(f"Текст найден: {' '.join(data['text'][i:i + len(target_words)])}")

                # Координаты первого и последнего слова
                x1 = data['left'][i] // 3
                y1 = data['top'][i] // 3
                x2 = data['left'][i + len(target_words) - 1] // 3
                y2 = data['top'][i + len(target_words) - 1] // 3

                # Вычисляем среднюю координату
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # Выводим средние координаты
                # print(f"Центральная координата: x: {center_x}, y: {center_y}")
                if coordinates == False: d.click(center_x, center_y); return True
                if coordinates == True: return True, center_x, center_y

    # print(f"Текст '{target_text}' вхождение №{occurrence} не найден.")
    return False
def BusinessRegister(d, udid):
    d.open_url('snssdk1233://webview?url=https://lf-main-gecko-source.tiktokcdn.com/obj/byte-gurd-source-sg/10/gecko/resource/tiktok_ba_pia/registration.html?_pia_=1&gecko_channel=tiktok_ba_pia&gecko_bundle=registration.html')
    while find_text_coordinates(d, udid, f"Basic information", occurrence=1) is False:
        if find_text_coordinates(d, udid, "Not approved", occurrence=1) is True: cprint.fatal(f'[{udid}] || Business Account register is not approved!'); return False
        if find_text_coordinates(d, udid, "Registration information", occurrence=1) is True:
            cprint.info(f'[{udid}] || Business Account register is success!')
            d.app_stop('com.zhiliaoapp.musically')
            d.app_start('com.zhiliaoapp.musically')
            sleep(2)
            d(name='Profile', visible=True).click_exists()
            return True
        if d(name='Build trust on TikTok').exists: break

    d.app_stop('com.zhiliaoapp.musically')
    d.app_start('com.zhiliaoapp.musically')
    sleep(2)
    d(name='Profile', visible=True).click_exists()

    cprint.warn(f'[{udid}] || Business Account register start!')
    documents_folders = os.listdir(f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Business/Documents')
    random.shuffle(documents_folders)
    print(f'[{udid}] || Documents copy. Folder name: {documents_folders[0]}')

    if documents_folders[0] == 'Articore':
        business_name = 'ARTICORE GROUP LIMITED'
        business_country_name = 'Australia'
        business_address = 'DOCKLANDS VIC 3008'
        business_state = 'Victoria'
        business_city = 'Melbourne'
        business_postal_code = '3008'
        business_license_id = '11 119 200 592'

    d.open_url('snssdk1233://webview?url=https://lf-main-gecko-source.tiktokcdn.com/obj/byte-gurd-source-sg/10/gecko/resource/tiktok_ba_pia/registration.html?_pia_=1&gecko_channel=tiktok_ba_pia&gecko_bundle=registration.html')
    while find_text_coordinates(d, udid, f"Basic information", occurrence=1) is False:
        if find_text_coordinates(d, udid, "Not approved", occurrence=1) is True: cprint.fatal(f'[{udid}] || Business Account register is not approved!'); return False
        if find_text_coordinates(d, udid, "Registration information", occurrence=1) is True:
            cprint.info(f'[{udid}] || Business Account register is success!')
            d.app_stop('com.zhiliaoapp.musically')
            d.app_start('com.zhiliaoapp.musically')
            sleep(2)
            d(name='Profile', visible=True).click_exists()
            return True
        if d(name='Build trust on TikTok').exists:
            y = d(nameMatches='By continuing').get().bounds.y
            x = d(nameMatches='Get started').get().bounds.x
            d.click(x, y)
            d(name='Get started').click()

    find_text_coordinates(d, udid, "Business name", occurrence=1)
    d.send_keys(f'{business_name}\n')

    find_text_coordinates(d, udid, "Business address", occurrence=1)
    d.send_keys(f'{business_address}\n')

    find_text_coordinates(d, udid, "Select", occurrence=1)
    if find_text_coordinates(d, udid, "Select country or region", occurrence=1) is True:
        while find_text_coordinates(d, udid, f"{business_country_name}", occurrence=1) is False: d.swipe_up()

    find_text_coordinates(d, udid, "Search", occurrence=1)
    if find_text_coordinates(d, udid, "Select", occurrence=1) is True: d.send_keys(f'{business_state[:-1]}\n')
    find_text_coordinates(d, udid, f"{business_state}", occurrence=1)

    d.swipe(0.5, 0.9, 0.5, 0.1, 0.01)
    find_text_coordinates(d, udid, "Search", occurrence=1)
    if find_text_coordinates(d, udid, "Select", occurrence=1) is True: d.send_keys(f'{business_city[:-1]}\n')
    find_text_coordinates(d, udid, f"{business_city}", occurrence=1)

    d.swipe(0.5, 0.9, 0.5, 0.1, 0.01)
    _, x, y = find_text_coordinates(d, udid, 'Next', occurrence=1, coordinates=True)

    find_text_coordinates(d, udid, "Selecty", occurrence=1)
    country_iso_code, country_name, mobile_number, api_sms_hub = GetNumber(udid)
    if find_text_coordinates(d, udid, "Search", occurrence=1) is True: d.send_keys(f'{country_name[:-1]}\n')
    find_text_coordinates(d, udid, f'{country_name}', occurrence=1)

    if find_text_coordinates(d, udid, "Business phone number", occurrence=1) is True: d.send_keys(f'{mobile_number}\n')
    d(name='Done').click()
    find_text_coordinates(d, udid, "Zip or postal code", occurrence=2)
    d.send_keys(f'{business_postal_code}\n')

    find_text_coordinates(d, udid, "Business license ID", occurrence=2)
    d.send_keys(f'{business_license_id}\n')

    d.swipe(0.5, 0.9, 0.5, 0.1, 0.01)

    while find_text_coordinates(d, udid, 'Verify business', occurrence=1) is False: d.click(x, y)

    bundle_id = d.app_current().get("bundleId")
    d.open_url('shortcuts://run-shortcut?name=Delete')

    folder_path = f'{local_path}/iPhoneTikTokFiles/AccountsSettings/Business/Documents/{documents_folders[0]}'
    photo_folders = os.listdir(folder_path)  # Получаем все файлы в папке

    # Фильтруем только фотофайлы, если требуется (например, по расширению)
    photo_files = [file for file in photo_folders if file.endswith(('.jpg', '.png', '.jpeg'))]

    # Цикл для копирования всех фото
    for count, photo in enumerate(photo_files):
        # Путь к файлу на компьютере
        local_photo_path = os.path.join(folder_path, photo)
        _, file_extension = os.path.splitext(photo)
        # Путь назначения на iPhone
        destination_path = f'/Documents/Gallery/{count}.{file_extension}'

        # Выполняем команду для копирования файла на iPhone
        subprocess.check_output(f'tidevice -u {udid} fsync -B notes.3u push "{local_photo_path}" "{destination_path}"', shell=True)

    # Уведомление о завершении копирования
    cprint.info(f'[{udid}] || All photos copied to iPhone!')

    d.open_url('shortcuts://run-shortcut?name=Save')
    d.app_start(bundle_id)
    sleep(0.5)

    find_text_coordinates(d, udid, "+", occurrence=1)
    d(name='Allow Full Access').wait(5)
    d(name='Allow Full Access').click_exists()
    d(type='XCUIElementTypeImage').wait(5)
    for photo in d(type='XCUIElementTypeImage').find_elements(): photo.click()
    d(nameMatches='Confirm').click_exists()

    while find_text_coordinates(d, udid, 'SMS', occurrence=1) is False: d.click(x, y)

    find_text_coordinates(d, udid, 'Send code', occurrence=1)

    tries = 0
    while True:
        code = GetSMS(udid, api_sms_hub)
        if code is False:
            _, x_mobile, y_mobile = find_text_coordinates(d, udid, mobile_number, occurrence=1, coordinates=True)
            d.tap_hold(x_mobile, y_mobile, duration=2.0)
            d(name='Cut').click()
            find_text_coordinates(d, udid, f'<', occurrence=1)
            while find_text_coordinates(d, udid, 'SMS', occurrence=1) is False: d.click(x, y)
            find_text_coordinates(d, udid, f'{country_iso_code}', occurrence=1)
            country_iso_code, country_name, mobile_number, api_sms_hub = GetNumber(udid)
            if find_text_coordinates(d, udid, "Search", occurrence=1) is True: d.send_keys(f'{country_name[:-1]}\n')
            find_text_coordinates(d, udid, f'{country_name}', occurrence=1)
            if find_text_coordinates(d, udid, "Business phone number", occurrence=1) is True: d.send_keys(f'{mobile_number}\n')
            d(name='Done').click()
            find_text_coordinates(d, udid, 'Send code', occurrence=1)
            tries += 1
            if tries >= 10: cprint.fatal(f'[{udid}] || Ban for SMS receive from TikTok! Need to try later!'); return False
        else: break

    find_text_coordinates(d, udid, 'Enter code', occurrence=1)
    d.send_keys(f'{code}')
    d(name='Done').click()
    while find_text_coordinates(d, udid, 'Submit', occurrence=1) is False: d.click(x, y)
    while find_text_coordinates(d, udid, 'Submitted', occurrence=1) is False: find_text_coordinates(d, udid, 'Submit', occurrence=1)
    cprint.info(f'[{udid}] || Business Account is registered! Wait for approved!')
    d.app_stop('com.zhiliaoapp.musically')
    d.app_start('com.zhiliaoapp.musically')
    sleep(2)
    d(name='Profile', visible=True).click_exists()

    sleep(60)
    d.open_url('snssdk1233://webview?url=https://lf-main-gecko-source.tiktokcdn.com/obj/byte-gurd-source-sg/10/gecko/resource/tiktok_ba_pia/registration.html?_pia_=1&gecko_channel=tiktok_ba_pia&gecko_bundle=registration.html')
    while find_text_coordinates(d, udid, f"Basic information", occurrence=1) is False:
        if find_text_coordinates(d, udid, "Not approved", occurrence=1) is True: cprint.fatal(f'[{udid}] || Business Account register is not approved!'); return False
        if find_text_coordinates(d, udid, "Registration information", occurrence=1) is True:
            cprint.info(f'[{udid}] || Business Account register is success!')
            d.app_stop('com.zhiliaoapp.musically')
            d.app_start('com.zhiliaoapp.musically')
            sleep(2)
            d(name='Profile', visible=True).click_exists()
            return True

def BusinessAccountEnable(d, udid):
    cprint.warn(f'[{udid}] || STEP: Business Account create start!')
    d.open_url('snssdk1233://setting')
    d(type='XCUIElementTypeButton', nameContains='Account', visible=True).wait(5)
    d(type='XCUIElementTypeButton', nameContains='Account', visible=True).click_exists()

    for _ in range(20):
        sleep(0.5)
        if d(nameContains='Switch to Personal Account').exists:
            cprint.info(f'[{udid}] || Business account is disabled!')
            d(nameContains='Switch to Personal Account').click_exists()
            d(name='Switch anyway').click()

        if d(nameContains='Switch to Business Account').exists:
            timer = datetime.now()
            while not d(name='Choose a category', visible=True).exists:
                if BadTimer(udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno) == False: return False
                try: d(nameContains='Switch to Business Account').click_exists(); d(type='XCUIElementTypeButton', name='Next').click_exists()
                except: pass
            break

    timer = datetime.now()
    while not d(type="XCUIElementTypeButton", name="Visit Business suite").exists:
        if BadTimer(udid, timer, 60, extract_stack()[-1].name, extract_stack()[-1].lineno) == False: break
        try: d(nameContains='Automotive').click_exists(); d(type='XCUIElementTypeButton', name='Next').click_exists(); d(type='XCUIElementTypeButton', name='Skip').click_exists()
        except: pass
        sleep(0.5)

    d.app_stop('com.zhiliaoapp.musically')
    d.app_start('com.zhiliaoapp.musically')
    sleep(2)
    d(name='Profile', visible=True).click_exists()

    cprint.info(f'[{udid}] || Business Account enable successfully!')
