from faker import Faker
from helpers.urls import Urls

fake = Faker()
fake_ru = Faker('ru_RU')

def generate_email():
    return fake.email()

def generate_password():
    return fake.password(length=10, special_chars=True, digits=True)

def generate_name():
    return fake_ru.name()

def get_valid_ingredients(api_client):
    response = api_client.get(Urls.INGREDIENTS)
    response.raise_for_status()
    return [ingredient['_id'] for ingredient in response.json()['data']][:2]