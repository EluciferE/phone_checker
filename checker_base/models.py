from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=255, help_text='Название региона')

    def __str__(self):
        return self.name


class Operator(models.Model):
    name = models.CharField(max_length=255, help_text='Название оператора')
    inn = models.CharField(help_text='ИНН оператора')

    def __str__(self):
        return f'{self.name} ({self.inn})'


class PhoneGroup(models.Model):
    prefix = models.IntegerField(db_index=True, help_text='Первые 3 цифры номера телефона')
    start_range = models.IntegerField(db_index=True, help_text='Начало диапазона номеров')
    end_range = models.IntegerField(db_index=True, help_text='Конец диапазона номеров')

    operator = models.ForeignKey(Operator, help_text='Оператор номеров', on_delete=models.CASCADE)
    region = models.ForeignKey(Region, help_text='Регион номеров', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.prefix} [{self.start_range} - {self.end_range}]'
