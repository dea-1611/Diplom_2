import allure
import pytest
from helpers.api_client import APIClient
from helpers.data_generator import generate_email, generate_password, generate_name
from helpers.urls import Urls


@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self, api_client):
        user_data = {
            'email': generate_email(),
            'password': generate_password(),
            'name': generate_name()
        }

        response = api_client.post(Urls.REGISTER, json=user_data)

        if response.status_code == 403:
            user_data['email'] = generate_email()
            response = api_client.post(Urls.REGISTER, json=user_data)

        assert response.status_code == 200, f"Failed to register user: {response.text}"
        assert response.json()['success'] is True
        assert 'accessToken' in response.json()

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_duplicate_user(self, api_client):
        user_data = {
            'email': generate_email(),
            'password': generate_password(),
            'name': generate_name()
        }

        api_client.post(Urls.REGISTER, json=user_data)

        response = api_client.post(Urls.REGISTER, json=user_data)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Создание пользователя без заполнения одного из обязательных полей')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, api_client, field):
        user_data = {
            'email': generate_email(),
            'password': generate_password(),
            'name': generate_name()
        }
        del user_data[field]

        response = api_client.post(Urls.REGISTER, json=user_data)

        assert response.status_code == 403
        assert response.json()['success'] is False

        assert response.json()['message'] == 'Email, password and name are required fields'

