from django.urls import path
from .views import FixtureListView

urlpatterns = [
    path('', FixtureListView.as_view(), name='fixture_list'),
]