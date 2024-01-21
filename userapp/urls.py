from django.urls import path
from userapp import views
from userapp.views import EmailVerification,LoginView

urlpatterns = [
    path('creation/',views.creation.as_view()),
    path('verify/<str:token>/', EmailVerification.as_view(), name='email-verification'),
    path('login/', LoginView.as_view(), name='login'),

]