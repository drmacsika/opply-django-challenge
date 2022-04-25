from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from products.models import Order, Product
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestCreateCustomerViewset(APITestCase):
    def setUp(self):
        self.user = baker.make(User, username="testuser", email="testuser@test.com")
        self.user.set_password("testpassword")
        self.user.save()

    def test_reject_create_with_no_data(self):
        url = reverse("customers:users-list")
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_creating_duplicate_username_and_email(self):
        url = reverse("customers:users-list")
        data = {
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "testpassword1",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer(self):
        url = reverse("customers:users-list")
        data = {
            "username": "testuser1",
            "email": "testuser1@gmail.com",
            "password": "testpassword1",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username="testuser").id, 1)
        self.assertEqual(User.objects.get(username="testuser1").id, 2)


class TestTokenObtainPairView(APITestCase):
    def setUp(self):
        self.user = baker.make(User, username="testuser", email="testuser@test.com")
        self.user.set_password("testpassword")
        self.user.save()

    def test_reject_login_with_no_data(self):
        url = reverse("customers:login")
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_login_with_incorrect_data(self):
        url = reverse("customers:login")
        data = {
            "username": "testuser",
            "password": "testpassword1",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_successful_login(self):
        url = reverse("customers:login")
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn("access", response_data)
        self.assertIn("refresh", response_data)
        self.assertNotEqual(response_data["access"], response_data["refresh"])


class TestTokenRefreshView(APITestCase):
    def setUp(self):
        self.user = baker.make(User, username="testuser", email="testuser@test.com")
        self.user.set_password("testpassword")
        self.user.save()

    def test_new_access_token_generation_fromrefresh_token(self):
        url = reverse("customers:login")
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        refresh_url = reverse("customers:refresh")

        # Reject Generating new access token from access token
        access_response = self.client.post(
            refresh_url, {"refresh": response_data["access"]}
        )
        self.assertEqual(access_response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Accept Generating new access token from refresh token
        refresh_response1 = self.client.post(
            refresh_url, {"refresh": response_data["refresh"]}
        )
        self.assertEqual(refresh_response1.status_code, status.HTTP_200_OK)


class TestCustomerOrderHistoryViewset(APITestCase):
    def setUp(self):
        self.user = baker.make(User, username="testuser", email="testuser@test.com")
        self.products_set = baker.prepare(Product, _quantity=16)
        self.order = baker.make(
            Order,
            customer=self.user,
            products=self.products_set,
            make_m2m=True,
            _quantity=16,
        )
        self.user.save()

    def test_reject_unauthenticated_access(self):
        url = reverse("customers:customers-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access(self):
        self.client.force_authenticate(self.user)
        url = reverse("customers:customers-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_list_results(self):
        self.client.force_authenticate(self.user)
        url = reverse("customers:customers-list")
        response = self.client.get(url)
        response_data = response.json()

        # Test if the response contains the correct data format
        self.assertIn("results", response_data)
        self.assertIn("next", response_data)
        self.assertIn("previous", response_data)
        self.assertIn("count", response_data)

        # Checks if the number of orders in results in first page is equal
        # to the count of the results and equal
        # to the number of orders in the database
        self.assertEqual(len(response_data["results"]), 10)
        self.assertEqual(response_data["count"], 16)

        # Checks that the previous link is none since this is the first page
        self.assertEqual(response_data["previous"], None)

        # Checks that the next link is has a value since this is the first page
        self.assertNotEqual(response_data["next"], None)

        # Checks that the next link is accessible
        next_response = self.client.get(response_data["next"])
        self.assertEqual(next_response.status_code, status.HTTP_200_OK)
        next_response_data = next_response.json()

        # Checks the number of orders in the next page
        # is equal to the number of orders in the database
        self.assertEqual(len(next_response_data["results"]), 6)
        self.assertEqual(next_response_data["count"], 16)

        # checks that the previous link has a value
        # since this is the next page
        self.assertNotEqual(next_response_data["previous"], None)

        # checks that the next link has no value
        # since this is the last page
        self.assertEqual(next_response_data["next"], None)
