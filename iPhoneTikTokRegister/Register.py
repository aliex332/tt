import random
from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneTikTokRegister.api_IMAP import GetIMAP_Message, GetIMAP_Email
from iPhoneTikTokRegister.api_KopeechkaMail import GetKopeechka_Mail, GetKopeechka_Message
from icecream import ic


def generate_password():
    # Доступные символы
    chars = 'abcdefghijklmnopqrstuvwxyz'  # Маленькие буквы
    charsUP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Большие буквы
    symbols = '!@?'  # Спецсимволы
    numbers = '1234567890'  # Цифры

    # Длина пароля (от 8 до 9 символов)
    length = random.randint(8, 10)

    # Обязательные компоненты пароля
    password = ''
    password += random.choice(symbols)  # Один спецсимвол
    password += random.choice(chars) + random.choice(charsUP)  # Одна маленькая и одна большая буква
    password += random.choice(numbers)  # Одна цифра

    # Заполняем оставшуюся длину пароля случайными символами
    while len(password) < length:
        password += random.choice(chars + charsUP + numbers)

    # Перемешиваем символы, чтобы спецсимвол не всегда был в начале
    password = ''.join(random.sample(password, len(password)))

    return password


def Register(d, udid, settings):
    account_password = generate_password()
    if settings.get('register_mode') == 'Kopeechka': email_data = GetKopeechka_Mail()
    if settings.get('register_mode') == 'IMAP': email_data = GetIMAP_Email(udid)

    if email_data is False: cprint.fatal(f'[{udid}] || ERROR: Get email failed. Please check your IMAP and Kopeechka settings!'); return False, False

    print(f'[{udid}] || Email: {email_data.split(':')[0]}')
    d.send_keys(email_data.split(':')[0])
    d.visible_button_click_exist('red')
    sleep(1)
    if d(type='XCUIElementTypeSecureTextField', visible=True).exists: d(type='XCUIElementTypeButton', name='Clear text').click_exists(); d(type='XCUIElementTypeSecureTextField').get().set_text(account_password); d.visible_button_click_exist('red')

    timer = datetime.now()
    while not (d(name='Profile', visible=True).exists or d(name='Skip', visible=True).exists):
        try:
            if BadTimer(udid, timer, 420, extract_stack()[-1].name, extract_stack()[-1].lineno) == False: return False, False
            d.visible_button_click_exist('red')

            if d(name='You’ve already signed up', visible=True).exists or d(name='Enter your password to log in to your account.', visible=True).exists: cprint.fatal(f'[{udid}] || ERROR: Account is already registered. Please use login mode to log in...'); return False, False
            if d(name='Maximum number of attempts reached. Try again later.', visible=True).exists or d(nameMatches='Something went wrong', visible=True).exists: cprint.fatal(f'[{udid}] || ERROR: Maximum number of attempts reached! Resetting settings...'); return False, False

            if d(name='Resend code').exists:
                print(f'[{udid}] || Waiting for TikTok code, please wait...')
                if settings.get('register_mode') == 'Kopeechka': mail_code = GetKopeechka_Message(email_data)
                if settings.get('register_mode') == 'IMAP': mail_code = GetIMAP_Message(email_data)
                if mail_code is False: cprint.fatal(f'[{udid}] || ERROR: TikTok code not received!'); return False, False
                cprint.info(f'[{udid}] || TikTok code is received: {mail_code}')
                d.send_keys(mail_code)
                d(name='Resend code', visible=True).wait_gone(10, False)
                sleep(1)
                if d(name='Verification code is expired or incorrect. Try again.', visible=True).exists: cprint.fatal(f'[{udid}] || ERROR: Verification code is expired!'); return False, False
            if d(type='XCUIElementTypeSecureTextField', visible=True).exists: d(type='XCUIElementTypeButton', name='Clear text').click_exists(); d(type='XCUIElementTypeSecureTextField').get().set_text(account_password); d.visible_button_click_exist('red'); d(type='XCUIElementTypeSecureTextField', visible=True).wait_gone(10, False)

        except:
            pass

    if d(type='XCUIElementTypeSecureTextField', visible=True).wait(5): d(type='XCUIElementTypeButton', name='Clear text').click_exists(); d(type='XCUIElementTypeSecureTextField').get().set_text(account_password); d.visible_button_click_exist('red'); d(type='XCUIElementTypeSecureTextField', visible=True).wait_gone(10, False)

    if settings.get('register_mode') == 'Kopeechka': email_data = ''
    if settings.get('register_mode') == 'IMAP': email_data = f'IMAP:{email_data}'
    return account_password, email_data
