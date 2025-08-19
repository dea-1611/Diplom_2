import requests
import allure

class BaseAPI:
    def __init__(self):
        self.session = requests.Session()

    @allure.step("Отправка POST запроса на {url}")
    def post(self, url, json=None, headers=None):
        allure.attach(
            f"URL: {url}\nHeaders: {headers}\nBody: {json}",
            name="Детали POST запроса",
            attachment_type=allure.attachment_type.TEXT
        )
        response = self.session.post(url, json=json, headers=headers)
        allure.attach(
            f"Status Code: {response.status_code}\nResponse: {response.text}",
            name="Детали POST ответа",
            attachment_type=allure.attachment_type.TEXT
        )
        return response

    @allure.step("Отправка GET запроса на {url}")
    def get(self, url, headers=None):
        allure.attach(
            f"URL: {url}\nHeaders: {headers}",
            name="Детали GET запроса",
            attachment_type=allure.attachment_type.TEXT
        )
        response = self.session.get(url, headers=headers)
        allure.attach(
            f"Status Code: {response.status_code}\nResponse: {response.text}",
            name="Детали GET ответа",
            attachment_type=allure.attachment_type.TEXT
        )
        return response

    @allure.step("Отправка DELETE запроса на {url}")
    def delete(self, url, headers=None):
        allure.attach(
            f"URL: {url}\nHeaders: {headers}",
            name="Детали DELETE запроса",
            attachment_type=allure.attachment_type.TEXT
        )
        response = self.session.delete(url, headers=headers)
        allure.attach(
            f"Status Code: {response.status_code}\nResponse: {response.text}",
            name="Детали DELETE ответа",
            attachment_type=allure.attachment_type.TEXT
        )
        return response