from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import render, get_object_or_404
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer, SeatBookingSerializer


class MovieViewSet(viewsets.ModelViewSet):
    # queryset selects all movies
    queryset = Movie.objects.all()
    # Used to convert to/from JSON 
    serializer_class = MovieSerializer
    # Allow public access for movies
    permission_classes = [AllowAny]  

    @action(detail=True, methods=['get'])
    # Returns all seats that are available for the movie
    def available_seats(self, request, pk=None):
        movie = self.get_object()
        available_seats = Seat.objects.filter(booking_status='available')
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data)


class SeatViewSet(viewsets.ModelViewSet):
    # queryset selects all seats
    queryset = Seat.objects.all()
    # Converts to/from JSON
    serializer_class = SeatSerializer
    # Allow public access for seats
    permission_classes = [AllowAny] 

    # Returns seats with available status
    @action(detail=False, methods=['get'])
    def available(self, request):
        available_seats = Seat.objects.filter(booking_status='available')
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)

    # Creates a booking if seat is available for the specific movie. This requires authentication (logged in)
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

    # Ensure bookings requires login
    permission_classes = [IsAuthenticated]

    # Gets bookings based on the logged in user
    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Booking.objects.none()
        return Booking.objects.filter(user=user)

    # Returns a list of bookings from user
    @action(detail=False, methods=['get'])
    def history(self, request):
        bookings = self.get_queryset()
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)


# Gets all movies at displays as movie_list.html
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

# Gets a specific movie by id or 404 
# Gets all seats and displays at seat_bookings.html
def seat_booking(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    available_seats = Seat.objects.filter(booking_status='available')
    return render(request, 'bookings/seat_booking.html', {
        'movie': movie,
        'seats': available_seats
    })

# List bookings for logged in user or none if not logged in
# Get and displays at booking_history.html
def booking_history(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user)
    else:
        bookings = []
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})
