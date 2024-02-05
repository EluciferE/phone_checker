# Phone Checker

![Phone Checker](https://i.ibb.co/1nkHxv0/Screenshot-2.png)
### <code>[Check demo](http://194.87.99.80/)</code>

������ Phone Checker ������������� ����������� �������� ���������� �� ������ �������� ����� ���-���������. ���������� �� Django, DRF, Celery, � �������������� PostgreSQL � �������� ���� ������, Redis ��� �������� �������� �����. ��� ���������� ������������ ������������ Docker � Docker Compose.

## ��� �������������

1. ���������� ���� pre-commit ��� ��������� �������������� �������������� ����:

   ```bash
   pre-commit install

# ������ Phone Checker

��������� ���������� ������� ��� ���������� ������ Phone Checker � �������������� Docker � Docker Compose.

## ���� �� ������

1. **����������� �����������:**

    ```bash
    git clone https://github.com/EluciferE/phone_checker.git
    ```

2. **���������� Docker � Docker Compose.**

3. **��������� ���� `.env` ������ ����������:**

4. **��������� ���������� � ������ detached:**

    ```bash
    docker-compose up --build -d
    ```

5. **���� �������� � ����� `phone_checker/logs/django` � `phone_checker/logs/celery`.**
