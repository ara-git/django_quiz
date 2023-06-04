from django.shortcuts import render
from .models import Quiz


def quiz_view(request):
    """
    # 質問を DBに登録しているっぽい
    quiz = Quiz()
    quiz.question = "What is the capital of France?"
    quiz.options = ["Paris", "London", "Berlin", "Madrid"]
    quiz.answer = "Paris"
    quiz.save()
    """

    # DBのすべてを呼び出している？
    quizzes = Quiz.objects.all().values()

    # パラメータを設定
    params = {"quizzes": quizzes, "title": "Hello"}
    return render(request, "quiz.html", params)
