import logging
import typing
from io import BytesIO

import pandas as pd
import requests
from celery import shared_task

from checker_base.models import Operator, PhoneGroup, Region

sync_phones_logger = logging.getLogger('sync_phones')


class PhoneRow(typing.TypedDict):
    prefix: int
    start: int
    end: int
    operator_name: str
    region_name: str
    operator_inn: int


def remove_empty_operators_and_regions():
    """
    Удаляем всех операторов и регионы, у которых не осталось привязок к номерам
    """
    used_ids = PhoneGroup.objects.values_list('operator__id', 'region__id').distinct()

    used_operator_ids, used_region_ids = zip(*used_ids)

    unused_operators = Operator.objects.exclude(id__in=used_operator_ids)
    unused_regions = Region.objects.exclude(id__in=used_region_ids)

    sync_phones_logger.info(f'Delete unused operators: {unused_operators.count()}')
    sync_phones_logger.info(f'Delete unused regions: {unused_regions.count()}')

    unused_operators.delete()
    unused_regions.delete()


def check_unlisted_phones(dataframe: pd.DataFrame, first_digit: int):
    """
    Проверяем номера из базы данных, что они находятся в файле. Если их нет, то удаляем
    """
    prefix_start = first_digit * 100
    prefix_end = prefix_start + 99

    phone_groups = PhoneGroup.objects.filter(
        prefix__gte=prefix_start,
        prefix__lte=prefix_end,
    ).iterator(chunk_size=10000)

    deleted_count = 0

    for phone_group in phone_groups:
        matched_rows = dataframe[
            (dataframe['prefix'] == phone_group.prefix) &
            (dataframe['start'] == phone_group.start_range) &
            (dataframe['end'] == phone_group.end_range)
        ]

        if matched_rows.empty:
            phone_group.delete()
            deleted_count += 1

    sync_phones_logger.info(f'Deleted unlisted phones: {deleted_count}, {first_digit = }')


def update_phone_group(phone_group: PhoneGroup, phone_row: PhoneRow):
    """
    Обновляем информацию об операторе / регионе телефонной группы
    """
    if phone_group.operator.name != phone_row['operator_name'] or \
            phone_group.operator.inn != phone_row['operator_inn']:

        phone_group.operator = Operator.objects.create(
            name=phone_row['operator_name'],
            inn=phone_row['operator_inn'],
        )

    if phone_group.region.name != phone_row['region_name']:
        phone_group.region = Region.objects.create(name=phone_row['region_name'])

    phone_group.save(update_fields=['operator', 'region'])


def create_phone_group(phone_row: PhoneRow):
    PhoneGroup.objects.create(
        prefix=phone_row['prefix'],
        start_range=phone_row['start'],
        end_range=phone_row['end'],
        operator=Operator.objects.get_or_create(
            name=phone_row['operator_name'],
            inn=phone_row['operator_inn'],
        )[0],
        region=Region.objects.get_or_create(
            name=phone_row['region_name'],
        )[0],
    )


def check_listed_phones(dataframe: pd.DataFrame):
    created_count = 0

    for index, row in dataframe.iterrows():
        phone_row: PhoneRow = typing.cast(PhoneRow, dict(row))

        phone_group = PhoneGroup.objects.filter(
            prefix=phone_row['prefix'],
            start_range__lte=phone_row['start'],
            end_range__gte=phone_row['end'],
        ).select_related('operator', 'region').first()

        if phone_group is not None:
            update_phone_group(phone_group, phone_row)
        else:
            create_phone_group(phone_row)
            created_count += 1

    sync_phones_logger.info(f'Created phones: {created_count}')


def rename_df_columns(dataframe: pd.DataFrame):
    map_columns = {
        'АВС/ DEF': 'prefix',
        'От': 'start',
        'До': 'end',
        'Оператор': 'operator_name',
        'Регион': 'region_name',
        'ИНН': 'operator_inn',
    }

    dataframe.rename(map_columns)


@shared_task(
    autoretry_for=(requests.exceptions.RequestException,),
    default_retry_delay=60 * 5,
    max_retries=5,
)
def sync_single_file(url: str, first_digit: int):
    sync_phones_logger.info(f'Sync with {url!r}')

    response = requests.get(url, verify=False)
    df = pd.read_csv(BytesIO(response.content), sep=';')
    rename_df_columns(df)

    check_unlisted_phones(df, first_digit)
    check_listed_phones(df)


@shared_task
def sync_phone_numbers():
    sync_phones_logger.info('Start to sync phone numbers')
    urls = {
        3: 'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv',
        4: 'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv',
        8: 'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv',
        9: 'https://opendata.digital.gov.ru/downloads/ABC-9xx.csv',
    }
    for first_digit, url in urls.items():
        sync_single_file(url, first_digit)

    remove_empty_operators_and_regions()

    sync_phones_logger.info('End sync phone numbers')