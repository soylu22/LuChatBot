from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .utils import RAGService
from .models import ChatHistory

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name', '')
        
        if User.objects.filter(username=email).exists():
            return Response({"error": "User already exists"}, status=400)
            
        user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name)
        return Response({"msg": "User created successfully"})

class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        question = request.data.get('question')
        rag = RAGService()
        answer = rag.get_response(question)
        
        # Save History using Django ORM
        ChatHistory.objects.create(
            user=request.user,
            question=question,
            answer=answer
        )
            
        return Response({"response": answer})

class IngestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        content = request.data.get('content')
        rag = RAGService()
        rag.ingest_text(content)
        return Response({"status": "success"})

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get chat history using Django ORM
        history = ChatHistory.objects.filter(user=request.user).values(
            'question', 'answer', 'created_at'
        )
        return Response(list(history))
