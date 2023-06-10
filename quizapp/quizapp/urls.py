from django.urls import path
from django.contrib import admin

# viewsから関数を読み込む
from quiz.views import quiz_top
from quiz.views import quiz_individual


urlpatterns = [
    path("quiz/", quiz_top.as_view(), name="home"),
    path("quiz/test_mode", quiz_individual.as_view(), name="quiz_test_mode"),
    path("admin/", admin.site.urls),
]

"""
# 個別クイズ画面を設定する
for i in range(150):
    urlpatterns.append(
        path("quiz/quiz_" + str(i), quiz_individual.as_view(), name="quiz_" + str(i)),
    )
"""
