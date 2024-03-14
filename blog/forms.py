from django import forms
from .models import Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]  # 사용자로부터 입력받을 필드 명시


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "contents",
            "main_image",
            "country",
            "city",
            "date_of_visit",
        ]
