import os
import sys
from time import sleep
from cprint import cprint
from datetime import datetime
from traceback import extract_stack
from iPhoneTikTokCheckers.BadTimer import BadTimer
from iPhoneTikTokRegister.api_IMAP import GetIMAP_Message

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')


def Login(d, udid, account_data, email_data):
    d.send_keys(account_data.strip().split(':')[0])
    if d(type='XCUIElementTypeSecureTextField', visible=True).exists: pass
    else: d.visible_button_click_exist('red')

    d(type='XCUIElementTypeSecureTextField', visible=True).get().set_text(account_data.strip().split(':')[1])

    timer = datetime.now()
    while not (d(name='Profile', visible=True).exists or d(name='Skip', visible=True).exists):
        try:
            if BadTimer(udid, timer, 250, extract_stack()[-1].name, extract_stack()[-1].lineno, d) == False: return False
            d.visible_button_click_exist('red')
            if d(nameContains='banned').exists or d(nameContains='Download').exists or d(nameMatches='Incorrect', visible=True).exists:
                cprint.fatal(f'[{udid}] || ERROR: Account permanently banned or deleted! Take new account...')

                with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt', 'r') as file: lines = file.readlines()
                updated_lines = [line for line in lines if account_data not in line]
                with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt', 'w') as file: file.writelines(updated_lines)
                with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/BannedAccounts.txt', 'a') as banned_file: banned_file.write(f'{account_data}\n')
                return False

            if d(name='Maximum number of attempts reached. Try again later.', visible=True).exists or d(nameMatches='Something went wrong', visible=True).exists: cprint.fatal(f'[{udid}] || ERROR: Maximum number of attempts reached! Resetting settings...'); return False

            if d(nameContains='Verify identity').exists:
                cprint.fatal(f'[{udid}] || Verify your account by Email!')
                if email_data is None: cprint.fatal(f'[{udid}] || ERROR: You do not have access to your email for recovering this account! Skipping this account...'); return False
                d.xpath('//*[contains(@value, "@")]').get().click()
                sleep(1)
                try: d(name='Next', visible=True).click()
                except: pass
                d(nameMatches='Enter').wait(15)
                code = GetIMAP_Message(email_data)
                if code is None: return False
                cprint.info(f'[{udid}] || TikTok verify code: {code}!')
                d.send_keys(code)
                d(name='Resend code').wait_gone(10, False)
        except: pass