from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from accounts.models import User
from ..models import Ticket, Post


class APIDeleteReply(APITestCase):
    def setUp(self):
        self.owner_user = User.objects.create_user(
            'owneruser', 'owneruser@example.com', 'testpassword')
        self.non_user_owner = User.objects.create_user(
            'nonuserowner', 'nonuserowner@example.com', 'testpassword')
        self.test_ticket = Ticket.objects.create(
            subject='test subject', owner=self.owner_user)
        self.first_post = Post.objects.create(
            message="test post", ticket=self.test_ticket, owner=self.owner_user)
        self.first_reply = Post.objects.create(
            message="test reply", ticket=self.test_ticket, owner=self.owner_user)
        self.delete_first_reply_url = reverse(
            'delete_reply', kwargs={'reply_pk': self.first_reply.pk})
        self.delete_first_post_url = reverse(
            'delete_reply', kwargs={'reply_pk': self.first_post.pk})
        self.delete_invalid_post_id_url = reverse(
            'delete_reply', kwargs={'reply_pk': self.first_reply.pk + 1})
        Token.objects.create(user=self.owner_user)
        Token.objects.create(user=self.non_user_owner)

    def test_delete_reply_from_reply_owner_sucess(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.owner_user.auth_token.key)
        response = self.client.delete(self.delete_first_reply_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_ticket.posts.count(), 1)

    def test_delete_reply_from_non_user_owner(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.non_user_owner.auth_token.key)
        response = self.client.delete(self.delete_first_reply_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_first_post(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.owner_user.auth_token.key)
        response = self.client.delete(self.delete_first_post_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_with_failed_authen(self):

        response = self.client.delete(self.delete_first_post_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_reply_with_delete_invalid_post_id_url(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                self.owner_user.auth_token.key)
        response = self.client.delete(self.delete_invalid_post_id_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
