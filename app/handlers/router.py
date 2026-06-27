from aiogram import Router

from . import start, booking

# Соглашение: при добавлении нового модуля с хендлерами нужно обновить два места:
# 1. Добавить импорт модуля в эту строку выше
# 2. Передать его router в master_router.include_routers() ниже
# Порядок важен: admin.router должен идти последним, так как его фильтр
# по from_user.id не должен перехватывать общие callback'и раньше других роутеров.


def get_root_router() -> Router:
    master_router = Router()

    master_router.include_routers(
        start.router, booking.router,
    )

    return master_router
