from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Quiz
from .forms import Quiz_options
import random


class quiz_top(TemplateView):
    def __init__(self):
        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
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
        # クイズを更新するか否か
        self.flag_update_quiz = True

        # 名称と番号が記録されたDBを読みこむ
        # 読み込まれたDBは"query_set"型となる
        self.poke_db = Quiz.objects.all().values()

        if self.flag_update_quiz:
            # クイズを作る
            self._make_quiz_set()

        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
            "poke_num_options": self.poke_num_options,
            "poke_name_options": self.poke_name_options,
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
        self.flag_update_quiz = 0

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

    def _make_quiz_set(self, num_of_options=4):
        """
        DBからクイズを作成
        具体的には、ポケモンの名前・番号の選択肢と、その答えをランダムに作成する。
        """
        # 選択肢となるポケモンの番号のリストを作成
        self.poke_num_options = random.sample(
            range(len(self.poke_db)), k=num_of_options
        )

        # 選択肢となるポケモンの名前のリストを作成
        self.poke_name_options = []
        for i in range(num_of_options):
            self.poke_name_options.append(self.poke_db[self.poke_num_options[i]]["JP"])

        # 答えとなるポケモンの番号を作成
        self.poke_num_answer = random.randrange(num_of_options)

        # 答えとなるポケモンの名前を作成
        self.poke_name_answer = self.poke_name_options[self.poke_num_answer]
