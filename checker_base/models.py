from django.db import models


class PhoneGroup(models.Model):
    prefix = models.IntegerField(db_index=True, help_text='Первые 3 цифры номера телефона')
    start_range = models.IntegerField(db_index=True, help_text='Начало диапазона номеров')
    end_range = models.IntegerField(db_index=True, help_text='Конец диапазона номеров')

    operator = models.CharField(max_length=255, help_text='Оператор номеров')
    region = models.CharField(max_length=255, help_text='Регион номеров')
    inn = models.IntegerField(help_text='ИНН оператора')
