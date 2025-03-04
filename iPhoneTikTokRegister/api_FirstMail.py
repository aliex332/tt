import re
import json
import requests
from time import sleep


def GetMail():
    url = "https://api.firstmail.ltd/v1/market/buy/mail?type=3"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "46ca3233-25f3-463a-8fc9-fbfcc8e662d7"
    }

    response = requests.get(url, headers=headers)
    # Разделяем значение поля "login" по символу ":"
    login_info = response.json()['login'].split(':')

    # Сохраняем логин и пароль в переменные
    login = login_info[0]
    password = login_info[1]
    return login, password


def GetMessage(login, password):
    url = f"https://api.firstmail.ltd/v1/market/get/message?username={login}&password={password}"

    headers = {
        "accept": "application/json",
        "X-API-KEY": "46ca3233-25f3-463a-8fc9-fbfcc8e662d7"
    }

    response = requests.get(url, headers=headers)
    sleep(1)
    if response.json()["has_message"] == 'false': return False
    subject = response.json()['subject']
    code = re.search(r'\d+', subject).group()
    return code