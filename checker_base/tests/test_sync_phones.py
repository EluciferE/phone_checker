from pathlib import Path
from unittest.mock import MagicMock, patch

from django.db import models
from django.test import TestCase

from checker_base.models import Operator, PhoneGroup, Region
from checker_base.tasks.sync_phones import remove_empty_operators_and_regions, sync_single_file


class MockGetResponse:
    def __init__(self, content):
        self.content = content


TEST_DIR = Path(__file__).parent
TEST_DIGIT_CSV = TEST_DIR / 'digit-9.csv'


class SyncPhonesTest(TestCase):
    def test_remove_empty_regions(self):
        """
        Проверяем, что регионы и операторы без привязок удаляются
        """

        test_region = Region.objects.create(name='test')
        test_operator = Operator.objects.create(name='test', inn=0)
        PhoneGroup.objects.create(
            prefix=0, start_range=0, end_range=0,
            region=test_region, operator=test_operator,
        )

        Operator.objects.create(name='empty', inn=0)
        Region.objects.create(name='empty')

        self.assertEqual(Operator.objects.count(), 2)
        self.assertEqual(Region.objects.count(), 2)

        remove_empty_operators_and_regions()

        self.assertEqual(Operator.objects.count(), 1)
        self.assertEqual(Region.objects.count(), 1)
        self.assertEqual(Operator.objects.first().name, 'test')

    @patch('checker_base.tasks.sync_phones.requests.get')
    def test_sync_phones(self, get_mock: MagicMock):
        """
        Проверяем, что создастся номера, которые были в csv файле
        """

        get_mock.return_value = MockGetResponse(content=open(TEST_DIGIT_CSV, 'rb').read())
        sync_single_file(url='test_url', first_digit=9)

        get_mock.assert_called_once()

        self.assertEqual(PhoneGroup.objects.count(), 6)
        self.assertEqual(Operator.objects.count(), 2)
        self.assertEqual(Region.objects.count(), 5)

    @patch('checker_base.tasks.sync_phones.requests.get')
    def test_delete_unlisted_phone(self, get_mock: MagicMock):
        """
        Проверка, что удалится группа, которой нет в списке телефонов
        """

        get_mock.return_value = MockGetResponse(content=open(TEST_DIGIT_CSV, 'rb').read())
        operator = Operator.objects.create(name='test', inn='0')
        region = Region.objects.create(name='test')
        phone_group = PhoneGroup.objects.create(
            prefix=999, start_range=0, end_range=0,
            operator=operator, region=region,
        )

        sync_single_file(url='test_url', first_digit=9)
        remove_empty_operators_and_regions()

        self.assertRaises(models.ObjectDoesNotExist, phone_group.refresh_from_db)
        self.assertRaises(models.ObjectDoesNotExist, operator.refresh_from_db)
        self.assertRaises(models.ObjectDoesNotExist, region.refresh_from_db)
