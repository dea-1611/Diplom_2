import pytest
import allure
from helpers.api_client import APIClient
from helpers.data_generator import generate_email, generate_password, generate_name
from helpers.urls import Urls


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def registered_user(api_client):
    user_data = {
        'email': generate_email(),
        'password': generate_password(),
        'name': generate_name()
    }

    # Регистрация
    response = api_client.post(Urls.REGISTER, json=user_data)
    if response.status_code == 403:
        # Пользователь уже существует, пробуем с новыми данными
        user_data['email'] = generate_email()
        response = api_client.post(Urls.REGISTER, json=user_data)

    assert response.status_code == 200, f"Failed to register user: {response.text}"

    # Логин для получения токена
    login_response = api_client.post(Urls.LOGIN, json={
        'email': user_data['email'],
        'password': user_data['password']
    })
    assert login_response.status_code == 200, f"Failed to login: {login_response.text}"

    token = login_response.json().get('accessToken', '')

    yield {
        'email': user_data['email'],
        'password': user_data['password'],
        'token': token
    }

    # Удаление пользователя
    if token:
        api_client.delete(Urls.USER, headers={'Authorization': token})