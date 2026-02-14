from django.db import models
from django.contrib.auth.models import User
from pgvector.django import VectorField

class KnowledgeBase(models.Model):
    content = models.TextField()
    metadata = models.JSONField(null=True, blank=True)
    embedding = VectorField(dimensions=3072)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_history')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.email}: {self.question[:30]}..."
