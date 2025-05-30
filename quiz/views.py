from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import QuestionSerializer,FormSerializer
    # Create your views here.

class QuestionAPI(APIView):
    def get(self, request):
        queryset = models.Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        return Response({
            "status":True,
            "message": "Hello, this is the Question View!",
            "data": serializer.data
            })
        
class FormAPI(APIView):
    def get(self, request, code):
        queryset = models.Form.objects.filter(code=code).first()        
        serializer = FormSerializer(queryset)
        return Response({   
            "status":True,
            "message": "Hello, this is the Form View!",
            "data": serializer.data
        })

class StoreResponseAPI(APIView):
    def post(self, request, code):
        data = request.data
        return Response({
            "status": True,
            "message": "Response stored successfully!",
            "data": data
        })