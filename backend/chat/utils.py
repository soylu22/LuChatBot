import os
import psycopg2
from django.db import connection
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from typing import List, Dict

# Configure Gemini
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

class RAGService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len
        )
        self.embedding_model = "models/text-embedding-004"
        self.llm_model = genai.GenerativeModel("gemini-1.5-flash")

    def ingest_text(self, text: str, metadata: dict = None):
        chunks = self.text_splitter.split_text(text)
        embeddings_result = genai.embed_content(
            model=self.embedding_model,
            content=chunks,
            task_type="RETRIEVAL_DOCUMENT"
        )
        embeddings = embeddings_result['embedding']
        
        with connection.cursor() as cursor:
            for content, embedding in zip(chunks, embeddings):
                # Using raw SQL because pgvector isn't easily handled by default Django ORM 
                # without extra packages like django-pgvector
                cursor.execute(
                    "INSERT INTO knowledge_base (content, embedding, metadata) VALUES (%s, %s, %s)",
                    [content, embedding, str(metadata) if metadata else None]
                )

    def get_response(self, question: str) -> str:
        # 1. Get embedding for the query
        query_embedding_result = genai.embed_content(
            model=self.embedding_model,
            content=question,
            task_type="RETRIEVAL_QUERY"
        )
        query_embedding = query_embedding_result['embedding']

        # 2. Retrieve Top 3 from Postgres
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT content FROM knowledge_base ORDER BY embedding <=> %s::vector LIMIT 3",
                [query_embedding]
            )
            rows = cursor.fetchall()
            context = [row[0] for row in rows]

        if not context:
            return "No relevant information found."

        # 3. Generate Answer
        context_str = "\n".join([f"- {c}" for c in context])
        prompt = f"""
        You are "LU", a helpful chatbot.
        Answer the question based ONLY on the context. 
        CONTEXT: {context_str}
        QUESTION: {question}
        """
        response = self.llm_model.generate_content(prompt)
        return response.text
