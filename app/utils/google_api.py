from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'

SPREADSHEET_BODY = {
    'properties': {'title': '',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': ''
}

UPDATE_BODY_TEMPLATE = {
    'majorDimension': 'ROWS',
    'values': []
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    SPREADSHEET_BODY['properties']['title'] = 'Отчет на {}'.format(
        datetime.now().strftime(FORMAT)
    )
    service = await wrapper_services.discover('sheets', 'v4')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=SPREADSHEET_BODY)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = PERMISSIONS_BODY.copy()
    permissions_body['emailAddress'] = settings.email

    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: list,
    wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчет от', now_date_time],
        ['Список проектов быстрее всего набравших сумму'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for proj in projects:
        new_row = [str(proj['name']), str(
            proj['project_lifetime']), str(proj['description'])]
        table_values.append(new_row)

    update_body = UPDATE_BODY_TEMPLATE.copy()
    update_body['values'] = table_values

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )