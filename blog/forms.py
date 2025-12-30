from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "status"]
        labels = {
            "title": "제목",
            "content": "내용",
            "status": "공개 상태",
        }
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "제목을 입력하세요"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 12, "placeholder": "본문을 입력하세요"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            (Post.STATUS_DRAFT, "초안"),
            (Post.STATUS_PUBLISHED, "공개"),
        ]
        if not self.instance.pk:
            self.fields["status"].initial = Post.STATUS_DRAFT


class ManageLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "아이디"}),
    )
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "비밀번호"}),
    )


class ManageSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        labels = {
            "username": "아이디",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "아이디"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "비밀번호"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "비밀번호 확인"}
        )
