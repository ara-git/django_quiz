from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Quiz
from .forms import HelloForm


class quiz_top(TemplateView):
    def __init__(self):
        # DBのすべてを呼び出している？
        quizzes = Quiz.objects.all().values()

        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
            "quizzes": quizzes,
            "title": "Hello",
            "message": "名前を入力してね（Inital Massage）",
            "goto": "next",
            "form": HelloForm(),
        }

    def get(self, request):
        """
        get時（普通にアクセスしたとき）の挙動を定義
        """
        return render(request, "quiz.html", self.params)

    def post(self, request):
        """
        post時（ユーザーからの入力を受けたとき）の挙動を定義
        """
        self.params["message"] = (
            "名前："
            + request.POST["name"]
            + "<br>メール："
            + request.POST["mail"]
            + "<br>年齢："
            + request.POST["age"]
        )
        self.params["form"] = HelloForm(request.POST)
        return render(request, "quiz.html", self.params)


def quiz_individual(request):
    # html上の変数"goto"には"quiz"を当てはめる
    params = {"title": "Hello/Next", "message": "これは、もう一つのページです。", "goto": "quiz"}
    return render(request, "quiz.html", params)
