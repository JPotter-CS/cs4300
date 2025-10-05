from django.db import models
from django.contrib.auth.models import User

# Below is the movie class, it has fields for title, description, release date, and duration.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    
    # Returns the movie title
    def __str__(self):
        return self.title
    
    # Orders movies by release date
    class Meta:
        ordering = ['release_date']

# Class to represent individual seats to book within the theater
class Seat(models.Model):
    # 3 statuses for bookings
    SEAT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
    ]
    
    seat_number = models.CharField(max_length=10, unique=True)

    booking_status = models.CharField(
        max_length=20, 
        choices=SEAT_STATUS_CHOICES, 
        # Sets default to each seat as available
        default='available'
    )
    
    # Returns string stating seat number and its current status
    def __str__(self):
        return f"Seat {self.seat_number} - {self.booking_status}"
    
    # Orders seats by number
    class Meta:
        ordering = ['seat_number']

# Model to represent each users booking
class Booking(models.Model):
    # Link to which movie the booking is for
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # Link to which seat the booking is for
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    # Link to which user the booking is for 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Timestamp for when the booking was made
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Makes sure you can't book the same seat twice for the same movie
        unique_together = ('movie', 'seat')
        # Newest first
        ordering = ['-booking_date']
    
    # Returns a string stating the user, what movie, and what seat
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"
