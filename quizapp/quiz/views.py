from django.shortcuts import render
from django.http import HttpResponse
from .models import Quiz
from .forms import HelloForm


def quiz_top(request):
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

    # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
    params = {"quizzes": quizzes, "title": "Hello", "goto": "next", "form": HelloForm()}

    if request.method == "POST":
        params["message"] = (
            "名前："
            + request.POST["name"]
            + "<br>メール："
            + request.POST["mail"]
            + "<br>年齢："
            + request.POST["age"]
        )
    return render(request, "quiz.html", params)


def quiz_individual(request):
    # html上の変数"goto"には"quiz"を当てはめる
    params = {"title": "Hello/Next", "msg": "これは、もう一つのページです。", "goto": "quiz"}
    return render(request, "quiz.html", params)
