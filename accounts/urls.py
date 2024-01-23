from django.urls import path
from .import views

urlpatterns = [
    path('login/', views.UserLogin.as_view(),name="login"),
    path('registration/', views.UserRegistrationView.as_view(),name="registration"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/',views.logOut,name='logout')
]