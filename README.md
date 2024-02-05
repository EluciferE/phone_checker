# Phone Checker

![Phone Checker](https://i.ibb.co/1nkHxv0/Screenshot-2.png)
### <code>[Check demo](http://194.87.99.80/)</code>

Проект Phone Checker предоставляет возможность получить информацию по номеру телефона через веб-интерфейс. Реализован на Django, DRF, Celery, с использованием PostgreSQL в качестве базы данных, Redis для хранения очередей задач. Для управления контейнерами используется Docker и Docker Compose.

## Для Разработчиков

1. Установите хуки pre-commit для поддержки единообразного форматирования кода:

   ```bash
   pre-commit install

# Деплой Phone Checker

Следующая инструкция поможет вам развернуть проект Phone Checker с использованием Docker и Docker Compose.

## Шаги по деплою

1. **Склонируйте репозиторий:**

    ```bash
    git clone https://github.com/EluciferE/phone_checker.git
    ```

2. **Установите Docker и Docker Compose.**

3. **Заполните файл `.env` своими значениями:**

4. **Запустите приложение в режиме detached:**

    ```bash
    docker-compose up --build -d
    ```

5. **Логи доступны в папке `phone_checker/logs/django` и `phone_checker/logs/celery`.**
