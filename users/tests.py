from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


# Create your tests here.
class UsersTestCase(APITestCase):
    """Тестирование привычек"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@sky.pro")
        self.user.set_password("admin")
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """Тест создания пользователя"""
        url = reverse("users:register")
        data = {
            "email": "helen597@mail.ru",
            "password": "59hl71ee"
        }
        response = self.client.post(url, data=data)
        print("\ntest_user_create")
        print(response.json())
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)