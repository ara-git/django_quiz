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
        self.poke_db = Quiz.objects.all()
        self.poke_name_all_list = self.poke_db.values_list("JP", flat=True)

        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
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

        if "poke_num_answer" not in request.session:
            """
            request.sessionに正解が登録されていなかったら新規にクイズを作成して、登録
            """
            self._make_quiz_set()

            # クイズの正解をrequest.sessionに格納
            request.session["poke_num_answer"] = self.poke_num_answer
            request.session["poke_name_answer"] = self.poke_name_answer

        # paramsをupdate
        self.params.update(
            {
                "poke_name_options": self.poke_name_all_list,
                "poke_num_answer": request.session["poke_num_answer"],
                "poke_name_answer": request.session["poke_name_answer"],
            }
        )
        return render(request, "quiz_individual.html", self.params)

    def post(self, request):
        """
        post時（ユーザーからの入力を受けたとき）の挙動を定義
        """
        # ユーザーによる選択肢を格納
        selected_value = request.POST["selected_value"]

        if selected_value == request.session["poke_name_answer"]:
            """
            クイズに正解した
            """
            # デバッグ用：
            self.params["result"] = [
                selected_value,
                request.session["poke_name_answer"],
            ]
            # クイズの正解をリセットする
            request.session.pop("poke_num_answer")
            request.session.pop("poke_name_answer")
        else:
            """
            クイズに不正解した
            """
            self.params["result"] = [
                selected_value,
                request.session["poke_name_answer"],
            ]

        if "poke_num_answer" not in request.session:
            """
            request.sessionに正解が登録されていなかったら新規にクイズを作成して、登録
            """
            self._make_quiz_set()

            # クイズの正解をrequest.sessionに格納
            request.session["poke_num_answer"] = self.poke_num_answer
            request.session["poke_name_answer"] = self.poke_name_answer

        # paramsをupdate
        self.params.update(
            {
                "poke_name_options": self.poke_name_all_list,
                "poke_num_answer": request.session["poke_num_answer"],
                "poke_name_answer": request.session["poke_name_answer"],
            }
        )

        return render(request, "quiz_individual.html", self.params)

    def _make_quiz_set(self):
        """
        DBからクイズを作成
        具体的には、ポケモンの名前・番号の選択肢と、その答えをランダムに作成する。
        """
        # 答えとなるポケモンの番号を作成
        self.poke_num_answer = random.randint(1, len(self.poke_name_all_list))

        # 答えとなるポケモンの名前を作成
        self.poke_name_answer = self.poke_name_all_list[self.poke_num_answer - 1]
