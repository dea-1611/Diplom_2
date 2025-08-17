import allure
from helpers.api_client import APIClient
from helpers.data_generator import generate_email, generate_password
from helpers.urls import Urls


@allure.feature('логин пользователя')
class TestLoginUser:
    @allure.title('Вход под существующим пользователем')
    def test_login_valid_user(self, api_client, registered_user):
        response = api_client.post(Urls.LOGIN, json={
            'email': registered_user['email'],
            'password': registered_user['password']
        })

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'accessToken' in response.json()

    @allure.title('Вход с неверным логином')
    def test_login_invalid_email(self, api_client, registered_user):
        response = api_client.post(Urls.LOGIN, json={
            'email': generate_email(),
            'password': registered_user['password']
        })

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'

    @allure.title('Вход с неверным паролем')
    def test_login_invalid_password(self, api_client, registered_user):
        response = api_client.post(Urls.LOGIN, json={
            'email': registered_user['email'],
            'password': generate_password()
        })

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'
