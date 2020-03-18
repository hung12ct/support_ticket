from django.test import TestCase
from django.urls import resolve, reverse

from accounts.models import User
from ..models import Ticket
from ..views import TicketListView


class TicketsTests(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='test', email='john@example.com', password='123')
        self.ticket = Ticket.objects.create(subject='test subject', owner=test_user)
        url = reverse('tickets')
        self.response = self.client.get(url)

    def test_tickets_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_tickets_url_resolves_tickets_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, TicketListView)

    def test_tickets_view_contains_link_to_posts_page(self):
        ticket_posts_url = reverse('ticket_posts', kwargs={'ticket_pk': self.ticket.pk})
        self.assertContains(self.response, 'href="{0}"'.format(ticket_posts_url))