import pytest
import requests
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

    response = api_client.post(Urls.REGISTER, json=user_data)
    if response.status_code == 403:
        user_data['email'] = generate_email()
        response = api_client.post(Urls.REGISTER, json=user_data)

    assert response.status_code == 200, f"Failed to register user: {response.text}"

    login_response = api_client.post(Urls.LOGIN, json={
        'email': user_data['email'],
        'password': user_data['password']
    })
    assert login_response.status_code == 200, f"Failed to login: {login_response.text}"

    token = login_response.json().get('accessToken', '')

    yield {
        'email': user_data['email'],
        'password': user_data['password'],
        'name': user_data['name'],
        'token': token
    }

    if token:
        try:
            api_client.delete(Urls.USER, headers={'Authorization': token})
        except requests.exceptions.RequestException:
            pass
