from datetime import datetime
# Класс «обёртки»
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser

from app.crud.charity_project import charity_project_crud
from app.utils.google_api import (set_user_permissions,
                                  spreadsheets_create,
                                  spreadsheets_update_value)

# Создаём экземпляр класса APIRouter
router = APIRouter()


@router.post(
    '/',
    # Тип возвращаемого эндпоинтом ответа
    response_model=list[dict[str, int]],
    # Определяем зависимости
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        # Начало периода
        from_reserve: datetime,
        # Конец периода
        to_reserve: datetime,
        # Сессия
        session: AsyncSession = Depends(get_async_session),
        # «Обёртка»
        wrapper_services: Aiogoogle = Depends(get_service)

):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id,
                                    projects,
                                    wrapper_services)
    return projects