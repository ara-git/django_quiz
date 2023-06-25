from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Quiz
import random


class quiz_top(TemplateView):
    def __init__(self):
        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
            "title": "Hello",
            "message": "↓のボタンからゲームを始めてね",
        }

        self.params["goto"] = "quiz_test_mode"

    def get(self, request):
        """
        get時（普通にアクセスしたとき）の挙動を定義
        """
        # 正解数の初期値を設定する
        request.session["win_counter"] = 0
        # 残機の初期値を設定する
        request.session["life"] = 3
        return render(request, "home.html", self.params)

    def post(self, request):
        """
        post時（ユーザーからの入力を受けたとき）の挙動を定義
        """
        chk = request.POST["choice"]
        self.params["result"] = "you selected: " + chk

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
            "result": None,
        }

    def get(self, request):
        """
        get時（普通にアクセスしたとき）の挙動を定義
        """

        """
        request.sessionに正解が登録されていなかったら新規にクイズを作成して、登録
        """
        if "poke_num_answer" not in request.session:
            self._make_quiz_set()

            # クイズの正解をrequest.sessionに格納
            request.session["poke_num_answer"] = self.poke_num_answer
            request.session["poke_name_answer"] = self.poke_name_answer

        """
        正解数の初期値を設定
        """

        """
        パラメータをupdate
        """
        self.params.update(
            {
                "poke_name_options": self.poke_name_all_list,
                "poke_num_answer": request.session["poke_num_answer"],
                "poke_name_answer": request.session["poke_name_answer"],
                "win_counter": request.session["win_counter"],
                "life": request.session["life"],
            }
        )
        return render(request, "quiz_individual.html", self.params)

    def post(self, request):
        """
        post時（ユーザーからの入力を受けたとき）の挙動を定義

        具体的には以下の通り
        - ユーザーの回答が正解か否かを判定し、その時の挙動も定義
        - request.sessionに正解が登録されていなかったら新規にクイズを作成して、登録
        - パラメータをupdate
        """

        """
        ユーザーの回答が正解か否かを判定し、その時の挙動も定義
        """
        # ユーザーによる選択肢を格納
        selected_value = request.POST["selected_value"]

        # デバッグ用：
        self.params["result"] = [
            selected_value,
            request.session["poke_name_answer"],
        ]

        if selected_value == request.session["poke_name_answer"]:
            """
            クイズに正解した
            1. 正解カウントを増やす
            2. クイズを更新
            3. パラメータ(params)を更新
            """

            # 正解カウントを増やす
            request.session["win_counter"] += 1

            # クイズを新規作成し、request.sessionに格納
            self._make_quiz_set()
            request.session["poke_num_answer"] = self.poke_num_answer
            request.session["poke_name_answer"] = self.poke_name_answer

            # パラメータをupdate
            self.params.update(
                {
                    "poke_name_options": self.poke_name_all_list,
                    "poke_num_answer": request.session["poke_num_answer"],
                    "poke_name_answer": request.session["poke_name_answer"],
                    "win_counter": request.session["win_counter"],
                    "life": request.session["life"],
                }
            )

            return render(request, "quiz_individual.html", self.params)

        else:
            """
            クイズに不正解した
            1. 正解カウントを増やす
            2. パラメータ(params)を更新
            3. クイズを更新

            正解側と2, 3の順が異なるのは、htmlには古いクイズをパラメータとして渡したいため。
            """
            # 残機を減らす
            request.session["life"] -= 1

            if request.session["life"] > 0:
                """
                まだ残機が残っている
                """
                # パラメータをupdate
                self.params.update({"goto": "quiz_test_mode"})
                self.params.update(
                    {
                        "poke_name_options": self.poke_name_all_list,
                        "poke_num_answer": request.session["poke_num_answer"],
                        "poke_name_answer": request.session["poke_name_answer"],
                        "win_counter": request.session["win_counter"],
                        "life": request.session["life"],
                    }
                )

                # クイズを新規作成し、request.sessionに格納
                self._make_quiz_set()
                request.session["poke_num_answer"] = self.poke_num_answer
                request.session["poke_name_answer"] = self.poke_name_answer

                # 失敗画面に移動
                return render(request, "fail.html", self.params)

            else:
                """
                ゲームオーバー
                """
                # パラメータを更新
                self.params.update(
                    {
                        "win_counter": request.session["win_counter"],
                    }
                )
                # ゲームオーバー画面に繊維
                return render(request, "game_over.html", self.params)

    def _make_quiz_set(self):
        """
        DBからクイズを作成
        具体的には、ポケモンの名前・番号の選択肢と、その答えをランダムに作成する。
        """
        # 答えとなるポケモンの番号を作成
        self.poke_num_answer = random.randint(1, len(self.poke_name_all_list))

        # 答えとなるポケモンの名前を作成
        self.poke_name_answer = self.poke_name_all_list[self.poke_num_answer - 1]

        # 左埋め
        self.poke_num_answer = str(self.poke_num_answer).zfill(3)
