from rest_framework import serializers
from .models import Chat,ChatItem


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"

class ChatItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatItem
        fields = "__all__"