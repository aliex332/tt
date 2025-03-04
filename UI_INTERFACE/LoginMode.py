import os
import sys
import platform
import webbrowser
import flet as ft

if getattr(sys, 'frozen', False): local_path = f'{os.path.dirname(sys.executable)}'.replace('\\', '/')
else: local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

def LoginModePage(page: ft.Page):
    if page.client_storage.get("Localisation") == 'EN':
        text1 = "Network settings will be reset before a new registration or if you get errors."
        text2 = "Mobile Network will be used instead of WiFi. Make sure your SIM card is working."
        text3 = "Before start, you need to configure your accounts list."
        text4 = "After finishing accounts, list will repeat for the numbers of laps."


    if page.client_storage.get("Localisation") == 'RU':
        text1 = "Настройки сети будут сброшены перед новой регистрацией или в случае возникновения ошибок."
        text2 = "Мобильная сеть будет использоваться вместо WiFi. Убедитесь, что ваша SIM-карта работает."
        text3 = "Перед началом вам нужно настроить ваш список с аккаунтами."
        text4 = "Когда аккаунты в списке закончатся, список будет повторяться указанное число раз."
    
    def UpdateStorage(switch_mobile_network=None, switch_reset_network=None, txt_number=None):
        page.client_storage.set("mobile_network", switch_mobile_network.value)
        page.client_storage.set("reset_network", switch_reset_network.value)
        page.client_storage.set("account_list_laps", int(txt_number.value))

    def OpenFolder(action):
        if action == 'ACCOUNTS':
            if platform.system() == "Windows": os.startfile(f'{local_path}/iPhoneTikTokFiles/AccountsDataBase/')
            if platform.system() == "Darwin": os.system(f'open {local_path}/iPhoneTikTokFiles/AccountsDataBase/')

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

    next_button = ft.ElevatedButton(
        text="NEXT",  # Текст кнопки
        on_click=lambda e: (UpdateStorage(switch_mobile_network, switch_reset_network, txt_number), page.go("/UploadModePage")),
        color="white",  # Цвет текста
        bgcolor="grey",  # Изначально серый фон
        disabled=True,  # Кнопка неактивна
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),  # Закругленные углы
        ),
    )

    def open_url_info(e):
        if page.client_storage.get("Localisation") == 'EN': webbrowser.open('https://google.com', new=2)  # new=2 откроет в новом окне/вкладке
        if page.client_storage.get("Localisation") == 'RU': webbrowser.open('https://google.com', new=2)  # new=2 откроет в новом окне/вкладке


    info_button = ft.IconButton(
                    icon=ft.Icons.INFO_OUTLINE_ROUNDED,  # Иконка
                    icon_size=20,
                    tooltip="More information",
                    on_click=lambda e: open_url_info(e),  # Обработчик клика
                    icon_color="white",  # Цвет иконки
                    visible=True
                )

    # Создаем AppBar
    page.appbar = ft.AppBar(
        title=ft.Text("SETUP LOGIN MODE", size=24, color='white', font_family="TikTok Bold"),
        center_title=True,
        bgcolor="black",
        elevation_on_scroll=0,  # Отключаем эффект повышения при скролле
        leading=ft.IconButton(ft.Icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=lambda e: page.go("/MainMenuPage")),
        actions=[
            ft.Container(
                content=info_button,
            ),
            ft.Container(
                content=next_button,
                alignment=ft.alignment.center,  # Центрирование кнопки
                padding=ft.padding.only(right=10),  # Отступ справа для кнопки
            )
        ]
    )

    # Иконки
    mobile_network_icon = ft.Icon(ft.Icons.NETWORK_CELL, size=22, color=ft.Colors.YELLOW)
    reset_icon = ft.Icon(ft.Icons.UPDATE, size=22, color=ft.Colors.RED)

    # Переключатели
    switch_reset_network = ft.Switch(value=False, label="Reset Network ", label_position=ft.LabelPosition.LEFT, thumb_color=ft.Colors.WHITE, track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY}, focus_color=ft.Colors.PURPLE, label_style=ft.TextStyle(size=18, font_family="TikTok Bold"), on_change=lambda e: update_content("reset_network"))
    switch_mobile_network = ft.Switch(value=False, label="Mobile Network ", label_position=ft.LabelPosition.LEFT, thumb_color=ft.Colors.WHITE, track_color={ft.ControlState.SELECTED: ft.Colors.RED, ft.ControlState.DEFAULT: ft.Colors.GREY}, focus_color=ft.Colors.PURPLE, label_style=ft.TextStyle(size=18, font_family="TikTok Bold"), on_change=lambda e: update_content("mobile_network"))

    # Функция для обновления текста и картинки
    image = ft.Image(src=f"{local_path}/resource/assets/photo/Login.png", left=130, top=-130) # Изначальная картинка
    last_active_switch = {"name": None} # Последний активный переключатель
    def update_content(changed_switch=None):
        if changed_switch == "reset_network" and switch_reset_network.value:
            text_content.value = text1
            image.src = f"{local_path}/resource/assets/photo/Reset.png"
            last_active_switch["name"] = "reset_network"
        elif changed_switch == "mobile_network" and switch_mobile_network.value:
            text_content.value = text2
            image.src = f"{local_path}/resource/assets/photo/MobileNetwork.png"
            last_active_switch["name"] = "mobile_network"
        elif not switch_reset_network.value and not switch_mobile_network.value:
            text_content.value = text3
            image.src = f"{local_path}/resource/assets/photo/Login.png"
            last_active_switch["name"] = None
        page.update()

    txt_number = ft.TextField(label="Laps:", value=0, text_align="center", border_radius=0, text_style=ft.TextStyle(font_family="TikTok Bold", size=13, color='WHITE70'),
        width=100,  # Устанавливаем ширину
        height=45,
        border_color='white'
    )

    def enable_next_button():
        if txt_number.value == 'Laps' or txt_number.value == 0:
            next_button.disabled = True
            next_button.bgcolor = "grey"
        else:
            next_button.bgcolor = "red"
            next_button.disabled = False  # Кнопка неактивна

    def validate_number(value):
        enable_next_button()
        return max(int(value), 1) if isinstance(value, str) and value.isdigit() else 0

    def minus_click(e):
        txt_number.value = validate_number(txt_number.value)
        txt_number.value = str(max(int(txt_number.value) - 1, 1))  # Минимальное значение - 1
        text_content.value = text4
        enable_next_button()
        page.update()

    def plus_click(e):
        txt_number.value = validate_number(txt_number.value)
        txt_number.value = str(int(txt_number.value) + 1)
        text_content.value = text4
        enable_next_button()
        page.update()

    def on_change(e):
        txt_number.value = validate_number(txt_number.value)
        enable_next_button()
        page.update()

    txt_number.on_change = on_change


    text_content = ft.Text(
        value=text3,
        size=15,
        font_family="TikTok Regular",
        width=300,
    )

    recover_button = ft.IconButton(
        icon=ft.Icons.FOLDER_COPY_OUTLINED,  # Иконка
        icon_size=30,
        tooltip="Accounts list",
        on_click=lambda e: OpenFolder('ACCOUNTS'),  # Обработчик клика
        icon_color="white",  # Цвет иконки
        visible=True
    )

    right_container = ft.Container(
        content=ft.Column(
            controls=[
                # Первый элемент: текст
                ft.Container(
                    content=text_content,  # Текстовый элемент
                    padding=ft.padding.only(bottom=0),  # Отступ снизу
                ),
                # Второй элемент: поле и кнопки
                ft.Container(
                    content=ft.Row(
                        controls=[
                            txt_number,
                            ft.IconButton(icon=ft.Icons.REMOVE, on_click=minus_click),
                            ft.IconButton(icon=ft.Icons.ADD, on_click=plus_click),
                            recover_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.only(top=10, bottom=20),  # Отступы сверху и снизу
                ),
            ],
            spacing=10,  # Общий отступ между элементами в колонке
        ),
        left=650,
        top=80,
    )

    stack = ft.Stack(
        controls=[
            image,
            right_container,
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[mobile_network_icon, switch_mobile_network],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[reset_icon, switch_reset_network],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ),
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                left=50,
                top=80,
            ),
        ]
    )
    page.add(stack)
