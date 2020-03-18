from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from .models import Ticket, Post
from .serializers import TicketSerializer, PostSerializer
from .pagination import PaginationHandlerMixin


class BasicPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class NewTicket(APIView):

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_customer_service:
                res = {
                    "error": "You are not allowed to create a ticket. Please contact administrators for help."
                }
                return Response(res, status=status.HTTP_403_FORBIDDEN)
            message = serializer.data['message']
            subject = serializer.data['subject']
            ticket = Ticket.objects.create(subject=subject, owner=user)
            Post.objects.create(
                message=message, ticket=ticket, owner=user)
            res = {
                "id": ticket.id,
                "subject": ticket.subject,
            }
            return Response(res, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyTicket(APIView):

    def post(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            message = serializer.data['message']
            post = Post.objects.create(
                message=message, ticket=ticket, owner=user)
            ticket.last_updated = timezone.now()
            ticket.save()
            res = {
                "id": post.id,
                "status": "Success",
            }
            return Response(res, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteReply(APIView):

    def delete(self, request, reply_pk):
        post = get_object_or_404(Post, pk=reply_pk)
        if post.owner == request.user and post != Ticket.objects.get(id=post.ticket.id).posts.first():
            post.delete()
            return Response("Post deleted", status=status.HTTP_204_NO_CONTENT)
        res = {
            "error": "You are not allowed to delete to this post. Please contact administrators for help."
        }
        return Response(res, status=status.HTTP_403_FORBIDDEN)


class GetPost(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request, ticket_pk):
        ticket = get_object_or_404(Ticket, pk=ticket_pk)
        posts = ticket.posts.get_queryset().order_by('created_at')
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_paginated_response(PostSerializer(page,
                                                                    many=True).data)
        else:
            serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
