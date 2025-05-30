from rest_framework import serializers
from .models import Question, Choices, Form, Response,ResponseAnswer

class ChoucesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choices
        exclude = ['updated_at', 'created_at','id']


class QuestionSerializer(serializers.ModelSerializer):
    choice = ChoucesSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        exclude = ['updated_at', 'created_at']
        # fields = '__all__'

class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        exclude = ['updated_at', 'created_at', 'creator', 'id']
        # fields = '__all__'
        
    def to_representation(self, instance):
        questions = []
        for question in instance.questions.all():
            choices = None
            if question.question_type in ['checkbox', 'multiple choice']:
                choices = [{'id':choice.id,'choice':choice.choice} for choice in question.choices.all()]
            
            
            questions.append({
                'id': question.id,
                'question': question.question,
                'question_type': question.question_type,
                'required': question.required,
                'choices': choices,
            })
            
        data = {
            'code': instance.code,
            'title': instance.title,
            'background_color': instance.background_color,
            'questions': questions,
        }
        return data

class ResponseAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseAnswer
        exclude = ['updated_at', 'created_at']
    
    def to_representation(self, instance):
        data = {
            'answer': instance.answer,
            'answer_to':{
                'question': instance.answer_to.question,
                'question_type': instance.answer_to.question_type,
                },
        }
        return data
    
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        exclude = ['updated_at', 'created_at']
    
    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'code': instance.code,
            'form_code': instance.form.code,
            'responder_email': instance.responder_email,
            'form': {
                'code': instance.form.code,
                'title': instance.form.title,
                'background_color': instance.form.background_color,
            },
            'responses': ResponseAnswerSerializer(instance.responses.all(), many=True).data,
        }
        return data

class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ['id']
    
    def to_representation(self, instance):
        queryset = Response.objects.filter(form=instance)
        data = {
            'id': instance.id,
            'code': instance.code,
            'title': instance.title,
            'background_color': instance.background_color,
            'responses': ResponseSerializer(queryset, many=True).data,
        }
        return data