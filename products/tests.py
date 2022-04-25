from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Order, Product

User = get_user_model()


class TestProductViewsets(APITestCase):
    def setUp(self):
        self.user = baker.make(User, username="testuser", email="testuser@test.com")
        self.products = baker.make(Product, _quantity=16)
        for i, v in enumerate(self.products):
            if i == 0:
                v.id = 1
                v.name = "Product 1"
                v.price = Decimal(100.00)
                v.quantity = 10
                v.save()
                break

        self.user.set_password("testpassword")
        self.user.save()

    def test_accept_unauthenticated_access_list(self):
        url = reverse("products:products-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_access_list(self):
        self.client.force_authenticate(self.user)
        url = reverse("products:products-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_list_results_list(self):
        self.client.force_authenticate(self.user)
        url = reverse("products:products-list")
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

    def test_accept_unauthenticated_access_detail(self):
        url = reverse("products:products-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_access_detail(self):
        self.client.force_authenticate(self.user)
        url = reverse("products:products-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_detail_result(self):
        self.client.force_authenticate(self.user)
        url = reverse("products:products-detail", args=[1])
        response = self.client.get(url)
        response_data = response.json()

        # Test if the response contains the correct data format
        self.assertIn("id", response_data)
        self.assertIn("name", response_data)
        self.assertIn("price", response_data)
        self.assertIn("quantity", response_data)

        # Checks if the number of orders in results in first page is equal
        # to the count of the results and equal
        # to the number of orders in the database
        self.assertEqual(response_data["id"], 1)
        self.assertEqual(Decimal(response_data["price"]), Decimal(100.00))
        self.assertEqual(response_data["name"], "Product 1")
        self.assertEqual(response_data["quantity"], 10)


class TestOrderViewset(APITestCase):
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
        self.user.set_password("testpassword")
        self.user.save()
        for i, v in enumerate(self.order):
            if i == 0:
                v.id = 1
                v.order_id = "cc23f040-1970-4ccf-8998-be0ebcf50c1e"
                v.save()
                break

    def test_reject_unauthenticated_access_list(self):
        url = reverse("products:orders-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access_list(self):
        self.client.force_authenticate(self.user)
        url = reverse("products:orders-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_list_results_list(self):
        self.client.force_authenticate(self.user)
        url = reverse("products:orders-list")
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

    def test_unauthenticated_access_detail(self):
        url = reverse(
            "products:orders-detail", args=["cc23f040-1970-4ccf-8998-be0ebcf50c1e"]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access_detail(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            "products:orders-detail", args=["cc23f040-1970-4ccf-8998-be0ebcf50c1e"]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_detail_result(self):
        self.client.force_authenticate(self.user)
        url = reverse(
            "products:orders-detail", args=["cc23f040-1970-4ccf-8998-be0ebcf50c1e"]
        )
        response = self.client.get(url)
        response_data = response.json()

        # Test if the response contains the correct data format
        self.assertIn("order_id", response_data)
        self.assertIn("customer", response_data)
        self.assertIn("products", response_data)

        # Checks if the number of orders in results in first page is equal
        # to the count of the results and equal
        # to the number of orders in the database
        self.assertEqual(
            response_data["order_id"], "cc23f040-1970-4ccf-8998-be0ebcf50c1e"
        )
