import unittest
import requests


class ApiTest(unittest.TestCase):

    def setUpClass(cls) -> None:
        cls.url = 'https://interview.doraclp.cn'
        return super().setUpClass()

    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    # login
    def test_login(self):
        path = '/login'
        data = {
            "email": "admin@example.com",
            "password": "password"
        }

        # send request
        r = requests.post(url=self.url+path, json=data)
        # get token
        self.token = r.json()["tokens"]
        # request assert
        self.assertEqual(r.status_code, 200)
        # data assert
        self.assertEqual(r.json()["user"]["email"], data["email"])

    # register
    def test_register(self):
        path = '/register'
        data = {
            "email": "admin@example.com",
            "password": "password",
            "firstName": "John",
            "lastName": "Smith"
        }

        # send request
        r = requests.post(url=self.url+path, json=data)
        # status code assert
        self.assertEqual(r.status_code, 200)
        # body assert
        self.assertEqual(r.json()["user"]["email"], data["email"])
