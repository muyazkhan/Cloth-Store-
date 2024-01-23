from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    class Meta:
        model = Review
        fields = ['user', 'clothing_item','rating', 'comment']


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['clothing_item'].disabled = True
            self.fields['clothing_item'].widget = forms.HiddenInput()
            self.fields['user'].disabled = True
            self.fields['user'].widget = forms.HiddenInput()