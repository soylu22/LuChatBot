from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import connection
from .utils import RAGService

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
        
        # Save History
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO chat_history (user_email, question, answer) VALUES (%s, %s, %s)",
                [request.user.email, question, answer]
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
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT question, answer, created_at FROM chat_history WHERE user_email = %s ORDER BY created_at ASC",
                [request.user.email]
            )
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response(results)
