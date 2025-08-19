import allure
from helpers.data_generator import get_valid_ingredients
from helpers.urls import Urls


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Создание заказа с авторизацией и валидными ингредиентами')
    def test_create_order_auth_valid_ingredients(self, api_client, registered_user):
        with allure.step('Получение валидных ингредиентов'):
            ingredients = get_valid_ingredients(api_client)

        with allure.step('Подготовка заголовков с токеном авторизации'):
            headers = {'Authorization': registered_user['token']}

        with allure.step('Отправка запроса на создание заказа'):
            response = api_client.post(
                Urls.ORDERS,
                json={'ingredients': ingredients},
                headers=headers
            )

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 200

        with allure.step('Проверка структуры ответа'):
            response_data = response.json()
            assert response_data['success'] is True
            assert 'name' in response_data
            assert 'order' in response_data
            assert 'number' in response_data['order']

            allure.attach(
                f"Ответ сервера: {response_data}",
                name="Детали ответа",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title('Создание заказа без авторизации')
    def test_create_order_no_auth(self, api_client):
        with allure.step('Получение валидных ингредиентов'):
            ingredients = get_valid_ingredients(api_client)

        with allure.step('Отправка запроса на создание заказа без авторизации'):
            response = api_client.post(Urls.ORDERS, json={'ingredients': ingredients})

        with allure.step('Проверка, что заказ не создается без авторизации'):
            # Согласно документации, только авторизованные пользователи могут сделать заказ.
            # Если API позволяет создавать заказы без авторизации - это нарушение требований.
            # Соответственно, тест должен получить статус failed, если заказ создается без авторизации.
            assert response.status_code != 200, "Заказы не должны создаваться без авторизации"
            assert response.status_code == 401, f"Ожидался код 401 Unauthorized, получен {response.status_code}"
            assert response.json()['success'] is False
            assert response.json()['message'] == 'You should be authorised'

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_no_ingredients(self, api_client, registered_user):
        with allure.step('Подготовка заголовков с токеном авторизации'):
            headers = {'Authorization': registered_user['token']}

        with allure.step('Отправка запроса на создание заказа без ингредиентов'):
            response = api_client.post(
                Urls.ORDERS,
                json={'ingredients': []},
                headers=headers
            )

        with allure.step('Проверка ошибки отсутствия ингредиентов'):
            assert response.status_code == 400
            assert response.json()['success'] is False
            assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание заказа с невалидными ингредиентами')
    def test_create_order_invalid_ingredients(self, api_client, registered_user):
        with allure.step('Подготовка заголовков с токеном авторизации'):
            headers = {'Authorization': registered_user['token']}

        with allure.step('Отправка запроса с невалидными ингредиентами'):
            response = api_client.post(
                Urls.ORDERS,
                json={'ingredients': ['invalid_hash_1', 'invalid_hash_2']},
                headers=headers
            )

        with allure.step('Проверка ошибки сервера'):
            assert response.status_code == 500
            assert 'Internal Server Error' in response.text