"""doctortracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('registration/',views.RegistrationPage,name="registration"),
    path('login/',views.LoginPage,name="login"),
    path('registeruser/',views.RegisterUser, name="registeruser"),
    path('login_evealuate/',views.login_evaluation,name="login-evaluate"),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('forgot_password_email/',views.forgot_password_email,name="forgot_password_email"),
    path('reset_password/',views.reset_password,name="reset_password"),
]


