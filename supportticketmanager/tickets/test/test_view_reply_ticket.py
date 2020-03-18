from accounts.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import PostForm
from ..models import Ticket, Post
from ..views import reply_ticket


class ReplyTicketTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = '123'
        test_user = User.objects.create_user(
            username=self.username, email='test@example.com', password=self.password)
        self.ticket = Ticket.objects.create(
            subject='Test subject', owner=test_user)
        Post.objects.create(message='Test message',
                            ticket=self.ticket, owner=test_user)
        self.url = reverse('view_reply_ticket', kwargs={'ticket_pk': self.ticket.pk})


class LoginRequiredReplyticketTests(ReplyTicketTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(
            login_url=login_url, url=self.url))


class ReplyticketTests(ReplyTicketTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/tickets/1/reply/')
        self.assertEquals(view.func, reply_ticket)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyticketTests(ReplyTicketTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(
            self.url, {'message': 'Test message 2'})

    def test_redirection(self):
        url = reverse('ticket_posts', kwargs={'ticket_pk': self.ticket.pk})
        ticket_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, ticket_posts_url)

    def test_reply_created(self):
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyticketTests(ReplyTicketTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
