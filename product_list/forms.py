from django import forms
from .models import SIZE,COLORS
from accounts.models import UserAccount,User


class ClothingFilterForm(forms.Form):
    size = forms.ChoiceField(choices=(), required=False)
    color = forms.ChoiceField(choices=(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].choices = SIZE
        self.fields['color'].choices = COLORS


class UpdateForm(forms.ModelForm):
    phone_no = forms.CharField(max_length=13)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            try:
                user_account = self.instance.user_account
            except:
                user_account = None

            if user_account:
                self.fields['phone_no'].initial = user_account.phone_no


    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_account.phone_no = self.cleaned_data.get("phone_no")
            user_account.save()

        return user