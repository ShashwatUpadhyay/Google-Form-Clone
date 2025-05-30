from django.db import models
from .choices import QUESTION_CHIOCES
from django.contrib.auth.models import User
from .utlis import generate_random_string
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Choices(BaseModel):
    choice = models.CharField(max_length=100)

    def __str__(self):
        return self.choice

class Question(BaseModel):
    question = models.CharField(max_length=255)
    question_type = models.CharField(max_length=100, choices=QUESTION_CHIOCES)
    required = models.BooleanField(default=True)
    choices = models.ManyToManyField(Choices, related_name='questions', blank=True)
    
    def __str__(self):
        return self.question
    
class Form(BaseModel):
    code = models.CharField(max_length=100, unique=True, blank=True)
    title = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question, related_name='forms', blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms_created')
    background_color = models.CharField(max_length=100, default=' #ff9933')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_string(20)
        super(Form,self).save(*args, **kwargs)

class ResponseAnswer(BaseModel):
    answer_to = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.TextField()  # Store the answer as text

    def __str__(self):
        return f"{self.answer_to.question}-{self.answer}"

class Response(BaseModel):
    code = models.CharField(max_length=100, unique=True, blank=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    responder_email = models.EmailField(null=True, blank=True)
    responses = models.ManyToManyField(ResponseAnswer, related_name='responses', blank=True)
    
    def __str__(self):  
        return self.code
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_string(20)
        super(Response,self).save(*args, **kwargs)