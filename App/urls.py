from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate

from .views import (RegisterView, HomeView, DashboardView, CMSDashboardView, CMSRegisterView, 
PredavacIzborView, PredavacReizborView, VisiPredavacIzborView, VisiPredavacReizborView, 
ProfesorStrucnogStudijaIzborView, ProfesorStrucnogStudijaReizborView, ProfesorStrucnogStudijaTrajniView,
QuestionnaireRedirectView, ApplicationDetailView  )



def user_login_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                messages.error(request, "Invalid credentials. Please try again.")
                return render(request, 'login.html') 

 
            login_response = auth_views.LoginView.as_view(template_name='login.html')(request, *args, **kwargs)
            return redirect('dashboard')

        messages.error(request, "Invalid credentials. Please try again.")
        return render(request, 'login.html')


    return auth_views.LoginView.as_view(template_name='login.html')(request, *args, **kwargs)

def cms_login_view(request, *args, **kwargs):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)

        if user is not None:

            if user.is_superuser:

                auth_views.LoginView.as_view(template_name='CMS_Login.html')(request, *args, **kwargs)
                return redirect('admin_dashboard')
            else:

                messages.error(request, "Invalid credentials. Please try again.")
                return render(request, 'CMS_Login.html')
        else:

            messages.error(request, "Invalid credentials. Please try again.")
            return render(request, 'CMS_Login.html')


    return auth_views.LoginView.as_view(template_name='CMS_Login.html')(request, *args, **kwargs)




urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', user_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('questionnaire/predavac-izbor/', PredavacIzborView.as_view(), name='predavac_izbor'),
    path('questionnaire/predavac-reizbor/', PredavacReizborView.as_view(), name='predavac_reizbor'),
    path('questionnaire/visipredavac-izbor/', VisiPredavacIzborView.as_view(), name='visi_predavac_izbor'),
    path('questionnaire/visipredavacre-izbor/', VisiPredavacReizborView.as_view(), name='visi_predavac_reizbor'),
    path('questionnaire/profesor-strucnog-studija-izbor/', ProfesorStrucnogStudijaIzborView.as_view(), name='profesor_strucnog_studija_izbor'),
    path('questionnaire/profesor-strucnog-studija-reizbor/', ProfesorStrucnogStudijaReizborView.as_view(), name='profesor_strucnog_studija_reizbor'),
    path('questionnaire/profesor-strucnog-studija-trajni/', ProfesorStrucnogStudijaTrajniView.as_view(), name='profesor_strucnog_studija_trajni'),
    path('questionnaire/<int:position_id>/', QuestionnaireRedirectView.as_view(), name='questionnaire_redirect'),

    path('admin-register/', CMSRegisterView.as_view(), name='CMS_Register'),
    path('admin-login/', cms_login_view, name='CMS_Login'),
    path('admin-logout/', auth_views.LogoutView.as_view(next_page='CMS_Login'), name='admin_logout'),
    path('admin-dashboard/', CMSDashboardView.as_view(), name='admin_dashboard'),
    path('application/<int:id>/', ApplicationDetailView.as_view(), name='application_detail'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)