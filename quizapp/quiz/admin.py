from django.contrib import admin
from .models import Quiz

# Quizクラスを管理ツールで編集可能にする
admin.site.register(Quiz)
