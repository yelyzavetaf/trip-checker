import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView
from tripchecker.forms import RegistrationForm
from tripchecker.forms import TripsCreateForm
from tripchecker.models import *
import folium


@login_required(login_url="/login")
def map_context(request):
    places = Trips.objects.all().filter(author=request.user)
    m = folium.Map(location=[49.8419, 24.0315], zoom_start=5, height='100%', width="100%", position='relative', min_zoom=3, max_zoom=13)

    now = datetime.datetime.today()
    trips_passed = places.order_by('start').values().filter(start__lt=now)
    trips_coming = places.order_by('start').values().filter(end__gt=now)
    for place in places:
        if place.latitude and place.longitude:
            coordinates = (place.latitude, place.longitude)
            if place.start < datetime.date.today():
                if place.visited == "N":
                    folium.Marker(coordinates, popup=place.name, icon = folium.Icon(color='red', icon='asterisk')).add_to(m)
                else:
                    folium.Marker(coordinates, popup=place.name, icon = folium.Icon(color='green', icon='flag')).add_to(m)
            else:
                folium.Marker(coordinates, popup=place.name, icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)

    context = {'map': m._repr_html_(), 'trips_passed': trips_passed, 'trips_coming' : trips_coming}

    return render(request, 'tripchecker/trips_list.html', context)




class DetailView(generic.DetailView):
    model = Trips
    template_name = 'tripchecker/trip_details.html'
    context_object_name = 'trip'



class UpdateView(generic.UpdateView):
    model = Trips
    form_class = TripsCreateForm
    template_name = 'tripchecker/trip_update.html'
    success_url = "/"



class DeleteView(generic.DeleteView):
    model = Trips
    template_name = 'tripchecker/trip_delete.html'
    success_url = "/"



class CreateTripView(FormView):
    template_name = "tripchecker/trips_create.html"
    form_class = TripsCreateForm
    success_url = "/"

    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            form.save()
            return super().form_valid(form)



class SignUp(generic.CreateView):
    form_class = RegistrationForm
    # success_url = "/"
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'

