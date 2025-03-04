import os
import sys
import platform

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def ResetFiles(path):
    if path == "/AccountsSettings/NickName":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/NameAccounts.txt', 'w') as file:
            file.write("Paste name for your account one.\n")
            file.write("Paste name for your account two.\n")

    if path == "/AccountsSettings/Website/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/Website.txt', 'w') as file:
            file.write("Paste link on your website one.\n")
            file.write("Paste link on your website two.\n")
            file.write("Example: https://google.com\n")

    if path == "AccountsSettings/Bio/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/BioMention.txt', 'w') as file:
            file.write("Paste link on your account one.\n")
            file.write("Paste link on your account two.\n")
            file.write("Example: https://www.tiktok.com/@riwww?is_from_webapp=1&sender_device=pc\n")

        with open(f'{local_path}/iPhoneTikTokFiles/{path}/BioText.txt', 'w') as file:
            file.write("Paste your text one.\n")
            file.write("Paste your text two.\n")

    if path == "/AccountsSettings/Follow/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/Profiles.txt', 'w') as file:
            file.write("Paste link on your account one.\n")
            file.write("Paste link on your account two.\n")
            file.write("Example: https://www.tiktok.com/@riwww?is_from_webapp=1&sender_device=pc\n")

    if path == "/AccountsSettings/Comments/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/CommentsMention.txt', 'w') as file:
            file.write("Paste link on your account one.\n")
            file.write("Paste link on your account two.\n")
            file.write("Example: https://www.tiktok.com/@riwww?is_from_webapp=1&sender_device=pc\n")

        with open(f'{local_path}/iPhoneTikTokFiles/{path}/CommentsText.txt', 'w') as file:
            file.write("Paste your text one.\n")
            file.write("Paste your text two.\n")

    if path == "/AccountsSettings/Description/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/DescriptionMention.txt', 'w') as file:
            file.write("Paste link on your account one.\n")
            file.write("Paste link on your account two.\n")
            file.write("Example: https://www.tiktok.com/@riwww?is_from_webapp=1&sender_device=pc\n")

        with open(f'{local_path}/iPhoneTikTokFiles/{path}/DescriptionVideo.txt', 'w') as file:
            file.write("Paste your text one.\n")
            file.write("Paste your text two.\n")

    if path == "/AccountsSettings/HashTags/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/HashtagsVideo.txt', 'w') as file:
            file.write("#Paste your hashtag one.\n")
            file.write("#Paste your hashtag two.\n")

    if path == "/AccountsSettings/HashTags/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/HashtagsVideo.txt', 'w') as file:
            file.write("#Paste your hashtag one.\n")
            file.write("#Paste your hashtag two.\n")

    if path == "/AccountsSettings/Music/":
        with open(f'{local_path}/iPhoneTikTokFiles/{path}/MusicGB.txt', 'w') as file:
            file.write("Paste your music link one.\n")
            file.write("Paste your music link two.\n")
            file.write("Example: https://www.tiktok.com/music/Guess-featuring-billie-eilish-7398255077729110032?is_from_webapp=1&sender_device=pc\n")

        with open(f'{local_path}/iPhoneTikTokFiles/{path}/MusicAU.txt', 'w') as file:
            file.write("Paste your music link one.\n")
            file.write("Paste your music link two.\n")
            file.write("Example: https://www.tiktok.com/music/Guess-featuring-billie-eilish-7398255077729110032?is_from_webapp=1&sender_device=pc\n")

        with open(f'{local_path}/iPhoneTikTokFiles/{path}/MusicUS.txt', 'w') as file:
            file.write("Paste your music link one.\n")
            file.write("Paste your music link two.\n")
            file.write("Example: https://www.tiktok.com/music/Guess-featuring-billie-eilish-7398255077729110032?is_from_webapp=1&sender_device=pc\n")

    if path == "Proxy":
        with open(f'{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/Proxy/Proxy.txt', 'w') as file:
            file.write("Example: COUNTRY_CODE_ISO2:IP:PORT:LOGIN:PASSWORD\n")
            file.write("Example: GB:IP:PORT:LOGIN:PASSWORD\n")

    if path == "VPN":
        with open(f'{local_path}/iPhoneTikTokFiles/iPhoneNetSettings/VPN/VPNServices.txt', 'w') as file:
            file.write("STRONG:richardjdcarey@gmail.com:Akina222\n")
            file.write("WHOER:NONE:NONE\n")
            file.write("Example:COUNTRY_VPN-NAME-CONFIG:LOGIN:PASSWORD\n")