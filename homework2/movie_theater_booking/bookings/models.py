from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['release_date']

class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('maintenance', 'Maintenance'),
    ]
    
    seat_number = models.CharField(max_length=10, unique=True)
    booking_status = models.CharField(
        max_length=20, 
        choices=SEAT_STATUS_CHOICES, 
        default='available'
    )
    
    def __str__(self):
        return f"Seat {self.seat_number} - {self.booking_status}"
    
    class Meta:
        ordering = ['seat_number']

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('movie', 'seat')
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"
