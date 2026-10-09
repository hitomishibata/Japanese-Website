from django import forms
from django.contrib import admin
from .models import Blog


class BlogAdminForm(forms.ModelForm):
    # ArrayField doesn't expose its base field's `choices` to the admin form
    # by default (it renders as a plain comma-separated text input), so the
    # tags/grammars widgets are overridden here to use proper multi-selects.
    tags = forms.MultipleChoiceField(
        choices=Blog.TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple,
    )
    grammars = forms.MultipleChoiceField(
        choices=Blog.GRAMMAR_CHOICES,
        widget=forms.SelectMultiple,
    )

    class Meta:
        model = Blog
        fields = "__all__"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
