from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Quiz
import random
import yaml


class quiz_top(TemplateView):
    def __init__(self):
        with open("./quiz/static/quiz/url/config.yaml", "r") as file:
            config = yaml.safe_load(file)

        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
            "title": "ポケモン鳴き声クイズ",
            "message": "↓のボタンからゲームスタート！",
            "form_url": config["form_url"],
        }

        self.params["goto"] = "quiz_mode"

    def get(self, request):
        """
        get時（普通にアクセスしたとき）の挙動を定義
        """
        # 正解数の初期値を設定する
        request.session["win_counter"] = 0
        # 残機の初期値を設定する
        request.session["life"] = 3

        # ↓後で消す
        request.session["mode"] = "classic"

        return render(request, "home.html", self.params)

    def post(self, request):
        """
        post時（ユーザーからの入力を受けたとき）の挙動を定義
        """
        # ユーザーが入力したモードを保存する
        # request.session["mode"] = request.POST["mode_option"]

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
        self.poke_name_all_list = self.poke_db.values_list("name", flat=True)

        # パラメータを設定("goto"で指定しているのは、urlの名称。名称とurlの紐づけはurls.pyで指定)
        self.params = {
            "title": "ポケモン鳴き声クイズ",
            "message": "どのポケモンの鳴き声？",
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
        # ユーザーによる回答を格納
        selected_pokemon = request.POST["selected_pokemon"]

        # デバッグ用：
        self.params["result"] = [
            selected_pokemon,
            request.session["poke_name_answer"],
        ]

        if selected_pokemon == request.session["poke_name_answer"]:
            """
            クイズに正解した
            1. 正解カウントを増やす
            2. クイズを更新
            3. パラメータ(params)を更新
            """

            # 正解カウントを増やす
            request.session["win_counter"] += 1

            # クイズを新規作成し、request.sessionに格納
            self._make_quiz_set(mode=request.session["mode"])
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
                self.params.update({"goto": "quiz_mode"})
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
                self._make_quiz_set(mode=request.session["mode"])
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
                        "poke_name_options": self.poke_name_all_list,
                        "poke_num_answer": request.session["poke_num_answer"],
                        "poke_name_answer": request.session["poke_name_answer"],
                        "win_counter": request.session["win_counter"],
                    }
                )

                # クイズを作成する(次のクイズに向けて)
                self._make_quiz_set(mode=request.session["mode"])

                # クイズの正解をrequest.sessionに格納
                request.session["poke_num_answer"] = self.poke_num_answer
                request.session["poke_name_answer"] = self.poke_name_answer

                # ゲームオーバー画面に遷移
                return render(request, "game_over.html", self.params)

    def _make_quiz_set(self, mode):
        """
        DBからクイズを作成
        具体的には、ポケモンの名前・番号の選択肢と、その答えをランダムに作成する。

        Augs
            mode: classicかmodernか。この値で乱数の範囲を決める. 機能追加するまではイッシュ地方まで
        """
        # 答えとなるポケモンの番号を作成
        if mode == "classic":
            self.poke_num_answer = random.randint(1, 649)
        else:
            self.poke_num_answer = random.randint(1, len(self.poke_name_all_list))

        # 答えとなるポケモンの名前を作成
        self.poke_name_answer = self.poke_name_all_list[self.poke_num_answer - 1]

        # 図鑑番号を左埋め
        self.poke_num_answer = str(self.poke_num_answer).zfill(3)
