from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import User
from ..models import Ticket, Post


class APIReplyTicket(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'ticketowner', 'ticketowner@example.com', 'testpassword')
        self.test_ticket = Ticket.objects.create(
            subject='test subject', owner=self.test_user)
        self.reply_ticket_url = reverse(
            'reply_ticket', kwargs={'ticket_pk': self.test_ticket.pk})
        self.reply_invalid_ticket_id_url = reverse(
            'reply_ticket', kwargs={'ticket_pk': self.test_ticket.pk + 1})
        Token.objects.create(user=self.test_user)

    def test_create_reply_ticket_from_ticket_owner_sucess(self):
        data = {
            "message": "test reply"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user .auth_token.key)
        response = self.client.post(self.reply_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reply_ticket_with_failed_authen(self):
        data = {
            "subject": "test subject"
        }

        response = self.client.post(self.reply_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reply_ticke_with_no_message(self):
        data = {
            "message": ""
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user .auth_token.key)
        response = self.client.post(self.reply_ticket_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_reply_with_invalid_ticket_id_url(self):
        data = {
            "message": "test reply"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user .auth_token.key)
        response = self.client.post(
            self.reply_invalid_ticket_id_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
