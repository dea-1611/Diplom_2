import allure
from helpers.data_generator import generate_email, generate_password
from helpers.urls import Urls

@allure.feature('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Вход с валидными учетными данными')
    def test_login_valid_user(self, api_client, registered_user):
        with allure.step('Подготовка валидных учетных данных'):
            credentials = {
                'email': registered_user['email'],
                'password': registered_user['password']
            }

        with allure.step('Отправка запроса на авторизацию'):
            response = api_client.post(Urls.LOGIN, json=credentials)

        with allure.step('Проверка успешной авторизации'):
            assert response.status_code == 200
            assert response.json()['success'] is True
            assert 'accessToken' in response.json()

    @allure.title('Вход с невалидным email')
    def test_login_invalid_email(self, api_client, registered_user):
        with allure.step('Подготовка невалидных учетных данных'):
            credentials = {
                'email': generate_email(),  # случайный несуществующий email
                'password': registered_user['password']  # правильный пароль
            }

        with allure.step('Отправка запроса на авторизацию с неверным email'):
            response = api_client.post(Urls.LOGIN, json=credentials)

        with allure.step('Проверка ошибки авторизации'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == 'email or password are incorrect'

    @allure.title('Вход с невалидным паролем')
    def test_login_invalid_password(self, api_client, registered_user):
        with allure.step('Подготовка невалидных учетных данных'):
            credentials = {
                'email': registered_user['email'],  # правильный email
                'password': generate_password()  # случайный неверный пароль
            }

        with allure.step('Отправка запроса на авторизацию с неверным паролем'):
            response = api_client.post(Urls.LOGIN, json=credentials)

        with allure.step('Проверка ошибки авторизации'):
            assert response.status_code == 401
            assert response.json()['success'] is False
            assert response.json()['message'] == 'email or password are incorrect'