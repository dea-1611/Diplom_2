import requests


class APIClient:
    def __init__(self):
        self.session = requests.Session()

    def post(self, url, json=None, headers=None):
        return self.session.post(url, json=json, headers=headers)

    def get(self, url, headers=None):
        return self.session.get(url, headers=headers)

    def delete(self, url, headers=None):
        return self.session.delete(url, headers=headers)