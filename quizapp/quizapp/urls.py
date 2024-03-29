from django.urls import path
from django.contrib import admin

# viewsから関数を読み込む
from quiz.views import quiz_top
from quiz.views import quiz_individual

urlpatterns = [
    path("", quiz_top.as_view(), name="home"),
    path("quiz_mode", quiz_individual.as_view(), name="quiz_mode"),
    path("admin/", admin.site.urls),
]
