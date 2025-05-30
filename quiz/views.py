from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from .serializers import QuestionSerializer,FormSerializer,ResponseSerializer,FormResponseSerializer
from django.db import transaction
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
        if data.get('form_code') is None or data.get('responses') is None:
            return Response({
                "status": False,
                "message": "Form code and responses are required!",
                "data" : {}
            })
        with transaction.atomic():
            responses = data.get('responses')
            response_obj = models.Response.objects.create(
                form=models.Form.objects.get(code=code)
            )
            
            for response in responses:
                question = models.Question.objects.filter(id=response['question_id']).first()
                if question.question_type == 'checkbox':
                    for ans in response['answers']:
                        answer_obj = models.ResponseAnswer.objects.create(
                            answer_to=question,
                            answer=models.Choices.objects.get(id=ans).choice
                        )
                        response_obj.responses.add(answer_obj)
                else:
                    answer_obj = models.ResponseAnswer.objects.create(
                        answer_to=question,
                        answer= models.Choices.objects.get(id=response['answers'][0])
                        )
                    response_obj.responses.add(answer_obj)
            
            return Response({
                "status": True,
                "message": "Response stored successfully!",
                "data": data
            })
        return Response({
                "status": False,
                "message": "Something went wrong!",
                "data" : {}
            })
        
class FromResponseAPI(APIView):
    def get(self, request, code):
        queryset = models.Form.objects.filter(code=code).first()
        serializer = FormResponseSerializer(queryset)
        return Response({
            "status": True,
            "message": "Hello, this is the Form Response View!",
            "data": serializer.data
        })