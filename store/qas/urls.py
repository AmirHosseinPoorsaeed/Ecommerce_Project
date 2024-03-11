from django.urls import path

from . import views

app_name = 'qas'

urlpatterns = [
    path('create/question/<int:product_id>/', views.QuestionCreateView.as_view(), name='question_create'),
    path('create/answer/<int:question_id>/', views.AnswerCreateView.as_view(), name='answer_create'),
]
