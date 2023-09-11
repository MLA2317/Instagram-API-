from django import forms
from post.models import Post, Comment


class NewPostform(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Location'}), required=True)
    image = forms.FileField(required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Description'}), required=True)

    class Meta:
        model = Post
        fields = ['image', 'location', 'description']


class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Write comment'}), required=True)

    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'post_id', 'message')
        exclude = ('user_id', 'post_id', 'message')


