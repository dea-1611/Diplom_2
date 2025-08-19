import time
import random
from faker import Faker
from helpers.urls import Urls

fake = Faker()
fake_ru = Faker('ru_RU')

def generate_email():
    timestamp = int(time.time() * 1000)
    random_num = random.randint(1000, 9999)
    return f"test_{timestamp}_{random_num}@example.com"

def generate_password():
    return fake.password(length=10, special_chars=True, digits=True)

def generate_name():
    return fake_ru.name()

def get_valid_ingredients(api_client):
    response = api_client.get(Urls.INGREDIENTS)
    response.raise_for_status()
    data = response.json()
    assert 'data' in data, "Unexpected response structure"
    return [ingredient['_id'] for ingredient in data['data']][:2]