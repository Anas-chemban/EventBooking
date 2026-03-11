from django.urls import path
from api.v1.events.views import (
    VenueListCreateView,
    EventListCreateView,
    EventDetailView,
    PublicEventListView,
    CancelEventView,
)

urlpatterns = [
    path('venues/', VenueListCreateView.as_view()),
    path('my-events/', EventListCreateView.as_view()),
    path('events/<int:pk>/', EventDetailView.as_view()),
    path('public-events/', PublicEventListView.as_view()),
    path('events/<int:event_id>/cancel/', CancelEventView.as_view()),
]
