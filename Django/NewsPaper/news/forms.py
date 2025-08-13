from django import forms

from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    post_title = forms.CharField(min_length=10, label='Title')
    post_text = forms.CharField(widget=forms.Textarea, min_length=60, label='Text')
    post_category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                   widget=forms.CheckboxSelectMultiple(
                                                       attrs={'class': 'category-list'}),
                                                   label='Category')
    post_author = forms.ModelChoiceField(queryset=Author.objects.all(), label='Author')

    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_text',
            'post_category',
            'post_author',
        ]

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        post_title = cleaned_data.get('post_title')
        post_text = cleaned_data.get('post_text')
        if post_title == post_text:
            raise forms.ValidationError("Title and text must be different")
        return cleaned_data

    def clean_title(self):
        post_title = self.cleaned_data["post_title"]
        if post_title[0].islower():
            raise forms.ValidationError(
                "Title must start with a uppercase letter"
            )
        return post_title
