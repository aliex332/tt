import os
import sys
import platform
import flet as ft
import multiprocessing
from DeviceRun import RunDevice
from UI_INTERFACE.ResetFiles import ResetFiles
from UI_INTERFACE.CreateSwitch import create_switch
from iPhoneControl.iPhoneControl import iPhone_Status
from UI_INTERFACE.Counter import create_counter, counter_values
from UI_INTERFACE.TerminalManager import TerminalHide, TerminalShow

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def ActionModePage(udid, page: ft.Page):
    if page.client_storage.get("Localisation") == 'EN':
        text1 = "Error with USB connection!"
        text2 = 'You have a problem with USB connection. Make sure your iPhone screen is unlocked and trust permissions are granted. Disconnect and reconnect your device using a different USB cable or port.'
        text3 = "Action edit the name of your account, you can change it before or after uploading, the name can be changed once every seven days. The name can contain emoji. Before enable, configure your file with names list in settings folder."
        text4 = "Action edit your account avatar before uploading. Before enable, configure your avatar folder."
        text5 = "Action edit the link in your account, you can add it before or after uploading. Before enable, make sure you have completed the business registration for the documents and check the links file in the settings folder."
        text6 = "Action edit the bio in your account, you can add it before or after uploading. You can also link to another account via mention, the links will be used from the follow file. Before enable, configure your bio file in the settings folder."
        text7 = "Action is subscribed to the account. Before enable, configure your Follow file in the settings folder."
        text8 = "Action sends comments under your videos. Comments can contain either text or links to an account via Mention. Before enable, configure your comments file in the settings folder."
        text9 = "Action edit the description of your video when uploading, the description can contain either text or a link to an account via Mention. Before enable, configure the video description file in the settings folder."
        text10 = "Action edit the hashtags for your video when uploading, you can choose how many to use in your video. Before enable, configure the video hashtags file in the settings folder."
        text11 = "Action removes your videos from your account before uploading."
        text12 = "Action removes your link from your account before uploading."
        text13 = "Action removes your bio from your account before uploading."
        text14 = "Action enable the business profile on your account."
        text15 = "Action is going through the business profile registration to documents on your account."
        text16 = "Choose which interactions to use for your account. Some of the actions can be customized both before the videos are uploaded and after. Before start, check your usb connection with iPhone."
        text17 = "Working, please wait..."
        text18 = "Work is done."
        text19 = 'Before'
        text20 = 'After'


    if page.client_storage.get("Localisation") == 'RU':
        text1 = "Ошибка подключения USB!"
        text2 = 'Убедитесь, что экран вашего iPhone разблокирован и разрешения доверия предоставлены. Отключите и повторно подключите устройство, используя другой USB-кабель или порт.'
        text3 = "Действие изменяет имя вашего аккаунта, вы можете изменить его до или после загрузки. Имя можно менять раз в семь дней. Имя может содержать эмодзи. Перед включением настройте файл со списком имен в папке настроек."
        text4 = "Действие изменяет аватар вашего аккаунта перед загрузкой. Перед включением настройте папку с аватарами."
        text5 = "Действие изменяет ссылку в вашем аккаунте, вы можете добавить её до или после загрузки. Перед включением убедитесь, что вы завершили бизнес-регистрацию для документов, и проверьте файл со ссылками в папке настроек."
        text6 = "Действие изменяет биографию в вашем аккаунте, вы можете добавить её до или после загрузки. Вы также можете отметить другой аккаунт через ссылку. Перед включением настройте файл с биографией в папке настроек."
        text7 = "Действие подписывает на аккаунт. Перед включением настройте файл Follow в папке настроек."
        text8 = "Действие отправляет комментарии под вашими видео. Комментарии могут содержать текст или ссылки на аккаунт через отметку. Перед включением настройте файл с комментариями в папке настроек."
        text9 = "Действие изменяет описание вашего видео при загрузке. Описание может содержать текст или ссылку на аккаунт через отметку. Перед включением настройте файл с описанием видео в папке настроек."
        text10 = "Действие изменяет хэштеги для вашего видео при загрузке. Вы можете выбрать, сколько использовать в вашем видео. Перед включением настройте файл с хэштегами видео в папке настроек."
        text11 = "Действие удаляет ваши видео из вашего аккаунта перед загрузкой."
        text12 = "Действие удаляет вашу ссылку из вашего аккаунта перед загрузкой."
        text13 = "Действие удаляет вашу биографию из вашего аккаунта перед загрузкой."
        text14 = "Действие включает бизнес-профиль в вашем аккаунте."
        text15 = "Действие проходит регистрацию бизнес-профиля для документов в вашем аккаунте."
        text16 = "Выберите, какие взаимодействия использовать для вашего аккаунта. Некоторые действия можно настроить как до загрузки видео, так и после."
        text17 = "Выполняю, пожалуйста подождите..."
        text18 = "Выполнение завершено."
        text19 = 'Перед'
        text20 = 'После'

    def UpdateStorage(switch_states):
        page.client_storage.set("nickname_change", {"enabled": switch_states["nickname_change"]["enabled"], "when": switch_states["nickname_change"]["when"]})
        page.client_storage.set("link_change", {"enabled": switch_states["link_change"]["enabled"], "when": switch_states["link_change"]["when"]})
        page.client_storage.set("bio_change", {"enabled": switch_states["bio_change"]["enabled"], "when": switch_states["bio_change"]["when"]})
        page.client_storage.set("avatar_change", {"enabled": switch_states["avatar_change"]})
        page.client_storage.set("follow_account", {"enabled": switch_states["follow_account"]})
        page.client_storage.set("send_comments", {"enabled": switch_states["send_comments"]})
        page.client_storage.set("video_description", {"enabled": switch_states["video_description"]})
        page.client_storage.set("video_hashtags", {"enabled": switch_states["video_hashtags"], "hashtag_count": counter_values['counter_hashtags']})
        page.client_storage.set("delete_video", {"enabled": switch_states["delete_video"]})
        page.client_storage.set("delete_link", {"enabled": switch_states["delete_link"]})
        page.client_storage.set("delete_bio", {"enabled": switch_states["delete_bio"]})
        page.client_storage.set("business_enable", {"enabled": switch_states["business_enable"]})
        page.client_storage.set("business_register", {"enabled": switch_states["business_register"]})
        if Check_iPhoneConnection() is False: return False

        data = {
            'Register': page.client_storage.get("Register"),
            'Login': page.client_storage.get("Login"),
            'register_mode': page.client_storage.get("register_mode"),
            'account_list_laps': page.client_storage.get("account_list_laps"),
            'mobile_network': page.client_storage.get("mobile_network"),
            'reset_network': page.client_storage.get("reset_network"),
            'proxy_enable': page.client_storage.get("proxy_enable"),
            'vpn_enable': page.client_storage.get("vpn_enable"),
            'accounts_count': page.client_storage.get("accounts_count"),
            'country_code': page.client_storage.get("country_code"),

            'Upload': page.client_storage.get("Upload"),
            'Video': page.client_storage.get("Video"),
            'Photo': page.client_storage.get("Photo"),
            'Autocut': page.client_storage.get("Autocut"),
            'Overlay': page.client_storage.get("Overlay"),
            'Record': page.client_storage.get("Record"),
            'use_music_switch': page.client_storage.get("use_music_switch"),
            'use_again_switch': page.client_storage.get("use_again_switch"),
            'videos_count': page.client_storage.get("videos_count"),
            'photo_count': page.client_storage.get("photo_count"),
            'record_time': page.client_storage.get("record_time"),

            'Mention': page.client_storage.get("Mention"),
            'nickname_change': page.client_storage.get("nickname_change"),
            'link_change': page.client_storage.get("link_change"),
            'bio_change': page.client_storage.get("bio_change"),
            'avatar_change': page.client_storage.get("avatar_change"),
            'follow_account': page.client_storage.get("follow_account"),
            'send_comments': page.client_storage.get("send_comments"),
            'delete_video': page.client_storage.get("delete_video"),
            'delete_link': page.client_storage.get("delete_link"),
            'delete_bio': page.client_storage.get("delete_bio"),
            'business_enable': page.client_storage.get("business_enable"),
            'business_register': page.client_storage.get("business_register"),

            'video_description': page.client_storage.get("video_description"),
            'video_hashtags': page.client_storage.get("video_hashtags")
        }

        # Создаём диалог
        dlg_modal = ft.AlertDialog(
            modal=True,
            barrier_color=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            bgcolor='#1c1c1e',
            title=ft.Text(text17,
                          size=16,
                          weight=ft.FontWeight.BOLD,
                          text_align="center",
                          ),
            actions=[
                ft.ElevatedButton(
                    text="STOP",
                    icon=ft.Icons.STOP,  # Иконка перед текстом
                    on_click=lambda _: (process.terminate(), setattr(dlg_modal, "open", False), page.update()),
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5)  # Закруглённые углы
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=ft.Container(
                width=120,
                height=120,
                border_radius=10,
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.ProgressRing(width=80, height=80, color='#3498db'),
                            alignment=ft.alignment.center,  # Центрирование
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ),
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        TerminalShow()
        page.update()

        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=RunDevice, args=(data, queue))
        process.start()
        process.join()

        result = 0
        if not queue.empty(): result = queue.get()

        if result == 'device_offline': Check_iPhoneConnection()
        if result == 'work_done':
            TerminalHide()
            dlg_modal = ft.AlertDialog(
                modal=True,
                barrier_color=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
                bgcolor='#1c1c1e',
                title=ft.Text(text18,
                              size=16,
                              weight=ft.FontWeight.BOLD,
                              text_align="center",
                              ),
                actions=[
                    ft.ElevatedButton(
                        text="OK",
                        on_click=lambda e: [setattr(dlg_modal, 'open', False), page.update(), page.go('/MainMenuPage')],
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5)  # Закруглённые углы
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                content=ft.Container(
                    height=60,
                    border_radius=10,
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.ADD_TASK_ROUNDED,  # Указываем иконку
                                    size=60,  # Размер иконки
                                    color='yellow'
                                ),
                                alignment=ft.alignment.center,  # Центрирование
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
            )

            page.overlay.append(dlg_modal)
            dlg_modal.open = True  # Открыть диалог
            page.update()




    def BackButton():
        if page.client_storage.get("Upload") is True: page.go('/UploadModePage')
        elif page.client_storage.get("UploadSkip") is True: page.go('/UploadModePage')
        else: page.go('/MainMenuPage')

    def OpenFolder():
        if platform.system() == "Windows": os.startfile(f'{local_path}/iPhoneTikTokFiles/{last_active_switch["folder_path"]}/')
        if platform.system() == "Darwin": os.system(f"open {local_path}/iPhoneTikTokFiles/{last_active_switch["folder_path"]}/")

    def RecoverFolder():
        ResetFiles(last_active_switch["folder_path"])

    def Check_iPhoneConnection():
        if iPhone_Status(udid):
            start_button.disabled = False
            start_button.bgcolor = 'red'
            connect_button.icon_color = 'green'
            page.update()
            return True
        else:
            connect_button.icon_color = 'red'
            start_button.disabled = True
            start_button.bgcolor = 'grey'
            ErrorDialog()
            page.update()
            return False


    def ErrorDialog():
        def handle_repeat(e):
            dlg_modal.open = False  # Закрыть диалог
            Check_iPhoneConnection()
            page.update()  # Обновить страницу

        def handle_close(e):
            dlg_modal.open = False  # Закрыть диалог
            page.update()  # Обновить страницу

        dlg_modal = ft.AlertDialog(
            modal=True,
            barrier_color=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            bgcolor='#1c1c1e',
            title=ft.Row(
                [
                    ft.Icon(name=ft.Icons.WARNING, color="red", size=30),  # Иконка "warning"
                    ft.Text(text1),  # Заголовок с текстом
                ],
                spacing=10,  # Расстояние между иконкой и текстом
                alignment=ft.MainAxisAlignment.START,  # Выравнивание слева
            ),
            content=ft.Container(
                content=ft.Text(text2),
                width=400,  # Ограничение по ширине
                height=80,  # Ограничение по высоте
            ),
            actions=[
                ft.TextButton("Retry", on_click=handle_repeat),
                ft.TextButton("Cancel", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True  # Открыть диалог
        page.update()

    page.window.width = 1024
    page.window.height = 650
    page.window.resizable = False
    page.window.maximizable = False
    page.window.minimizable = True
    page.window.full_screen = False

    page.fonts = {
        "TikTok Bold": "fonts/TikTokText-Bold.ttf",
        "TikTok Medium": "fonts/TikTokText-Medium.ttf",
        "TikTok Regular": "fonts/TikTokText-Regular.ttf",
    }

    start_button = ft.ElevatedButton(
        text="START",
        on_click=lambda e: UpdateStorage(switch_states),
        color="white",
        bgcolor="red",
        disabled=False,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
    )

    connect_button = ft.IconButton(
                    icon=ft.Icons.USB,  # Иконка
                    icon_size=20,
                    tooltip="iPhone Connection",
                    on_click=lambda e: Check_iPhoneConnection(),  # Обработчик клика
                    icon_color="white",  # Цвет иконки
                    visible=True
                )

    page.appbar = ft.AppBar(
        title=ft.Text("SETUP ACTION MODE", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,
        leading=ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=lambda e: BackButton()),
        actions=[
            ft.Container(  # Оборачиваем кнопку в контейнер для отступа
                content=connect_button
            ),
            ft.Container(
                content=start_button,
                alignment=ft.alignment.center,
                padding=ft.padding.only(right=10),
            )
        ]
    )


    switch_link_change = create_switch(
        label="Link change ",
        icon=ft.Icon(ft.Icons.ADD_LINK),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("link_change"),
        visible=True
    )

    switch_video_description = create_switch(
        label="Video description ",
        icon=ft.Icon(ft.Icons.FEATURED_VIDEO_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("video_description"),
    )

    switch_video_hashtags = create_switch(
        label="Video hashtags ",
        icon=ft.Icon(ft.Icons.TAG_SHARP),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("video_hashtags"),
    )

    switch_nickname_change = create_switch(
        label="Nickname change ",
        icon=ft.Icon(ft.Icons.BADGE_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("nickname_change"),
    )

    switch_bio_change = create_switch(
        label="Bio change ",
        icon=ft.Icon(ft.Icons.AUTO_FIX_HIGH_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("bio_change"),
    )

    switch_delete_bio = create_switch(
        label="Delete bio ",
        icon=ft.Icon(ft.Icons.AUTO_FIX_OFF_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("delete_bio"),
    )

    switch_delete_link = create_switch(
        label="Delete link ",
        icon=ft.Icon(ft.Icons.LINK_OFF_ROUNDED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("delete_link"),
    )

    switch_delete_video = create_switch(
        label="Delete video ",
        icon=ft.Icon(ft.Icons.VIDEOCAM_OFF_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("delete_video"),
    )

    switch_send_comments = create_switch(
        label="Send comments ",
        icon=ft.Icon(ft.Icons.INSERT_COMMENT_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("send_comments"),
    )

    switch_follow_account = create_switch(
        label="Follow account ",
        icon=ft.Icon(ft.Icons.GROUP_ADD_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("follow_account"),
    )

    switch_change_avatar = create_switch(
        label="Avatar change ",
        icon=ft.Icon(ft.Icons.CAMERASWITCH_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("avatar_change"),
    )

    switch_business_enable = create_switch(
        label="Business enable ",
        icon=ft.Icon(ft.Icons.ADD_BUSINESS_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("business_enable"),
    )

    switch_business_register = create_switch(
        label="Business register ",
        icon=ft.Icon(ft.Icons.BUSINESS_CENTER_OUTLINED),
        icon_color=ft.Colors.BLUE,
        on_change=lambda e: update_content("business_register"),
    )


    # Функция для обновления текста и картинки
    image = ft.Image(src=f"{local_path}/resource/assets/photo/Profile.png", left=130, top=-130)
    last_active_switch = {"name": None, "folder_path": None}

    switch_states = {
        "nickname_change": {"enabled": False, "when": "Before"},
        "avatar_change": False,
        "link_change": {"enabled": False, "when": "Before"},
        "bio_change": {"enabled": False, "when": "Before"},
        "follow_account": False,
        "send_comments": False,
        "video_description": False,
        "video_hashtags": False,
        "delete_video": False,
        "delete_link": False,
        "delete_bio": False,
        "business_enable": False,
        "business_register": False
    }
    hashtags_counter, set_hashtags_counter_visibility = create_counter("counter_hashtags", 3, "Hashtag count:", "white", "black", "black", visible=False)
    def update_content(changed_switch=None):
        if changed_switch == "nickname_change" and switch_nickname_change.controls[1].value:
            text_content.value = text3
            image.src = f"{local_path}/resource/assets/photo/nickname_change.png"
            last_active_switch["name"] = "nickname_change"
            last_active_switch["folder_path"] = "/AccountsSettings/NickName"
            switch_states["nickname_change"]["enabled"] = True
            folder_button.visible = True
            recover_button.visible = True
            buttons_container.visible = True
            buttons_container.content.controls[0].selected_index = 0
            set_hashtags_counter_visibility(False)

        elif changed_switch == "avatar_change" and switch_change_avatar.controls[1].value:
            text_content.value = text4
            image.src = f"{local_path}/resource/assets/photo/change_avatar.png"
            last_active_switch["name"] = "avatar_change"
            last_active_switch["folder_path"] = "/AccountsSettings/Avatars"
            switch_states["avatar_change"] = True
            folder_button.visible = True
            recover_button.visible = False
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "link_change" and switch_link_change.controls[1].value:
            text_content.value = text5
            image.src = f"{local_path}/resource/assets/photo/change_link.png"
            last_active_switch["name"] = "link_change"
            last_active_switch["folder_path"] = "/AccountsSettings/Website/"
            switch_states["link_change"]["enabled"] = True
            folder_button.visible = True
            recover_button.visible = True
            buttons_container.visible = True
            buttons_container.content.controls[0].selected_index = 0
            set_hashtags_counter_visibility(False)

        elif changed_switch == "bio_change" and switch_bio_change.controls[1].value:
            text_content.value = text6
            image.src = f"{local_path}/resource/assets/photo/change_bio.png"
            last_active_switch["name"] = "bio_change"
            last_active_switch["folder_path"] = "/AccountsSettings/Bio/"
            switch_states["bio_change"]["enabled"] = True
            folder_button.visible = True
            recover_button.visible = True
            buttons_container.visible = True
            buttons_container.content.controls[0].selected_index = 0
            set_hashtags_counter_visibility(False)

        elif changed_switch == "follow_account" and switch_follow_account.controls[1].value:
            text_content.value = text7
            image.src = f"{local_path}/resource/assets/photo/follow.png"
            last_active_switch["name"] = "follow_account"
            last_active_switch["folder_path"] = "/AccountsSettings/Follow/"
            switch_states["follow_account"] = True
            folder_button.visible = True
            recover_button.visible = True
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "send_comments" and switch_send_comments.controls[1].value:
            text_content.value = text8
            image.src = f"{local_path}/resource/assets/photo/send_comments.png"
            last_active_switch["name"] = "send_comments"
            last_active_switch["folder_path"] = "/AccountsSettings/Comments/"
            switch_states["send_comments"] = True
            folder_button.visible = True
            recover_button.visible = True
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "video_description" and switch_video_description.controls[1].value:
            text_content.value = text9
            image.src = f"{local_path}/resource/assets/photo/edit_description.png"
            last_active_switch["name"] = "video_description"
            last_active_switch["folder_path"] = "/AccountsSettings/Description/"
            switch_states["video_description"] = True
            folder_button.visible = True
            recover_button.visible = True
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "video_hashtags" and switch_video_hashtags.controls[1].value:
            text_content.value = text10
            image.src = f"{local_path}/resource/assets/photo/edit_hashtags.png"
            last_active_switch["name"] = "video_hashtags"
            last_active_switch["folder_path"] = "/AccountsSettings/HashTags/"
            switch_states["video_hashtags"] = True
            folder_button.visible = True
            recover_button.visible = True
            buttons_container.visible = False
            set_hashtags_counter_visibility(True)

        elif changed_switch == "delete_video" and switch_delete_video.controls[1].value:
            text_content.value = text11
            image.src = f"{local_path}/resource/assets/photo/delete_video.png"
            last_active_switch["name"] = "delete_video"
            last_active_switch["folder_path"] = None
            folder_button.visible = False
            recover_button.visible = False
            switch_states["delete_video"] = True
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "delete_link" and switch_delete_link.controls[1].value:
            text_content.value = text12
            image.src = f"{local_path}/resource/assets/photo/change_link.png"
            last_active_switch["name"] = "delete_link"
            last_active_switch["folder_path"] = None
            folder_button.visible = False
            recover_button.visible = False
            switch_states["delete_link"] = True
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "delete_bio" and switch_delete_bio.controls[1].value:
            text_content.value = text13
            image.src = f"{local_path}/resource/assets/photo/change_bio.png"
            last_active_switch["name"] = "delete_bio"
            last_active_switch["folder_path"] = None
            switch_states["delete_bio"] = True
            folder_button.visible = False
            recover_button.visible = False
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "business_enable" and switch_business_enable.controls[1].value:
            text_content.value = text14
            image.src = f"{local_path}/resource/assets/photo/business_enable.png"
            last_active_switch["name"] = "business_enable"
            last_active_switch["folder_path"] = None
            folder_button.visible = False
            recover_button.visible = False
            switch_states["business_enable"] = True
            buttons_container.visible = False
            set_hashtags_counter_visibility(False)

        elif changed_switch == "business_register" and switch_business_register.controls[1].value:
            text_content.value = text15
            image.src = f"{local_path}/resource/assets/photo/business_register.png"
            last_active_switch["name"] = "business_register"
            last_active_switch["folder_path"] = "/AccountsSettings/Business/"
            switch_states["business_register"] = True
            buttons_container.visible = False
            folder_button.visible = True
            recover_button.visible = False
            set_hashtags_counter_visibility(False)


        elif not any([
            switch_nickname_change.controls[1].value,
            switch_change_avatar.controls[1].value,
            switch_link_change.controls[1].value,
            switch_bio_change.controls[1].value,
            switch_follow_account.controls[1].value,
            switch_send_comments.controls[1].value,
            switch_video_description.controls[1].value,
            switch_video_hashtags.controls[1].value,
            switch_delete_video.controls[1].value,
            switch_delete_link.controls[1].value,
            switch_delete_bio.controls[1].value,
            switch_business_enable.controls[1].value,
            switch_business_register.controls[1].value
        ]):
            text_content.value = text16
            image.src = f"{local_path}/resource/assets/photo/Profile.png"
            last_active_switch["name"] = None
            last_active_switch["folder_path"] = None
            folder_button.visible = False
            recover_button.visible = False
            buttons_container.visible = False

        if switch_nickname_change.controls[1].value is False: switch_states["nickname_change"]["enabled"] = False; switch_states["nickname_change"]["when"] = 'Before'
        if switch_link_change.controls[1].value is False: switch_states["link_change"]["enabled"] = False; switch_states["link_change"]["when"] = 'Before'
        if switch_bio_change.controls[1].value is False: switch_states["bio_change"]["enabled"] = False; switch_states["bio_change"]["when"] = 'Before'

        if switch_change_avatar.controls[1].value is False: switch_states["avatar_change"] = False
        if switch_follow_account.controls[1].value is False: switch_states["follow_account"] = False
        if switch_send_comments.controls[1].value is False: switch_states["send_comments"] = False
        if switch_video_description.controls[1].value is False: switch_states["video_description"] = False
        if switch_video_hashtags.controls[1].value is False: switch_states["video_hashtags"] = False; set_hashtags_counter_visibility(False)
        if switch_delete_video.controls[1].value is False: switch_states["delete_video"] = False
        if switch_delete_link.controls[1].value is False: switch_states["delete_link"] = False
        if switch_delete_bio.controls[1].value is False: switch_states["delete_bio"] = False
        if switch_business_enable.controls[1].value is False: switch_states["business_enable"] = False
        if switch_business_register.controls[1].value is False: switch_states["business_register"] = False
        page.update()

    text_content = ft.Text(
        value=text16,
        size=15,
        font_family="TikTok Regular",
        width=300,
    )

    folder_button = ft.IconButton(
        icon=ft.Icons.FOLDER_COPY_OUTLINED,  # Иконка
        icon_size=30,
        tooltip="Configure settings",
        on_click=lambda e: OpenFolder(),  # Обработчик клика
        icon_color="white",  # Цвет иконки
        visible=False
    )

    recover_button = ft.IconButton(
        icon=ft.Icons.AUTO_DELETE_OUTLINED,  # Иконка
        icon_size=30,
        tooltip="Reset settings",
        on_click=lambda e: RecoverFolder(),  # Обработчик клика
        icon_color="white",  # Цвет иконки
        visible=False
    )

    # Контейнер для текста и кнопки
    right_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=text_content,
                    padding=ft.padding.only(bottom=0),
                ),
                ft.Row(  # Добавил row для folder_button
                    controls=[
                        folder_button,
                        recover_button
                    ],
                ),
                hashtags_counter,
            ],
            spacing=20,
        ),
        left=650,
        top=130,
    )

    def on_button_change(e, last_active_switch):
        if e.data == '0': switch_states[last_active_switch["name"]]["when"] = 'Before'
        if e.data == '1': switch_states[last_active_switch["name"]]["when"] = 'After'

    buttons_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.CupertinoSegmentedButton(
                    selected_index=0,
                    border_color='black',
                    click_color='white',
                    unselected_color='#ecf0f1',
                    selected_color='blue',
                    on_change=lambda e: on_button_change(e, last_active_switch),
                    controls=[
                        ft.Text(text19),
                        ft.Container(
                            padding=ft.padding.symmetric(0, 30),
                            content=ft.Text(text20),
                        ),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.START,  # Выравнивание кнопок по левому краю
        ),
        left=633,  # Позиционирование контейнера
        top=80,
        visible=False
    )


    if page.client_storage.get("Upload") is False or page.client_storage.get("Upload") is None: visible_video_setting = False; visible_business_setting = True
    if page.client_storage.get("Upload") is True: visible_video_setting = True; visible_business_setting = False
    scrollable_switches_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[switch_nickname_change],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_change_avatar],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_link_change],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_bio_change],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_follow_account],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_send_comments],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_video_description],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0),
                    visible=visible_video_setting
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_video_hashtags],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0),
                    visible=visible_video_setting
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_delete_video],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_delete_link],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                ft.Container(
                    content=ft.Row(
                        controls=[switch_delete_bio],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=ft.Padding(right=20, top=0, left=0, bottom=0)
                ),

                # ft.Container(
                #     content=ft.Row(
                #         controls=[switch_business_enable],
                #         spacing=10,
                #         alignment=ft.MainAxisAlignment.END,
                #     ),
                #     padding=ft.Padding(right=20, top=0, left=0, bottom=0),
                #     visible=visible_business_setting
                # ),

                # ft.Container(
                #     content=ft.Row(
                #         controls=[switch_business_register],
                #         spacing=10,
                #         alignment=ft.MainAxisAlignment.END,
                #     ),
                #     padding=ft.Padding(right=20, top=0, left=0, bottom=0),
                #     visible=visible_business_setting
                # ),

            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            scroll=ft.ScrollMode.ALWAYS,  # Включает прокрутку для содержимого
        ),
        width=300,  # Ширина контейнера
        height=230,  # Высота контейнера
    )

    stack = ft.Stack(
        controls=[
            image,
            right_container,
            buttons_container,
            ft.Container(
                content=scrollable_switches_container,  # Используем ListView вместо Column
                left=10,
                top=75,
            ),
        ]
    )
    page.add(stack)
