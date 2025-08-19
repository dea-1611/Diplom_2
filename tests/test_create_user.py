import allure
import pytest
from helpers.data_generator import generate_email, generate_password, generate_name
from helpers.urls import Urls


@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self, api_client):
        with allure.step('Генерация тестовых данных пользователя'):
            user_data = {
                'email': generate_email(),
                'password': generate_password(),
                'name': generate_name()
            }

        with allure.step('Отправка запроса на регистрацию'):
            response = api_client.post(Urls.REGISTER, json=user_data)

        with allure.step('Проверка успешной регистрации'):
            assert response.status_code == 200, f"Не удалось зарегистрировать пользователя: {response.text}"
            assert response.json()['success'] is True
            assert 'accessToken' in response.json()

        with allure.step('Удаление тестового пользователя'):
            token = response.json()['accessToken']
            api_client.delete(Urls.USER, headers={'Authorization': token})

    @allure.title('Создание дубликата пользователя')
    def test_create_duplicate_user(self, api_client, registered_user):
        with allure.step('Подготовка данных существующего пользователя'):
            user_data = {
                'email': registered_user['email'],
                'password': registered_user['password'],
                'name': registered_user['name']
            }

        with allure.step('Попытка регистрации с существующими данными'):
            response = api_client.post(Urls.REGISTER, json=user_data)

        with allure.step('Проверка ошибки дублирования пользователя'):
            assert response.status_code == 403
            assert response.json()['success'] is False
            assert response.json()['message'] == 'User already exists'

    @allure.title('Создание пользователя с отсутствующим полем')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, api_client, field):
        with allure.step('Генерация тестовых данных пользователя'):
            user_data = {
                'email': generate_email(),
                'password': generate_password(),
                'name': generate_name()
            }

        with allure.step(f'Удаление поля {field}'):
            del user_data[field]

        with allure.step('Отправка запроса на регистрацию с неполными данными'):
            response = api_client.post(Urls.REGISTER, json=user_data)

        with allure.step('Проверка ошибки отсутствия обязательного поля'):
            assert response.status_code == 403
            assert response.json()['success'] is False
            assert response.json()['message'] == 'Email, password and name are required fields'