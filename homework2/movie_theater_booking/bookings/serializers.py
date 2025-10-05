from rest_framework import serializers
from .models import Movie, Seat, Booking

#DRF will automatically make serializer fields for the movie model due to using ModelSerializer
class MovieSerializer(serializers.ModelSerializer):
    # Will output the listed fields from the movie model in JSON format
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'duration']

# Same thing as the Movie serializer but for seats
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'booking_status']

class BookingSerializer(serializers.ModelSerializer):
    # Read-only fields to show movie title, seat num, and user. DRF uses the foreignkey to to grab var using "source='..'"
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    seat_number = serializers.CharField(source='seat.seat_number', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    # Returns booking info
    class Meta:
        model = Booking
        fields = ['id', 'movie', 'movie_title', 'seat', 'seat_number', 
                 'user', 'username', 'booking_date']
        read_only_fields = ['user', 'booking_date']

# Inherits from Serilizaers instead of modelserializer
class SeatBookingSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()
    
    def validate(self, data):
        # Makes sure that movie and seat exist in the db
        try:
            movie = Movie.objects.get(id=data['movie_id'])
            seat = Seat.objects.get(id=data['seat_id'])
        except Movie.DoesNotExist:
            raise serializers.ValidationError("Movie not found")
        except Seat.DoesNotExist:
            raise serializers.ValidationError("Seat not found")
        
        # Makes sure the seat is available to prevent double booking
        if seat.booking_status != 'available':
            raise serializers.ValidationError("Seat is not available")
        
        data['movie'] = movie
        data['seat'] = seat
        return data
    
    def create(self, validated_data):
        # Uses current user that is logged in
        user = self.context['request'].user

        # Makes the booking for user
        booking = Booking.objects.create(
            movie=validated_data['movie'],
            seat=validated_data['seat'],
            user=user
        )
        
        # Update seat status
        seat = validated_data['seat']
        seat.booking_status = 'booked'
        seat.save()
        
        return booking
