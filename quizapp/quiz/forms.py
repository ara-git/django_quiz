from django import forms


class Quiz_options(forms.Form):
    options = [
        ("one", "フシギダネ"),
        ("two", "ガブリアス"),
        ("tree", "ジバコイル"),
        ("four", "サンダー"),
        ("five", "ミライドン"),
    ]
    choice = forms.ChoiceField(
        label="radio", choices=options, widget=forms.Select(attrs={"size": 5})
    )
