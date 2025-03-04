import os
import sys
import flet as ft
from UI_INTERFACE.TerminalManager import TerminalHide, TerminalShow
from iPhoneControl.iPhoneControl import iPhoneReset, iPhone_ConnectPC, iPhone_Status, Create_WiFiconfig

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def SetupDevicePage(udid, page: ft.Page):
    if page.client_storage.get("Localisation") == 'EN':
        text1 = 'You need to enter the name and password for your WiFi. Click WiFi right button to setup. Make sure to check the case sensitivity carefully. If you provide incorrect information, your iPhone will not be able to activate.'
        text2 = 'Action setup the automation software on your iPhone. Ensure your iPhone screen is unlocked and trust permissions are granted. Do not touch the phone or disconnect the USB cable!'
        text3 = 'Your device is successfully configured. Now, you need to sign in to your Apple ID. You can find more guides and tutorials about the setup on the main page in the information!'
        text4 = 'Action will reset your iPhone to factory settings and then configured your device. Make sure you are logged out of iCloud or Apple ID. Save all your data from this iPhone! It will be deleted and you will not be able to recover it.'
        text5 = 'Connect your iPhone to the computer using a USB or USB Type-C cable. Wait for the trust dialog to appear on your iPhone. Tap \'Trust\' on your iPhone, unlock the screen, and then press the \'Next\' button to test the connection.'
        text6 = 'Error with USB connection!'
        text7 = 'You have a problem with USB connection. Make sure your iPhone screen is unlocked and trust permissions are granted. Disconnect and reconnect your device using a different USB cable or port.'
        text8 = 'Resetting, please wait...'
        text9 = 'Do not touch the phone or disconnect the USB cable! It takes 10 minutes.'
        text10 = 'Connecting, please wait...'
        text11 = 'Do not touch the phone or disconnect the USB cable! It takes 1 minute.'
        text12 = 'Error with iPhone Reset!'
        text13 = 'Make sure you are logged out of iCloud or Apple ID and trust permissions are granted. Disconnect and reconnect your device using a different USB cable or port.'
        text14 = 'Error with iPhone Automation!'
        text15 = 'You have the problems with automation software on your iPhone! Ensure your screen is unlocked and trust permissions are granted. Disconnect and reconnect your device using a different usb cable or port.'
        text16 = 'Invalid SSID or password. Try again.'
        text17 = 'Please enter your SSID and password.'
        text18 = 'NEXT'
        text19 = 'FINISH'
        text20 = 'Connect to WI-FI:'

    if page.client_storage.get("Localisation") == 'RU':
        text1 = 'Вам необходимо ввести имя и пароль для вашей WiFi сети. Нажмите правую кнопку WiFi, чтобы настроить. Убедитесь, что вы внимательно проверили регистр букв. Если вы введете неверную информацию, ваш iPhone \nне сможет активироваться.'
        text2 = 'Действие настраивает программное обеспечение автоматизации на вашем iPhone. Убедитесь, что экран iPhone разблокирован и разрешения доверия предоставлены. Не прикасайтесь к телефону и не отключайте USB-кабель!'
        text3 = 'Ваше устройство успешно настроено. Теперь вам нужно войти в свой Apple ID. Вы сможете найти больше инструкций по настройке на главной странице в информации!'
        text4 = 'Действие сбросит ваш iPhone до заводских настроек и затем настроит устройство. Убедитесь, что вы вышли из iCloud или Apple ID. Сохраните все данные с этого iPhone! Они будут удалены, и вы не сможете их восстановить.'
        text5 = 'Подключите ваш iPhone к компьютеру с помощью кабеля USB или USB Type-C. Подождите, пока на iPhone не появится диалоговое окно доверия. Нажмите \n"Доверять" на вашем iPhone.'
        text6 = 'Ошибка подключения USB!'
        text7 = 'Убедитесь, что экран вашего iPhone разблокирован и разрешения доверия предоставлены. Отключите и повторно подключите устройство, используя другой USB-кабель или порт.'
        text8 = 'Сброс, пожалуйста подождите...'
        text9 = 'Не прикасайтесь к телефону, не отключайте USB-кабель! Это займет 10 минут.'
        text10 = 'Подключение, пожалуйста подождите...'
        text11 = 'Не прикасайтесь к телефону и не отключайте USB-кабель! Это займет 1 минуту.'
        text12 = 'Ошибка сброса iPhone!'
        text13 = 'Убедитесь, что вы вышли из iCloud или Apple ID и предоставили разрешения доверия. Отключите и повторно подключите устройство, используя другой USB-кабель или порт.'
        text14 = 'Ошибка автоматизации iPhone!'
        text15 = 'У вас возникли проблемы с программным обеспечением автоматизации на вашем iPhone! Убедитесь, что экран разблокирован и разрешения доверия предоставлены. Отключите и повторно подключите устройство, используя другой USB-кабель или порт.'
        text16 = 'Недействительный SSID или пароль.'
        text17 = 'Пожалуйста, введите SSID и пароль.'
        text18 = 'ДАЛЕЕ'
        text19 = 'ГОТОВО'
        text20 = 'Подключить WI-FI:'

    def create_icon_container(icon, icon_size, icon_color, bgcolor, on_click=None):
        container = ft.Container(
            width=100,
            height=100,
            bgcolor=bgcolor,
            border_radius=10,
            content=ft.Stack(
                controls=[ft.Icon(name=icon, size=icon_size, color=icon_color)],
                alignment=ft.alignment.center,
            ),
            alignment=ft.alignment.center,
            on_click=on_click,  # Передаем функцию для обработки клика
        )
        return container

    def BackButton():
        page.go('/MainMenuPage')

    def Check_iPhoneConnection():
        if iPhone_Status(udid):
            usb_appbar_button.icon_color = 'green'
            page.update()
            return True
        else:
            usb_appbar_button.icon_color = 'red'
            ErrorDialog()
            page.update()
            return False


    def ErrorDialog():
        def handle_repeat(e):
            dlg_modal.open = False  # Закрыть диалог
            if Check_iPhoneConnection() is False: return False
            segmented_button.selected_index = 1
            text_content.value = text1
            usb_container.visible = False
            wifi_container.visible = True
            usb_appbar_button.icon_color = 'green'
            image_container.content = ft.Image(src=f"{local_path}/resource/assets/photo/WiFi.png")
            page.update()
            return True

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
                    ft.Text(text6),  # Заголовок с текстом
                ],
                spacing=10,  # Расстояние между иконкой и текстом
                alignment=ft.MainAxisAlignment.START,  # Выравнивание слева
            ),
            content=ft.Container(
                content=ft.Text(text7),
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

    def LoaderDialog(key=None):
        if key == 'reset': key = text8; key_desc = text9
        if key == 'automation': key = text10; key_desc = text11
        dlg_modal = ft.AlertDialog(
            modal=True,
            barrier_color=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            bgcolor='#1c1c1e',
            title=ft.Container(
                content=ft.Text(
                    key,
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,  # Центрирование текста
                ),
                alignment=ft.alignment.center,
                padding=5,  # Добавлен нижний отступ
            ),
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=ft.Container(
                width=120,
                height=150,  # Увеличена высота для размещения текста
                border_radius=10,
                alignment=ft.alignment.center,  # Центрирование контейнера
                content=ft.Column(
                    [
                        ft.ProgressRing(width=80, height=80, color='#3498db'),
                        ft.Text(
                            key_desc,
                            size=12,
                            weight=ft.FontWeight.NORMAL,
                            text_align=ft.TextAlign.CENTER,  # Центрирование текста
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Центрирование содержимого по вертикали
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Центрирование содержимого по горизонтали
                    spacing=30,  # Расстояние между ProgressRing и Text
                ),
            )
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True  # Открыть диалог
        page.update()
        return dlg_modal

    def ErrorResetDialog(key=None):
        if key == 'reset': title = text12; key = text13
        if key == 'automation': title = text14; key = text15
        def handle_close(e):
            dlg_modal.open = False  # Закрыть диалог
            page.update()  # Обновить страницу

        dlg_modal = ft.AlertDialog(
            modal=True,
            barrier_color=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            bgcolor='#1c1c1e',
            title=ft.Row(
                [
                    ft.Icon(name=ft.Icons.WARNING, color="red", size=30),
                    ft.Text(title),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
            ),
            content=ft.Container(
                width=320,  # Ширина окна
                height=80,  # Высота окна
                content=ft.Text(key, text_align=ft.alignment.start),
            ),
            actions=[
                ft.TextButton("Retry", on_click=lambda _: NextUpdate()),
                ft.TextButton("Cancel", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True  # Открыть диалог
        page.update()

    def NextUpdate():
        if segmented_button.selected_index == 0:
            if Check_iPhoneConnection():
                segmented_button.selected_index = 1
                text_content.value = text1
                usb_container.visible = False
                wifi_container.visible = True
                usb_appbar_button.icon_color = 'green'
                image_container.content = ft.Image(src=f"{local_path}/resource/assets/photo/WiFi.png")
                page.update()
                return True

            page.update()
            return False

        if segmented_button.selected_index == 1:
            if WifiDialog() is False:
                wifi_appbar_button.bgcolor = 'red'
                page.update()
                return False

        if segmented_button.selected_index == 2:
            reset_container.bgcolor = 'black'
            dlg_modal = LoaderDialog('reset')
            TerminalShow()
            if iPhoneReset(udid) is False:
                reset_appbar_button.icon_color = 'red'
                ErrorResetDialog('reset')
                return False
            dlg_modal.open = False
            TerminalHide()
            page.update()

            button_next.disabled = False
            segmented_button.selected_index = 3
            text_content.value = text2
            wifi_container.visible = False
            reset_container.visible = False
            automation_container.visible = True
            image_container.content = ft.Image(src=f"{local_path}/resource/assets/photo/Automation.png")
            reset_appbar_button.icon_color = 'green'
            page.update()
            return True

        if segmented_button.selected_index == 3:
            automation_container.bgcolor = 'black'
            dlg_modal = LoaderDialog('automation')
            TerminalShow()
            if iPhone_ConnectPC(udid) is False:
                ErrorResetDialog('automation')
                automation_appbar_button.icon_color = 'red'
                page.update()
                return False
            automation_appbar_button.icon_color = 'green'
            dlg_modal.open = False
            TerminalHide()
            page.update()


            segmented_button.selected_index = 4
            text_content.value = text3
            wifi_container.visible = False
            reset_container.visible = False
            automation_container.visible = False
            tiktok_container.visible = True
            image_container.content = ft.Image(src=f"{local_path}/resource/assets/photo/LoginAppleID.png")
            button_next.text = text19
            page.update()
            return True

        if segmented_button.selected_index == 4:
            page.go("/MainMenuPage")

    def WifiDialog():
        def handle_close(e):
            dlg_modal.open = False
            page.update()

        def handle_generate(e):
            if Create_WiFiconfig(login_field.value, password_field.value) is False:
                dlg_modal.content.controls[0].value = text16
                wifi_appbar_button.icon_color = 'red'
                dlg_modal.title.controls[0].color = "red"
                page.update()
                return False
            dlg_modal.open = False
            text_content.value = text4
            segmented_button.selected_index = 2
            reset_container.visible = True
            wifi_container.visible = False
            automation_container.visible = False
            image_container.content = ft.Image(src=f"{local_path}/resource/assets/photo/ResetLoading.png")
            wifi_appbar_button.icon_color = 'green'
            page.update()
            return True

        login_field = ft.TextField(label="Login", autofocus=True, width=250, border_color='grey')
        password_field = ft.TextField(label="Password", autofocus=True, width=250, border_color='grey')

        dlg_modal = ft.AlertDialog(
            modal=True,
            barrier_color=ft.Colors.with_opacity(0.65, ft.Colors.BLACK),
            bgcolor='#1c1c1e',
            title=ft.Row(
                [
                    ft.Icon(name=ft.Icons.WARNING, color="yellow", size=30),  # Иконка "warning"
                    ft.Text(text20),  # Заголовок с текстом
                ],
                spacing=10,  # Расстояние между иконкой и текстом
                alignment=ft.MainAxisAlignment.START,  # Выравнивание слева
            ),
            content=ft.Column(
                controls=[
                    ft.Text(text17),
                    login_field,
                    password_field,
                ],
                spacing=11,
                height=130,  # Ограничиваем высоту контента
            ),
            actions=[
                ft.TextButton("Submit", on_click=handle_generate),
                ft.TextButton("Cancel", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END
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
    page.bgcolor = "#191919"

    page.fonts = {
        "TikTok Bold": "fonts/TikTokText-Bold.ttf",
        "TikTok Medium": "fonts/TikTokText-Medium.ttf",
        "TikTok Regular": "fonts/TikTokText-Regular.ttf",
    }

    wifi_appbar_button = ft.IconButton(
                    icon=ft.Icons.WIFI,  # Иконка
                    icon_size=20,
                    tooltip="WiFi Settings",
                    icon_color="white",  # Цвет иконки
                    visible=True,
                    disabled=True
                )

    usb_appbar_button = ft.IconButton(
                    icon=ft.Icons.USB,  # Иконка
                    icon_size=20,
                    tooltip="iPhone Connection",
                    icon_color="white",  # Цвет иконки
                    visible=True,
                    disabled=True
                )

    reset_appbar_button = ft.IconButton(
                    icon=ft.Icons.SETTINGS_BACKUP_RESTORE,  # Иконка
                    icon_size=20,
                    tooltip="Reset iPhone",
                    icon_color="white",  # Цвет иконки
                    visible=True,
                    disabled=True
                )

    automation_appbar_button = ft.IconButton(
                    icon=ft.Icons.TERMINAL,  # Иконка
                    icon_size=20,
                    tooltip="Check Automation",
                    icon_color="white",  # Цвет иконки
                    visible=True,
                    disabled=True
                )

    page.appbar = ft.AppBar(
        title=ft.Text("SETUP YOUR IPHONE", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,
        leading=ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=lambda e: BackButton()),
        actions=[
            ft.Container(  # Оборачиваем кнопку в контейнер для отступа
                content=usb_appbar_button
            ),
            ft.Container(  # Оборачиваем кнопку в контейнер для отступа
                content=wifi_appbar_button
            ),
            ft.Container(  # Оборачиваем кнопку в контейнер для отступа
                content=reset_appbar_button
            ),
            ft.Container(  # Оборачиваем кнопку в контейнер для отступа
                content=automation_appbar_button
            ),
        ]
    )

    # Элементы для сегментированной кнопки
    segmented_button = ft.CupertinoSegmentedButton(
        selected_index=0,
        border_color='#191919',
        click_color='black',
        unselected_color='black',
        selected_color='#27ae60',
        disabled=True,
        controls=[
            ft.Container(
                padding=ft.padding.symmetric(0, 20),
                content=ft.Text("USB", color='white'),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 20),
                content=ft.Text("WIFI", color='white'),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 20),
                content=ft.Text("RESET", color='white'),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 20),
                content=ft.Text("AUTOMATE", color='white'),
            ),
            ft.Container(
                padding=ft.padding.symmetric(0, 20),
                content=ft.Text("FINISH", color='white'),
            ),
        ],
        top=50,
        left=351
    )

    # Контейнер с изображением (он будет виден поверх других элементов)
    image_container = ft.Container(
        content=ft.Image(src=f"{local_path}/resource/assets/photo/ConnectPC.png",),
        left=-140,  # Горизонтальное смещение
        top=-120,   # Верхнее смещение
    )

    text_content = ft.Text(text5, size=16, font_family="TikTok Regular")

    text_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=text_content,
                    padding=ft.padding.only(bottom=0),
                ),
            ],
            spacing=10,  # Расстояние между текстом и иконкой
        ),
        width=400,  # Ширина контейнера
        alignment=ft.alignment.center,  # Выравнивание текста и иконки
        padding=ft.padding.all(10),  # Отступы внутри контейнера
        left=360,  # Горизонтальное смещение контейнера
        top=120,  # Вертикальное смещение контейнера
    )

    usb_container = create_icon_container(
        icon=ft.Icons.USB,
        icon_size=40,
        icon_color="white",
        bgcolor="black",
    )

    wifi_container = create_icon_container(
        icon=ft.Icons.WIFI,
        icon_size=40,
        icon_color="white",
        bgcolor="black",
        on_click=lambda e: WifiDialog()
    )
    wifi_container.visible = False

    reset_container = create_icon_container(
        icon=ft.Icons.LOCK_RESET,
        icon_size=40,
        icon_color="white",
        bgcolor="black"
    )
    reset_container.visible = False

    automation_container = create_icon_container(
        icon=ft.Icons.TERMINAL,
        icon_size=40,
        icon_color="white",
        bgcolor="black"
    )
    automation_container.visible = False

    tiktok_container = create_icon_container(
        icon=ft.Icons.APPLE,
        icon_size=40,
        icon_color="white",
        bgcolor="black"
    )
    tiktok_container.visible = False

    button_next = ft.ElevatedButton(
        text=text18,
        width=100,
        height=50,
        on_click=lambda e: NextUpdate()
    )


    buttons_container = ft.Container(
        content=ft.Column(
            controls=[
                usb_container,
                wifi_container,
                reset_container,
                automation_container,
                tiktok_container,
                button_next
            ],
            spacing=20,  # Отступ между `Row` в `Column`
            alignment=ft.MainAxisAlignment.START,  # Выравнивание по началу
        ),
        alignment=ft.alignment.center,  # Выравнивание контейнера по центру
        top=133,  # Смещение вниз
        left=828,  # Смещение вправо
    )

    # Основной Stack
    stack = ft.Stack(
        controls=[
            image_container,  # Изображение будет первым в списке (оно будет на фоне)
            segmented_button,
            text_container,
            buttons_container,
        ],
    )

    page.add(stack)