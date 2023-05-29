import pytest
from django.contrib.auth.models import User

from tripchecker.models import Trips

@pytest.fixture
def user_create():
    u = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    return u

@pytest.fixture
def first_trip(user_create):
    ft = Trips.objects.create(name="Lviv", author_id=user_create.id, start="2023-04-01", end="2023-04-21", visited="Y", description="First trip description")
    return ft




