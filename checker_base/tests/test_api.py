from django.test import TestCase

from checker_base.models import Operator, PhoneGroup, Region


class PhoneInfoTest(TestCase):
    PREFIX = '999'
    START = 0
    END = 9999999

    PHONE = '79990000001'
    PHONE_2 = 's1234567890'

    def test_existing_phone(self):
        """
        Проверка, что номер находится, если он был в базе данных
        """
        test_operator = Operator.objects.create(
            name='test_operator',
            inn=999999,
        )
        test_region = Region.objects.create(name='test_region')
        phone_group = PhoneGroup.objects.create(
            prefix=self.PREFIX,
            start_range=self.START,
            end_range=self.END,
            operator=test_operator,
            region=test_region,
        )

        response = self.client.get(f'/api/v1/phone_info?phone={self.PHONE}')

        self.assertEqual(response.status_code, 200)

        r_json = response.json()
        self.assertEqual(r_json['status'], 'OK')

        data = r_json['data']
        self.assertEqual(data['phone'], self.PHONE)
        self.assertEqual(data['operator'], phone_group.operator.name)
        self.assertEqual(data['region'], phone_group.region.name)

    def test_unlisted_phone(self):
        """
        Проверка ошибки, если телефона нет в базе данных
        """
        response = self.client.get(f'/api/v1/phone_info?phone={self.PHONE}')
        r_json = response.json()

        self.assertEqual(r_json['status'], 'error')

        error = r_json['data']['phone'][0]
        self.assertEqual(error, 'Номер не найден в базе данных')

    def test_badformat_phone(self):
        """
        Проверка ошибки, если введен неверный формат телефона
        """
        response = self.client.get(f'/api/v1/phone_info?phone={self.PHONE_2}')
        r_json = response.json()

        self.assertEqual(r_json['status'], 'error')

        error = r_json['data']['phone'][0]
        self.assertEqual(error, 'Некорректный номер телефона')
