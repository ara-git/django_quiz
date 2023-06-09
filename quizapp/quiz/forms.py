from django import forms


class Quiz_options(forms.Form):
    quiz = {
        "options": [
            ("one", "フシギダネ"),
            ("two", "ガブリアス"),
            ("tree", "ジバコイル"),
            ("four", "サンダー"),
            ("five", "ミライドン"),
        ],
        "answer": "two",
    }

    options = quiz["options"]
    answer = quiz["answer"]

    choice = forms.ChoiceField(
        label="radio", choices=options, widget=forms.Select(attrs={"size": 5})
    )
