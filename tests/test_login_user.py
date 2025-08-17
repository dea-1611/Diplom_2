import allure
from helpers.api_client import APIClient
from helpers.data_generator import generate_email, generate_password
from helpers.urls import Urls


@allure.feature('User Login')
class TestLoginUser:
    @allure.title('Login with valid credentials')
    def test_login_valid_user(self, api_client, registered_user):
        response = api_client.post(Urls.LOGIN, json={
            'email': registered_user['email'],
            'password': registered_user['password']
        })

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'accessToken' in response.json()

    @allure.title('Login with invalid credentials')
    def test_login_invalid_credentials(self, api_client):
        response = api_client.post(Urls.LOGIN, json={
            'email': generate_email(),
            'password': generate_password()
        })

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == 'email or password are incorrect'