from django.urls import path
from . import views

# These are the HTML pages. Since django_project/urls.py mounts this app at the
# empty string '', these paths are the real site URLs - which is why homeView
# below is the page you land on when you open the site with no path at all.
urlpatterns = [
    path('', views.homeView, name='Home-View'),
    path('about/', views.aboutView, name='About-View'),
    path('add/', views.addStudentView, name='Add-View'),
    path('update/', views.updateStudentView, name='Update-View'),
    path('partial-update/', views.partialUpdateView, name='Partial-Update-View'),
    path('delete/', views.deleteStudentView, name='Delete-View'),
]
