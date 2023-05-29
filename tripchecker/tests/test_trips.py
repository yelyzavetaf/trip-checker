import pytest
from django import urls
from django.urls import reverse
from tripchecker.models import Trips


@pytest.mark.parametrize('param', [ ('login')])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_wrong_dates_trip(user_create):
    with pytest.raises(Exception):
        Trips.objects.create(name="London", author_id=user_create.id, start="2023-04-22", end="2023-04-21", visited="Y", description="Second trip description")


@pytest.mark.django_db
def test_trip_detailed_view(first_trip, client):
    url = reverse('tripchecker:detail', kwargs={'pk': first_trip.id})
    response = client.get(url)
    assert f"{first_trip.name}" in str(response.content)










