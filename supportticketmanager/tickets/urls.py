from django.urls import path
from . import views, apitickets


urlpatterns = [
    path('', views.TicketListView.as_view(), name='tickets'),
    path('tickets/<int:ticket_pk>/',
         views.PostListView.as_view(), name='ticket_posts'),
    path('tickets/new/', views.new_ticket, name='view_new_ticket'),
    path('tickets/<int:ticket_pk>/reply/', views.reply_ticket,
         name='view_reply_ticket'),
    path('api/newticket/', apitickets.NewTicket.as_view(), name='new_ticket'),
    path('api/tickets/<int:ticket_pk>/reply/',
         apitickets.ReplyTicket.as_view(), name='reply_ticket'),
    path('api/tickets/<int:ticket_pk>/posts/',
         apitickets.GetPost.as_view(), name='get_posts'),
    path('api/posts/<int:reply_pk>/',
         apitickets.DeleteReply.as_view(), name='delete_reply'),
]
