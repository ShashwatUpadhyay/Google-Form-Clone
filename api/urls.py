from django.urls import path
from quiz.views import QuestionAPI,FormAPI,StoreResponseAPI,StoreResponseAPI,FromResponseAPI

urlpatterns = [
    path('questions/', QuestionAPI.as_view()),
    path('form/<code>/', FormAPI.as_view()),
    path('store-response/<code>/', StoreResponseAPI.as_view()),
    path('form/response/<code>/', FromResponseAPI.as_view()),
]