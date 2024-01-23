from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount


class RegistrationForm(UserCreationForm):
    phone_no = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'phone_no', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            phone_no = self.cleaned_data.get("phone_no")
            if not UserAccount.objects.filter(user=user).exists():
                UserAccount.objects.create(
                    phone_no=phone_no,
                    user=user,
                    customer_id=1000 + user.id
                )

        return user
