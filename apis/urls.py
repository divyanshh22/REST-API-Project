from django.urls import path
from . import views

# Remember the real path is "/apis/" + whatever is written below, because
# django_project/urls.py mounts this file under the 'apis/' prefix.
#
# The name= part matters more than it looks. Templates look these names up with
# {% url 'student-list' %}, so no path is ever hardcoded in the HTML. Change the
# path here one day and every template follows along automatically.
urlpatterns = [
    path('', views.studentListView, name='student-list'),
    path('<int:pk>/', views.studentDetailView, name='student-detail'),
    path('<int:pk>/update/', views.studentUpdateView, name='student-update'),
    path('<int:pk>/partial-update/', views.studentPartialUpdateView, name='student-partial-update'),
    path('<int:pk>/delete/', views.studentDeleteView, name='student-delete'),
]

# The <int:pk> bit only matches digits. That means /apis/abc/ gets an instant 404
# from the URL resolver, instead of travelling all the way into the view and
# blowing up there.
