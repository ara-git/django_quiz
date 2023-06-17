from django.db import models


class Quiz(models.Model):
    # DBからポケモン名を読み込む(変数名はDB列名とそろえる必要がある)
    # idは指定する必要なし
    JP = models.CharField(max_length=100)

    class Meta:
        # 読み込むDBテーブルを設定
        db_table = "pokemon_kanto"
