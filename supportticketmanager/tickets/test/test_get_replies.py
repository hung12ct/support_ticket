from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import User
from ..models import Ticket, Post


class APIGetPosts(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'testuser', 'test@example.com', 'testpassword')

        self.test_ticket = Ticket.objects.create(
            subject='test subject', owner=self.test_user)
        for i in range(22):
            Post.objects.create(message="test post {}".format(
                i), ticket=self.test_ticket, owner=self.test_user)
        self.get_posts_url = reverse(
            'get_posts', kwargs={'ticket_pk': self.test_ticket.pk})
        self.get_posts_invalid_ticket_id_url = reverse(
            'get_posts', kwargs={'ticket_pk': self.test_ticket.pk + 1})
        Token.objects.create(user=self.test_user)

    def test_get_posts_sucess(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user.auth_token.key)
        response = self.client.get(self.get_posts_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 22)
        self.assertEqual(len(response.data['results']), 10)

    def test_get_posts_with_failed_authen(self):

        response = self.client.get(self.get_posts_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_posts_with_invalid_ticket_id(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.test_user.auth_token.key)
        response = self.client.get(
            self.get_posts_invalid_ticket_id_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
