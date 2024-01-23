from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import AuthenticationForm ,PasswordChangeForm
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import RegistrationForm
from .models import User

class UserRegistrationView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        messages.success(self.request, 'Registration Done! Check your mail for confirmation')

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        confirm_mail = f"http://{self.request.get_host()}/accounts/activate/{uid}/{token}"
        email_subject = "Confirmation Email"
        email_body = render_to_string('email.html', {'confirm_mail': confirm_mail})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
        return super().form_valid(form)
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.warning(self.request, 'Your information is incorrect')
        return response



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.save()
        return  redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Activation link is invalid!")


class UserLogin(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successfully')
        return super().form_valid(form)


    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        messages.warning(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)

def logOut(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')
