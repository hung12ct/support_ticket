from rest_framework import serializers


class TicketSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255, allow_blank=False)
    message = serializers.CharField(max_length=4000, allow_blank=False, style={
                                    'base_template': 'textarea.html'})


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='owner.username', read_only=True)
    message = serializers.CharField(max_length=4000, allow_blank=False, style={
                                    'base_template': 'textarea.html'})
    created_at = serializers.DateTimeField(read_only=True)

