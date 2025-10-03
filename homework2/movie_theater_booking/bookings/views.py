from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, get_object_or_404
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer, SeatBookingSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]  # Allow public access to list and retrieve movies

    @action(detail=True, methods=['get'])
    def available_seats(self, request, pk=None):
        movie = self.get_object()
        available_seats = Seat.objects.filter(booking_status='available')
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data)


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [AllowAny]  # Allow public access to list and retrieve seats

    @action(detail=False, methods=['get'])
    def available(self, request):
        available_seats = Seat.objects.filter(booking_status='available')
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        seat = self.get_object()
        movie_id = request.data.get('movie_id')

        if not movie_id:
            return Response({'error': 'Movie ID is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = SeatBookingSerializer(
            data={'movie_id': movie_id, 'seat_id': seat.id},
            context={'request': request}
        )

        if serializer.is_valid():
            booking = serializer.create(serializer.validated_data)
            return Response(BookingSerializer(booking).data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]  # Bookings require login

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Booking.objects.none()
        return Booking.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def history(self, request):
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


# Template views for UI
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})


def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    available_seats = Seat.objects.filter(booking_status='available')
    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seats': available_seats
    })


def booking_history(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = []
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})
