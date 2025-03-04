import random
from iPhoneTikTok import iPhoneTikTok
from iPhoneTikTokCheckers.AccountsDataBase import GetAccountBase, GetAccountFromBase

def RunDevice(data, queue):
    udid = '00008030-000D05341E3B802E'

    if data.get('Register'): count = range(data.get('accounts_count'))
    if data.get('Login') is False and data.get('Register') is False:
        if data.get('Upload') or data.get('Mention'): count = range(1)

    if data.get('Login'): lap_list = data.get("account_list_laps")
    else: lap_list = 1

    for _ in range(lap_list):
        if data.get('Login'): count = GetAccountBase()
        for account in count:
            try:
                country_code = random.choice(['GB'])
                iPhone = iPhoneTikTok(udid=udid, account_data=account, country_code=country_code, settings=data)
                with iPhone as iPhone:
                    if data.get('Login') or data.get('Register'):
                        if iPhone.RegisterLoginAccount() is False: continue

                    if data.get('Upload'):
                        if iPhone.UploadVideo() is False: continue

                    if data.get('Mention'):
                        iPhone.Mention()

            except RuntimeError as e:
                # Обработка исключения "устройство оффлайн"
                queue.put('device_offline')
                return 'device_offline'
            except: pass

    queue.put('work_done')
    return 'work_done'