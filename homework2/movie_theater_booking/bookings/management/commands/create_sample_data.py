from django.core.management.base import BaseCommand
from bookings.models import Movie, Seat
from django.contrib.auth.models import User
from datetime import date

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Create sample movies
        Movie.objects.get_or_create(
            title="The Matrix",
            defaults={
                "description": "A computer hacker learns about the true nature of reality and his role in the war against its controllers.",
                "release_date": date(1999, 3, 31),
                "duration": 136,
            },
        )
        
        Movie.objects.get_or_create(
            title="Inception",
            defaults={
                "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
                "release_date": date(2010, 7, 16),
                "duration": 148,
            },
        )

        # Create sample seats
        for seat_number in ["A1", "A2", "A3", "B1", "B2", "B3"]:
            Seat.objects.get_or_create(seat_number=seat_number, defaults={"booking_status": "available"})

        # Create a test user
        if not User.objects.filter(username="user").exists():
            User.objects.create_user("user", "user@example.com", "user123")
            self.stdout.write(self.style.SUCCESS("Test user created: username='user', password='user123'"))
        else:
            self.stdout.write(self.style.WARNING("Test user already exists"))

        self.stdout.write(self.style.SUCCESS("Sample data created or already exists"))
