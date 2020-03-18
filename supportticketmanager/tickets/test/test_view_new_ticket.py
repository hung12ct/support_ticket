from accounts.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import NewTicketForm
from ..models import Ticket, Post
from ..views import new_ticket


class NewTicketTests(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='test', email='test@example.com', password='123')
        self.client.login(username='test', password='123')

    def test_new_ticket_view_success_status_code(self):
        url = reverse('view_new_ticket')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_ticket_url_resolves_new_ticket_view(self):
        view = resolve('/tickets/new/')
        self.assertEquals(view.func, new_ticket)

    def test_new_ticket_view_contains_link_back_to_tickets_view(self):
        new_ticket_url = reverse('view_new_ticket')
        tickets_url = reverse('tickets')
        response = self.client.get(new_ticket_url)
        self.assertContains(response, 'href="{0}"'.format(tickets_url))

    def test_csrf(self):
        url = reverse('view_new_ticket')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('view_new_ticket')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTicketForm)

    def test_new_ticket_valid_post_data(self):
        url = reverse('view_new_ticket')
        data = {
            'subject': 'Test subject',
            'message': 'Test message'
        }
        self.client.post(url, data)
        self.assertTrue(Ticket.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_ticket_invalid_post_data(self):
        url = reverse('view_new_ticket')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_ticket_invalid_post_data_empty_fields(self):
        url = reverse('view_new_ticket')
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Ticket.objects.exists())
        self.assertFalse(Post.objects.exists())


class LoginRequiredNewticketTests(TestCase):
    def setUp(self):
        self.url = reverse('view_new_ticket')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(
            login_url=login_url, url=self.url))
