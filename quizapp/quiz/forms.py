from django import forms


class region_option_class(forms.Form):
    REGION_CHOICES = [
        ("kanto", "カントーまで"),
        ("jouto", "ジョウトまで"),
        ("houen", "ホウエンまで"),
        ("sinou", "シンオウまで"),
        ("issyu", "イッシュまで"),
    ]

    region_option = forms.ChoiceField(
        choices=REGION_CHOICES,
        widget=forms.RadioSelect,
    )


"""
class debug_mode_class(forms.Form):
    debug_checkbox = forms.BooleanField(required=False)
"""
