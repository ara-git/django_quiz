from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Quiz
from .forms import Quiz_options
import random


class quiz_top(TemplateView):
    def __init__(self):
        # DBのすべてを呼び出している？
        quizzes = Quiz.objects.all().values()

        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
            "quizzes": quizzes,
            "title": "Hello",
            "message": "↓のボタンから個別クイズに飛べるよ",
            "form": Quiz_options(),
        }

        self.params["goto"] = "quiz_test_mode"

    def get(self, request):
        """
        get時（普通にアクセスしたとき）の挙動を定義
        """
        return render(request, "home.html", self.params)

    def post(self, request):
        """
        post時（ユーザーからの入力を受けたとき）の挙動を定義
        """
        chk = request.POST["choice"]
        self.params["result"] = "you selected: " + chk

        self.params["message"] = (
            "名前："
            + request.POST["name"]
            + "<br>メール："
            + request.POST["mail"]
            + "<br>年齢："
            + request.POST["age"]
        )
        self.params["form"] = Quiz_options(request.POST)
        return render(request, "top.html", self.params)


class quiz_individual(TemplateView):
    """
    個別クイズページのviewを設定
    """

    def __init__(self):
        """
        paramsの初期値を設定
        """
        # クイズを諸々設定
        quizzes = [
            {
                "question": "q1",
                "option1": "o1",
                "option2": "o2",
                "option3": "o3",
                "option4": "o4",
            },
            {
                "question": "q2",
                "option1": "o1",
                "option2": "o2",
                "option3": "o3",
                "option4": "o4",
            },
            {
                "question": "q3",
                "option1": "o1",
                "option2": "o2",
                "option3": "o3",
                "option4": "o4",
            },
        ]

        # クイズのページをランダムに一つ決める
        quiz_page_num = random.randrange(0, len(quizzes))

        # ランダムにクイズを抽出
        quiz = quizzes[quiz_page_num]

        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
            "quiz": quiz,
            "title": "Hello",
            "message": "なんのポケモンの鳴き声？",
            "goto": "home",
            "form": Quiz_options(),  # フォームを呼び出し
            "result": None,
        }

    def get(self, request):
        """
        get時（普通にアクセスしたとき）の挙動を定義
        """
        return render(request, "quiz_individual.html", self.params)

    def post(self, request):
        """
        post時（ユーザーからの入力を受けたとき）の挙動を定義
        """

        if "choice" in request.POST.keys():
            """
            選択肢が選ばれた状態
            """
            # ユーザーによる選択肢を格納
            chk = request.POST["choice"]
            self.params["result"] = "you selected: " + chk
        else:
            """
            選択肢が選ばれていない状態
            """
            self.params["result"] = "Please select any botton."

        return render(request, "quiz_individual.html", self.params)
