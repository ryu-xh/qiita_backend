from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestUserModel(TestCase):

    def setUp(self):
        user = User()
        user.handle = 'test'
        user.username = 'test'
        user.set_password('1234')
        user.save()

    def test_authenticate_by_handle(self):
        case1 = self.client.post('/auth/token', data={
            'handle': 'test',
            'password': '1234'
        })
        self.assertEqual(case1.status_code, 200)

        case2 = self.client.post('/auth/token', data={
            'handle': 'test',
            'password': '1235'
        })
        self.assertEqual(case2.status_code, 401)


class TestSignup(TestCase):

    def test_signup_by_handle(self):
        case1 = self.client.post('/auth/signup', data={
            'handle': 'testcase1',
            'password': '1234'
        })
        self.assertEqual(case1.status_code, 200)

        case2 = self.client.post('/auth/signup', data={
            'handle': 'test',
            'password': '1234'
        })
        self.assertEqual(case2.status_code, 400)

