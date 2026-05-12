from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Paragraph


class ParagraphCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        text = request.data.get('text')

        if not text:

            return Response(
                {"error": "Text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        paragraphs = text.split('\n\n')

        created_paragraphs = []

        for para in paragraphs:

            para = para.strip()

            if para:

                paragraph = Paragraph.objects.create(
                    user=request.user,
                    content=para
                )

                created_paragraphs.append(paragraph.content)

        return Response(
            {
                "message": "Paragraphs stored successfully",
                "paragraphs": created_paragraphs
            },
            status=status.HTTP_201_CREATED
        )


class SearchWordView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        word = request.GET.get('word')

        if not word:

            return Response(
                {"error": "Word parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        paragraphs = Paragraph.objects.filter(
            user=request.user
        )

        result = []

        for para in paragraphs:

            words = para.content.lower().split()

            count = words.count(word.lower())

            if count > 0:

                result.append({
                    "paragraph": para.content,
                    "count": count
                })

        result = sorted(
            result,
            key=lambda x: x['count'],
            reverse=True
        )

        top_10 = result[:10]

        return Response(top_10)

# Create your views here.
