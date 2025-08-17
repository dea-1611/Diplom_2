import allure
import pytest
from helpers.api_client import APIClient
from helpers.data_generator import get_valid_ingredients
from helpers.urls import Urls


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией и валидными ингредиентами')
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

    @allure.title('Создание заказа без авторизации')
    def test_create_order_no_auth(self, api_client):
        ingredients = get_valid_ingredients(api_client)
        response = api_client.post(Urls.ORDERS, json={'ingredients': ingredients})

        assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
        if response.status_code == 200:
            assert response.json()['success'] is True
        else:
            assert response.json()['message'] == 'You should be authorised'

    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_with_ingredients(self, api_client, registered_user):
        ingredients = get_valid_ingredients(api_client)
        headers = {'Authorization': registered_user['token']}
        response = api_client.post(
            Urls.ORDERS,
            json={'ingredients': ingredients},
            headers=headers
        )
        assert response.status_code == 200

    @allure.title('Создание заказа без ингредиентов')
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

    @allure.title('Создание заказа с неверным  хешем ингредиентов')
    def test_create_order_invalid_ingredients(self, api_client, registered_user):
        headers = {'Authorization': registered_user['token']}
        response = api_client.post(
            Urls.ORDERS,
            json={'ingredients': ['invalid_hash_1', 'invalid_hash_2']},
            headers=headers
        )

        assert response.status_code == 500, f"Expected 500, got {response.status_code}"


        assert 'Internal Server Error' in response.text

