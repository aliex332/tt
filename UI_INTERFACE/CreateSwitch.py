import flet as ft

def create_switch(
    label: str,
    icon: ft.Icon,
    icon_color: str = "black",
    value: bool = False,
    on_change=None,
    track_color=None,
    thumb_color="white",
    label_style=None,
    visible=True,
):
    """
    Создает переключатель с иконкой.
    """
    return ft.Row(
        controls=[
            ft.Icon(name=icon.name, size=icon.size, color=icon_color, visible=visible),  # Иконка
            ft.Switch(
                value=value,
                label=label,
                visible=visible,
                label_position=ft.LabelPosition.LEFT,
                thumb_color=thumb_color,
                track_color=track_color or {
                    ft.ControlState.SELECTED: ft.Colors.RED,
                    ft.ControlState.DEFAULT: ft.Colors.GREY,
                },
                focus_color=ft.Colors.PURPLE,
                label_style=label_style
                or ft.TextStyle(size=18, font_family="TikTok Bold"),
                on_change=on_change,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
    )
