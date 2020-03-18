from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import NewTicketForm, PostForm
from .models import Ticket, Post
from django.utils import timezone


class TicketListView(ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = 'tickets/tickets.html'
    paginate_by = 10


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'tickets/ticket_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.ticket.pk)
        if not self.request.session.get(session_key, False):
            self.ticket.views += 1
            self.ticket.save()
            self.request.session[session_key] = True
        kwargs['ticket'] = self.ticket
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.ticket = get_object_or_404(
            Ticket, pk=self.kwargs.get('ticket_pk'))
        queryset = self.ticket.posts.order_by('created_at')
        return queryset


@login_required
def new_ticket(request):
    if request.method == 'POST':
        form = NewTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.owner = request.user
            ticket.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                ticket=ticket,
                owner=request.user
            )
            return redirect('ticket_posts', ticket_pk=ticket.pk)
    else:
        form = NewTicketForm()
    return render(request, 'tickets/new_ticket.html', {'form': form})


@login_required
def reply_ticket(request, ticket_pk):
    ticket = get_object_or_404(Ticket, pk=ticket_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.ticket = ticket
            post.owner = request.user
            post.save()
            ticket.last_updated = timezone.now()
            ticket.save()
            ticket_url = reverse('ticket_posts', kwargs={
                                 'ticket_pk': ticket_pk})
            ticket_post_url = '{url}?page={page}#{id}'.format(
                url=ticket_url,
                page=ticket.get_page_count(),
                id=post.pk
            )

            return redirect(ticket_post_url)
    else:
        form = PostForm()
    return render(request, 'tickets/reply_ticket.html', {'ticket': ticket, 'form': form})
