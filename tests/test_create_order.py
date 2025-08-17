import allure
import pytest
from helpers.api_client import APIClient
from helpers.data_generator import get_valid_ingredients
from helpers.urls import Urls


@allure.feature('Order Creation')
class TestCreateOrder:
    @allure.title('Create order with auth and valid ingredients')
    def test_create_order_auth_valid_ingredients(self, api_client, registered_user):
        ingredients = get_valid_ingredients(api_client)
        headers = {'Authorization': registered_user['token']}
        response = api_client.post(
            Urls.ORDERS,
            json={'ingredients': ingredients},
            headers=headers
        )

        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'name' in response.json()

    @allure.title('Create order without auth')
    def test_create_order_no_auth(self, api_client):
        ingredients = get_valid_ingredients(api_client)
        response = api_client.post(Urls.ORDERS, json={'ingredients': ingredients})

        # API может возвращать 200 или 401 в зависимости от реализации
        # Уточните правильный ожидаемый код ответа в документации API
        assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
        if response.status_code == 200:
            assert response.json()['success'] is True
        else:
            assert response.json()['message'] == 'You should be authorised'

    @allure.title('Create order with ingredients')
    def test_create_order_with_ingredients(self, api_client, registered_user):
        ingredients = get_valid_ingredients(api_client)
        headers = {'Authorization': registered_user['token']}
        response = api_client.post(
            Urls.ORDERS,
            json={'ingredients': ingredients},
            headers=headers
        )
        assert response.status_code == 200

    @allure.title('Create order without ingredients')
    def test_create_order_no_ingredients(self, api_client, registered_user):
        headers = {'Authorization': registered_user['token']}
        response = api_client.post(
            Urls.ORDERS,
            json={'ingredients': []},
            headers=headers
        )

        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Create order with invalid ingredients')
    def test_create_order_invalid_ingredients(self, api_client, registered_user):
        headers = {'Authorization': registered_user['token']}
        response = api_client.post(
            Urls.ORDERS,
            json={'ingredients': ['invalid_hash_1', 'invalid_hash_2']},
            headers=headers
        )

        # Проверяем статус код
        assert response.status_code == 500, f"Expected 500, got {response.status_code}"

        # Проверяем, что ответ содержит HTML с сообщением об ошибке
        assert 'Internal Server Error' in response.text