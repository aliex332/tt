import random
import re
import os
import sys
import email
import imaplib
from time import sleep
from cprint import cprint

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')


def GetIMAP_Message(email_data):
    email_login, email_password, email_domain, email_port = email_data.split(':')
    for _ in range(20):
        mail = imaplib.IMAP4_SSL(email_domain, int(email_port))
        mail.login(email_login, email_password)
        mail.select('INBOX')

        # Поиск письма
        _, data = mail.search(None, '(FROM "register@account.tiktok.com")')
        if data[0]:  # Если письма найдены
            _, msg_data = mail.fetch(data[0].split()[-1], "(RFC822)")
            subject = email.message_from_bytes(msg_data[0][1]).get('Subject')
            code = re.findall(r'\d+', subject)

            if code:
                # Если код найден, удалить строку из файла
                with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/IMAP.txt', 'r') as file: lines = file.readlines()
                with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/IMAP.txt', 'w') as file: file.writelines(line for line in lines if line.strip() != email_data)
                return code[0]  # Возвращаем найденный код
        # Если письма нет или код не найден, ждем
        sleep(5)
    return None

def GetIMAP_Email(udid):
    valid_account = None

    # Чтение файла
    with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/IMAP.txt', 'r') as file:
        lines = file.readlines()
        random.shuffle(lines)

    for line in lines:
        line = line.strip()
        if not line: continue
        try:
            login, password, domain, port = line.split(':')
            if not valid_account:
                try:
                    mail = imaplib.IMAP4_SSL(domain, port=int(port))
                    mail.login(login, password)
                    mail.logout()
                    valid_account = line  # Сохраняем первую валидную строку
                    break
                except imaplib.IMAP4.error: print(f"[{udid}] || ERROR: Invalid email: {line}")
                except Exception as e: print(f"[{udid}] || ERROR: Checking email: {line}")
        except ValueError: print(f"[{udid}] || ERROR: Incorrect format of the line: {line}")

    # Удаление валидной строки из файла
    if valid_account:
        with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/IMAP.txt', 'w') as file:
            for line in lines:
                if line.strip() != valid_account: file.write(line.strip() + '\n')  # Перезаписываем файл без валидной строки
        return valid_account
    else:
        with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/IMAP.txt', 'w') as file: file.write('')
        cprint.fatal(f"[{udid}] || ERROR: No valid IMAP accounts."); return False