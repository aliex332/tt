import re
import os
import random
from time import sleep
from cprint import cprint
from requests import post, get

import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
def GetAccountBase():
    with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt') as f:  ## Открываем файл
        lines = [line.strip() for line in f]
        random.shuffle(lines)
        return lines

def GetAccountFromBase(udid, account):
    account_split = account.split(':')
    country_code = account_split[1]
    NickName = account_split[2]
    Password = account_split[3]
    Email = account_split[4]
    Password_Email = account_split[5]
    VPN_Name = account_split[6]

    if account_split[0] != udid: return False
    return NickName, Password, VPN_Name, country_code, Email, Password_Email

def GetAccountPurchased():
    with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsPurchased.txt') as f:  ## Открываем файл
        lines = [line.strip() for line in f]
        random.shuffle(lines)

    for account in lines:
        account_split = account.split('|')
        print(account_split[0], account_split[1], account_split[2], account_split[3])
        udid = '00008030-000D05341E3B802E'
        country_code = account_split[4]
        vpn_configs = os.listdir(f'{local_path}/iPhoneVPNSettings/VPN/{country_code}')
        random.shuffle(vpn_configs)
        vpn_named = re.findall(r"([\s\S]*)\.ovpn*", vpn_configs[0])
        account_email = account_split[0]
        account_email_pass = account_split[1]
        account_nick = account_split[2]
        account_pass = account_split[3]

        with open(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/AccountsLogin.txt', 'a') as account_new:
            account_new.write(f'{udid}:{country_code}:{account_nick}:{account_pass}:{account_email}:{account_email_pass}:{vpn_named[0]}' + '\n')

# GetAccountPurchased()