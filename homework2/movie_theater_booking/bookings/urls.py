from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet, basename='booking')

urlpatterns = [
    
    # Template URLs
    path('', views.movie_list, name='movie_list'),
    path('book/<int:movie_id>/', views.seat_booking, name='book_seat'),
    path('history/', views.booking_history, name='booking_history'),
    
    # Auth URLs
    path('accounts/', include('django.contrib.auth.urls')),
]
