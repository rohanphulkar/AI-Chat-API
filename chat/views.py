from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Chat,ChatItem
from profiles.models import Profile
from .serializers import ChatSerializer,ChatItemSerializer
from datetime import date
import openai
from decouple import config
from django.http import JsonResponse

openai.api_key = config("OPENAI_API_KEY")

class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_id = request.GET.get('chat', None)
        if chat_id:
            try:
                chat = Chat.objects.get(id=chat_id)
            except Chat.DoesNotExist:
                return Response({'error':'chat not found'},status=status.HTTP_404_NOT_FOUND)
            chats = ChatItem.objects.filter(chat=chat)
            serializer = ChatItemSerializer(chats,many=True)
        else:
            chats = Chat.objects.filter(user=request.user)
            serializer = ChatSerializer(chats,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        chat_id = request.GET.get('chat', None)
        profile = Profile.objects.get(user=request.user)

        if profile.plan_validity < date.today():
            return Response({'error':'Your plan has been expired'},status=status.HTTP_400_BAD_REQUEST)
        
        prompt = request.data['prompt']

        if chat_id:
            try:
                chat = Chat.objects.get(id=chat_id)
            except Chat.DoesNotExist:
                return Response({'error':'chat not found'},status=status.HTTP_404_NOT_FOUND)
            previous_items = ChatItem.objects.filter(chat=chat)
            previous_io = '\n'.join(f'User: {item.input}\nAI: {item.output}\n' for item in previous_items)
            inputs = f"{previous_io}\n{prompt}"
        else:
            chat = Chat.objects.create(user=request.user)
            inputs = prompt

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=inputs,
            temperature=0.5,
            max_tokens=2800,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        output = response.choices[0].text
        chat_item = ChatItem.objects.create(chat=chat, input=prompt, output=output)
        if not chat.name:
            chat.name = prompt
            chat.save()
        
        return JsonResponse(output,safe=False)