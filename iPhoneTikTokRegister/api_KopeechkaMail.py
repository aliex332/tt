import random
from time import sleep
from requests import post, get


def GetMail():
    for __ in range(20):
        # mail_domens = random.choice(['outlook.com', 'hotmail.com'])
        mail_domens = random.choice(['gmx.com', 'mail.com', 'email.com'])
        sleep(1)
        r = get(f"https://api.kopeechka.store/mailbox-get-email?api=2.0&site=tiktok.com&sender=tiktok&regex=&mail_type={mail_domens}&token=8a895e0e2d7459cd700ea036dc17ea41")
        if r.json()['status'] == 'OK':
            id_mail = r.json()['id']
            email = r.json()['mail']
            return email, 'no_pass', id_mail

def GetMessage(id_mail):
    r = get(f"https://api.kopeechka.store/mailbox-get-message?full=1&id={id_mail}&token=8a895e0e2d7459cd700ea036dc17ea41")
    mail_code = r.json()['value']
    if mail_code == 'WAIT_LINK': return False
    else: return mail_code