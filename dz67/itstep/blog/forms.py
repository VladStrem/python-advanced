from django import forms
from .models import Post, Rating, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'status', 'category', 'tags', 'publish']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'class': 'form-control'}),
            # 'image': forms.ClearableFileInput(attrs={'multiple': False}),
            'publish': forms.DateTimeInput(attrs={'type': 'datetime-local'})}
        labels = {'title': 'Назва публікації', 'body': 'Текст публікації'}


class TagForm(forms.Form):
    name = forms.CharField(label="Title for tag",
                           help_text="Enter your tag",
                           max_length=10)
    slug = forms.SlugField(max_length=31,
                           help_text="Enter your slug")

    # def save(self, instance, **kwargs):
    #     instance.update(**kwargs)
    #     instance.save()
    #     return instance


class TagFormModel(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']

    def clean_name(self):
        value = self.cleaned_data['name']
        return value.lower()

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if len(slug) < 3:
            raise forms.ValidationError("Довжина менша за 3 символи")
        return slug

    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data.get("name")) < 3:
            self.add_error(None, "The total number of chars must be 3 or greate.")


# class RatingForm(forms.Form):
#     CHOICES = [(i, str(i)) for i in range(5, 0, -1)]
#     score = forms.ChoiceField(
#         choices=CHOICES,
#         widget=forms.RadioSelect(
#             attrs={'class': 'radio_1'}
#         ),
#         label="Score",
#     )
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, str(i)) for i in range(1, 6)]),
        }
        labels = {
            'rating': 'Rate this post',
        }