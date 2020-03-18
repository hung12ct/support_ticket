from accounts.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from accounts.models import User
from ..models import Ticket, Post
from ..views import PostListView


class TicketPostsTests(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='test', email='john@example.com', password='123')
        ticket = Ticket.objects.create(subject='test subject', owner=test_user)
        Post.objects.create(message='test message', ticket=ticket, owner=test_user)
        url = reverse('ticket_posts', kwargs={'ticket_pk': ticket.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/tickets/1/')
        self.assertEquals(view.func.view_class, PostListView)