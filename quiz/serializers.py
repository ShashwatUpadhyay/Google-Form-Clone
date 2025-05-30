from rest_framework import serializers
from .models import Question, Choices, Form, Response

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