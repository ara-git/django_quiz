from django.urls import path
from django.contrib import admin

# viewsから関数を読み込む
from quiz.views import quiz_top
from quiz.views import quiz_individual


urlpatterns = [
    path("quiz/", quiz_top.as_view(), name="home"),
    path("admin/", admin.site.urls),
]

# 個別クイズ画面を設定する
urlpatterns.append(
    path("quiz/quiz_1/", quiz_individual.as_view(), name="quiz_1"),
)
