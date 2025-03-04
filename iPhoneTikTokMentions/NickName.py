import os
import random
from time import sleep
from cprint import cprint
import sys
if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')


def ChangeNickName(d, udid):
    if d(name='Change photo', visible=True).exists is False: d.open_url('snssdk1233://user/profile/edit')
    d(value='Name').click()
    if d(nameContains='You can change it again', visible=True).exists: cprint.fatal(f'[{udid}] || Nickname can only be changed every 7 days!'); Exception(); return True
    with open(f'{local_path}/iPhoneTikTokFiles/AccountsSettings/NickName/NameAccounts.txt', 'r', encoding='utf-8') as f:
        name_text = f.readlines()
        name_text = [line.strip() for line in name_text]
        random.shuffle(name_text)

    smiles = random.choice(['🔞', '⛔️', '🟥', '🛑', '❤️', '🍓', '🍒', '🍑', '🍌', '🍉', '🍆', '⭕️', '🛑', '📛', '🔴'])
    name_text = f'{smiles} {name_text[0]} {smiles}'
    if d(type="XCUIElementTypeTextView").exists: d(type="XCUIElementTypeTextView").get().clear_text(); d(type="XCUIElementTypeTextView").get().set_text(name_text)
    if d(type="XCUIElementTypeTextField").exists: d(type="XCUIElementTypeTextField").clear_text(); d(type="XCUIElementTypeTextField").get().set_text(name_text)
    d(value='Save').click()
    d(name='Confirm').click()
    cprint.info(f'[{udid}] || Account nick changed: {name_text}')
    d(name='Change photo', visible=True).wait(5)