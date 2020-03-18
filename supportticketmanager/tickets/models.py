import math
from django.db import models
from django.utils.text import Truncator
from django.conf import settings
from django.utils.html import mark_safe
from markdown import markdown

User = settings.AUTH_USER_MODEL


class Ticket(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='tickets')
    views = models.PositiveIntegerField(default=0)
    objects = models.Manager()

    class Meta:
        ordering = ('-last_updated', )

    def __str__(self):
        return self.subject

    def get_last_ten_posts(self):
        return self.posts.order_by('-created_at')[:10]

    def get_replies_count(self):
        return self.posts.count() - 1

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 10
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 5

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)


class Post(models.Model):
    message = models.TextField(max_length=4000)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE,
                               related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='posts')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                   related_name='+')
    objects = models.Manager()

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))


