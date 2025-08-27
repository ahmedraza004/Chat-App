from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import User, ChatRoom, Messages
from .serializers import UserSerializer, ChatRoomSerializer, MessageSerializer, Register
from rest_framework.permissions import IsAuthenticated, AllowAny

# 🔐 User Registration
class RegistrationView(generics.CreateAPIView):
    serializer_class = Register
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 👤 User Info View
class UserView(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    @action(methods=['get'], detail=False, url_path='info')
    def info(self, request):
        try:
            user = self.queryset.get(id=request.user.id)
            user.is_active = True
            user.save()
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_403_FORBIDDEN)

# 💬 Chat Room Management
class ChatView(ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.prefetch_related('participants', 'messages__sender')


    @action(methods=['post'], detail=False, url_path='add_user')
    def add_user(self, request):
        try:
            room = self.queryset.get(name=request.data.get('name'))
            user = User.objects.get(id=request.data.get('user_id'))
            room.participants.add(user)
            room.save()
            room.check_group_status()
            return Response({"message": "User added successfully"})
        except (ChatRoom.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Room or User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='remove_user')
    def remove_user(self, request):
        try:
            room = self.queryset.get(name=request.data.get('name'))
            user = User.objects.get(id=request.data.get('user_id'))
            room.participants.remove(user)
            room.save()
            return Response({"message": "User removed successfully"})
        except (ChatRoom.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Room or User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='private_room')
    def private_room(self, request):
        try:
            room = self.queryset.get(name=request.data.get('name'))
            user1 = User.objects.get(id=request.data.get('user1'))
            user2 = User.objects.get(id=request.data.get('user2'))
            room.participants.add(user1, user2)
            room.save()
            room.check_group_status()
            return Response({"message": "Private room created successfully"})
        except (ChatRoom.DoesNotExist, User.DoesNotExist):
            return Response({"error": "Room or User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='messages')
    def get_messages(self, request, pk=None):
        try:
            room = ChatRoom.objects.get(id=pk)
            messages = room.messages.order_by('timestamp')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='messages')
    def post_message(self, request, pk=None):
        try:
            room = ChatRoom.objects.get(id=pk)
            message = Messages.objects.create(
                room=room,
                sender=request.user,
                message=request.data.get('content')
            )
            serializer = MessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ChatRoom.DoesNotExist:
            return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)


# 📩 Message Handling
class MessageView(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Messages.objects.all()

    def get_queryset(self):
        room_id = self.request.query_params.get('room')
        if room_id:
            return Messages.objects.filter(room_id=room_id).order_by('timestamp')
        return Messages.objects.none()

    @action(detail=False, methods=['post'], url_path='mark-read')
    def mark_as_read(self, request):
        message_ids = request.data.get('message_ids', [])
        Messages.objects.filter(id__in=message_ids).update(is_read=True)
        return Response({"status": "Messages marked as read"}, status=status.HTTP_200_OK)