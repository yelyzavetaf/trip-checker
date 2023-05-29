from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'tripchecker'
urlpatterns = [
    path('', views.map_context, name="trips_list"),
    path('trips/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('trips/create/', login_required(views.CreateTripView.as_view()), name='new_trip'),
    path('trips/<int:pk>/update', login_required(views.UpdateView.as_view()), name='update'),
    path('trips/<int:pk>/delete', login_required(views.DeleteView.as_view()), name='delete'),
    path('sign-up', views.SignUp.as_view(), name='sign_up')

]