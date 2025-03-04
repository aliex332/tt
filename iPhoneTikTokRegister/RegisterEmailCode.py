import random
from time import sleep
from requests import get
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
import iPhoneTikTokRegister.api_FirstMail as api_FirstMail
import iPhoneTikTokRegister.api_KopeechkaMail as api_KopeechkaMail

def RegisterEmailCode(d, udid, email_service):
    if email_service == 'Kopeechka': email_login, email_password, id_mail = api_KopeechkaMail.GetMail()
    if email_service == 'FirstMail': email_login, email_password = api_FirstMail.GetMail()

    print(f'[{udid}] || Email: {email_login}:{email_password}')
    d.send_keys(email_login)
    sleep(1)

    account_password = generate_password()
    timer = datetime.now()
    max_numbs = 0
    while not (d(name='Profile', visible=True).exists or d(nameMatches='Create', visible=True).exists):
        try:
            if BadTimer(udid, timer, 420, extract_stack()[-1].name, extract_stack()[-1].lineno, d=d) == False: return False

            d(name='Use another method').click_exists()
            d(name='Next', visible=True).click_exists()
            d(name='Continue', visible=True).click_exists()

            if d(name='You’ve already signed up', visible=True).exists or d(name='Enter your password to log in to your account.', visible=True).exists: return False

            if d(name='Maximum number of attempts reached. Try again later.', visible=True).exists or d(name='Something went wrong. Please try again later.', visible=True).exists or d(name='Something went wrong. Try again later.', visible=True).exists:
                cprint.fatal(f'[{udid}] || Maximum number of attemps reached! Reset settings!')
                if max_numbs == 3: return False
                max_numbs += 1

            if d(name='Verification code is expired or incorrect. Try again.', visible=True).exists:
                d.app_stop('com.zhiliaoapp.musically')
                d.app_start('com.zhiliaoapp.musically')

            if d(nameMatches='Enter', visible=True).exists or d(nameMatches='Verify', visible=True).exists or d(nameMatches='Check', visible=True).exists or d(name='Resend code').exists:
                print(f'[{udid}] || Wait email code from TikTok!')
                if d(name='Verification code is expired or incorrect. Try again.', visible=True).exists: cprint.fatal(f'[{udid}] || Code is expired!'); return False
                for _ in range(20):
                    if email_service == 'Kopeechka': mail_code = api_KopeechkaMail.GetMessage(id_mail)
                    if email_service == 'FirstMail': mail_code = api_FirstMail.GetMessage(email_login, email_password)
                    if _ == 19: cprint.fatal(f'[{udid}] || Code from TikTok not received!'); return False
                    if mail_code is False: sleep(5)
                    else:
                        cprint.info(f'[{udid}] || TikTok code is received: {mail_code}')
                        d.send_keys(mail_code)
                        d(name='Resend code', visible=True).wait_gone(10)
                        break

            if d(name='Create password', visible=True).exists or d(name='Password', visible=True).exists:
                d(name="Password").click()
                d.send_keys(account_password)
                d(name='Next', visible=True).click_exists()
                d(name='Continue', visible=True).click_exists()
        except: pass
    return account_password, email_login, email_password

def generate_password():
    chars = 'abcdefghijklnopqrstuvwxyz'
    charsUP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    symbols = '!$*-+=?'
    numbers = '1234567890'
    length = random.randint(3, 4)
    global password
    password = ''
    for i in range(length):
        password += random.choice(chars) + random.choice(symbols) + random.choice(charsUP) + random.choice(numbers)
    return password
