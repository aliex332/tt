import re
import random
from time import sleep
from cprint import cprint
from requests import post, get

def GetNumber(udid):
    for _ in range(1000):
        # country_sms = random.choice(['US', 'PH', 'ID', 'MY', 'VN'])
        country_sms = random.choice(['PH'])
        if country_sms == 'PH': country_sms = ['4', 'Philippines', '+63', 'PH', 2]
        if country_sms == 'ID': country_sms = ['6', 'Indonesia', '+62', 'ID', 2]
        if country_sms == 'MY': country_sms = ['7', 'Malaysia', '+60', 'MY', 2]
        if country_sms == 'VN': country_sms = ['10', 'Vietnam', '+84', 'VN', 2]
        if country_sms == 'US': country_sms = ['12', 'United States', '+1', 'US', 1]
        if country_sms == 'UK': country_sms = ['16', 'United Kingdom', '+44', 'UK', 2]

        number = get(f"https://smshub.org/stubs/handler_api.php?api_key=182712U4ce8e18942806f85e4d15d986c823aa1&action=getNumber&service=lf&operator=any&country={country_sms[0]}").text
        if number == 'NO_NUMBERS' or number == 'WRONG_ACTIVATION_ID': print(f'[{udid}] || Country: {country_sms} - NO_NUMBERS'); continue
        else:
            phone_split = number.split(':')
            mobile_number = phone_split[-1]
            phone_id = phone_split[-2]
            cprint.info(f'[{udid}] || Phone number: {mobile_number}')
            return country_sms[3], country_sms[1], mobile_number[country_sms[4]:], phone_id


def GetSMS(udid, phone_id):
    for _ in range(15):
        code = get(f"https://smshub.org/stubs/handler_api.php?api_key=182712U4ce8e18942806f85e4d15d986c823aa1&action=getStatus&id={phone_id}").text
        if code == 'STATUS_WAIT_CODE' or code == 'WRONG_ACTIVATION_ID':
            print(f'[{udid}] || SMS CODE: {code}')
            sleep(3)
        else:
            cprint.info(f'[{udid}] || CODE RECEIVED: {code}')
            code = re.findall(r'\d+', code)
            return code[0]
    cprint.fatal(f'[{udid}] || SMS Code is not received!')
    get(f"https://smshub.org/stubs/handler_api.php?api_key=182712U4ce8e18942806f85e4d15d986c823aa1&action=setStatus&status=8&id={phone_id}")
    return False