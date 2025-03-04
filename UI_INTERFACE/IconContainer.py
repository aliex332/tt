import flet as ft
import asyncio

def create_icon_container_with_progress(
    icon: str,
    container_size: int = 100,
    icon_size: int = 50,
    bgcolor: str = "#222222",
    icon_color: str = "white"
) -> ft.Container:
    """
    Создает контейнер с иконкой и прогресс-кольцом.

    :param icon: Иконка, например, `ft.Icons.FOLDER_COPY_OUTLINED`.
    :param container_size: Размер контейнера (ширина и высота).
    :param icon_size: Размер иконки.
    :param bgcolor: Цвет фона контейнера.
    :param icon_color: Цвет иконки.
    :return: Контейнер с иконкой и прогресс-кольцом.
    """
    # Создаем контейнер
    return ft.Container(
        width=100,
        height=50,
        bgcolor=bgcolor,
        border_radius=container_size // 10,
        content=ft.Stack(
            controls=[ft.Icon(name=icon, size=icon_size, color=icon_color)],
            alignment=ft.alignment.center,
        ),
        alignment=ft.alignment.center,
    )