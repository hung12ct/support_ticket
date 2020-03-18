from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import User


class APICreateTicket(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'testuser', 'test@example.com', 'testpassword')
        self.customer_service_user = User.objects.create_user(
            'customerservice', 'customersv@example.com', 'testpassword')
        self.customer_service_user.is_customer_service = True
        self.customer_service_user.save()
        self.new_ticket_url = reverse('new_ticket')
        Token.objects.create(user=self.test_user)
        Token.objects.create(user=self.customer_service_user)

    def test_create_new_ticket_sucess(self):
        data = {
            "subject": "test subject",
            "message": "test message"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['subject'], data['subject'])

    def test_create_new_ticket_with_failed_authen(self):
        data = {
            "subject": "test subject",
            "message": "test message"
        }

        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new_ticket_from_customer_service(self):
        data = {
            "subject": "test subject",
            "message": "test message"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.customer_service_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_ticket_with_no_subject(self):
        data = {
            "subject": "",
            "message": "test message"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_new_ticket_with_no_message(self):
        data = {
            "subject": "test subject",
            "message": ""
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user.auth_token.key)
        response = self.client.post(self.new_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
