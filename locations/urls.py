from django.urls import path
from .views import GeoLocationListView, CreateMamaMbogaNearbyView

urlpatterns = [
    path('locations/', GeoLocationListView.as_view(), name='location-list'),
    path('locations/add/', CreateMamaMbogaNearbyView.as_view(), name='location-add'),
]
