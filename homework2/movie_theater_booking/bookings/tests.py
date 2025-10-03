# bookings/tests.py - Comprehensive Test Suite for Movie Theater Booking System

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import Movie, Seat, Booking
import json


class ModelTests(TestCase):
    """Unit tests for Django models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='A test movie description',
            release_date=date.today(),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number='A1',
            booking_status='available'
        )

    def test_movie_creation(self):
        """Test movie model creation and string representation"""
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.description, 'A test movie description')
        self.assertEqual(self.movie.duration, 120)
        self.assertEqual(str(self.movie), 'Test Movie')
        
    def test_movie_ordering(self):
        """Test movie ordering by release date"""
        movie2 = Movie.objects.create(
            title='Earlier Movie',
            description='Earlier movie',
            release_date=date.today() - timedelta(days=1),
            duration=90
        )
        movies = Movie.objects.all()
        self.assertEqual(movies[0], movie2)  # Earlier movie comes first
        self.assertEqual(movies[1], self.movie)

    def test_seat_creation(self):
        """Test seat model creation and string representation"""
        self.assertEqual(self.seat.seat_number, 'A1')
        self.assertEqual(self.seat.booking_status, 'available')
        self.assertEqual(str(self.seat), 'Seat A1 - available')

    def test_seat_choices(self):
        """Test seat status choices"""
        # Test available status
        self.assertEqual(self.seat.booking_status, 'available')
        
        # Test booked status
        self.seat.booking_status = 'booked'
        self.seat.save()
        self.assertEqual(self.seat.booking_status, 'booked')
        
        # Test maintenance status
        self.seat.booking_status = 'maintenance'
        self.seat.save()
        self.assertEqual(self.seat.booking_status, 'maintenance')

    def test_booking_creation(self):
        """Test booking model creation and relationships"""
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)
        self.assertEqual(booking.user, self.user)
        self.assertIsNotNone(booking.booking_date)
        
        expected_str = f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"
        self.assertEqual(str(booking), expected_str)

    def test_booking_unique_constraint(self):
        """Test that same movie-seat combination cannot be booked twice"""
        # Create first booking
        booking1 = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        
        # Create another user
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Try to create duplicate booking for same movie and seat
        with self.assertRaises(Exception):
            Booking.objects.create(
                movie=self.movie,
                seat=self.seat,
                user=user2
            )


class ViewTests(TestCase):
    """Unit tests for Django views (templates)"""
    
    def setUp(self):
        """Set up test data for view tests"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='A test movie description',
            release_date=date.today(),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number='A1',
            booking_status='available'
        )

    def test_movie_list_view(self):
        """Test movie list template view"""
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertContains(response, 'Available Movies')
        self.assertTemplateUsed(response, 'bookings/movie_list.html')

    def test_movie_list_view_no_movies(self):
        """Test movie list view when no movies exist"""
        Movie.objects.all().delete()
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Movies Available')

    def test_seat_booking_view(self):
        """Test seat booking template view"""
        response = self.client.get(reverse('book_seat', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)
        self.assertContains(response, 'Select Your Seat')
        self.assertTemplateUsed(response, 'bookings/seat_booking.html')

    def test_seat_booking_view_invalid_movie(self):
        """Test seat booking view with invalid movie ID"""
        response = self.client.get(reverse('book_seat', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_booking_history_view_anonymous(self):
        """Test booking history view for anonymous user"""
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please Log In')
        self.assertTemplateUsed(response, 'bookings/booking_history.html')

    def test_booking_history_view_authenticated(self):
        """Test booking history view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Booking History')

    def test_booking_history_with_bookings(self):
        """Test booking history view with actual bookings"""
        # Create a booking
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)
        self.assertContains(response, self.seat.seat_number)


class APITests(APITestCase):
    """Unit tests for REST API endpoints"""
    
    def setUp(self):
        """Set up test data for API tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='A test movie description',
            release_date=date.today(),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number='A1',
            booking_status='available'
        )

    def test_movie_list_api_unauthenticated(self):
        """Test movie list API without authentication"""
        url = '/api/movies/'
        response = self.client.get(url)
        # Movies should be viewable without authentication
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_list_api_authenticated(self):
        """Test movie list API with authentication"""
        self.client.force_authenticate(user=self.user)
        url = '/api/movies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if paginated response structure is correct
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            movie_data = response.data['results'][0]
        else:
            self.assertEqual(len(response.data), 1)
            movie_data = response.data[0]
            
        self.assertEqual(movie_data['title'], 'Test Movie')

    def test_movie_detail_api(self):
        """Test movie detail API endpoint"""
        url = f'/api/movies/{self.movie.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Movie')
        self.assertEqual(response.data['duration'], 120)

    def test_seat_list_api(self):
        """Test seat list API endpoint"""
        url = '/api/seats/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_available_seats_api(self):
        """Test available seats API endpoint"""
        url = '/api/seats/available/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if seat is in results
        if 'results' in response.data:
            seats = response.data['results']
        else:
            seats = response.data
            
        self.assertEqual(len(seats), 1)
        self.assertEqual(seats[0]['seat_number'], 'A1')

    def test_booking_requires_authentication(self):
        """Test that booking endpoints require authentication"""
        url = '/api/bookings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_booking_list(self):
        """Test booking list API with authentication"""
        self.client.force_authenticate(user=self.user)
        url = '/api/bookings/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_booking_history_api(self):
        """Test booking history API endpoint"""
        # Create a booking first
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        url = '/api/bookings/history/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if 'results' in response.data:
            bookings = response.data['results']
        else:
            bookings = response.data
            
        self.assertEqual(len(bookings), 1)

    def test_seat_booking_api(self):
        """Test seat booking API endpoint"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/seats/{self.seat.id}/book/'
        data = {'movie_id': self.movie.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that seat status changed
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, 'booked')

    def test_seat_booking_api_missing_movie(self):
        """Test seat booking API without movie ID"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/seats/{self.seat.id}/book/'
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_seat_booking_api_invalid_movie(self):
        """Test seat booking API with invalid movie ID"""
        self.client.force_authenticate(user=self.user)
        url = f'/api/seats/{self.seat.id}/book/'
        data = {'movie_id': 999}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class IntegrationTests(APITestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up test data for integration tests"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Integration Test Movie',
            description='A movie for integration testing',
            release_date=date.today(),
            duration=150
        )
        self.seat1 = Seat.objects.create(
            seat_number='A1',
            booking_status='available'
        )
        self.seat2 = Seat.objects.create(
            seat_number='A2',
            booking_status='available'
        )

    def test_complete_booking_workflow(self):
        """Test complete booking workflow from API perspective"""
        # Authenticate user
        self.client.force_authenticate(user=self.user)
        
        # Step 1: Get list of movies
        movies_url = '/api/movies/'
        movies_response = self.client.get(movies_url)
        self.assertEqual(movies_response.status_code, status.HTTP_200_OK)
        
        # Step 2: Check available seats
        seats_url = '/api/seats/available/'
        seats_response = self.client.get(seats_url)
        self.assertEqual(seats_response.status_code, status.HTTP_200_OK)
        
        # Extract seats from response
        if 'results' in seats_response.data:
            available_seats = seats_response.data['results']
        else:
            available_seats = seats_response.data
            
        self.assertEqual(len(available_seats), 2)  # Both seats should be available
        
        # Step 3: Book the first seat
        book_url = f'/api/seats/{self.seat1.id}/book/'
        book_data = {'movie_id': self.movie.id}
        book_response = self.client.post(book_url, book_data)
        self.assertEqual(book_response.status_code, status.HTTP_201_CREATED)
        
        # Step 4: Verify seat status changed
        self.seat1.refresh_from_db()
        self.assertEqual(self.seat1.booking_status, 'booked')
        
        # Step 5: Check that available seats decreased
        seats_response_after = self.client.get(seats_url)
        if 'results' in seats_response_after.data:
            available_seats_after = seats_response_after.data['results']
        else:
            available_seats_after = seats_response_after.data
            
        self.assertEqual(len(available_seats_after), 1)  # Only one seat left
        
        # Step 6: Check booking history
        history_url = '/api/bookings/history/'
        history_response = self.client.get(history_url)
        self.assertEqual(history_response.status_code, status.HTTP_200_OK)
        
        if 'results' in history_response.data:
            bookings = history_response.data['results']
        else:
            bookings = history_response.data
            
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0]['movie_title'], 'Integration Test Movie')
        self.assertEqual(bookings[0]['seat_number'], 'A1')

    def test_double_booking_prevention(self):
        """Test that double booking is prevented"""
        # Create initial booking
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat1,
            user=self.user
        )
        self.seat1.booking_status = 'booked'
        self.seat1.save()
        
        # Create another user
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Try to book the same seat with different user
        self.client.force_authenticate(user=user2)
        book_url = f'/api/seats/{self.seat1.id}/book/'
        book_data = {'movie_id': self.movie.id}
        response = self.client.post(book_url, book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_multiple_user_booking_scenario(self):
        """Test multiple users booking different seats"""
        # Create second user
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # User 1 books seat A1
        self.client.force_authenticate(user=self.user)
        book_url1 = f'/api/seats/{self.seat1.id}/book/'
        book_data1 = {'movie_id': self.movie.id}
        response1 = self.client.post(book_url1, book_data1)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # User 2 books seat A2
        self.client.force_authenticate(user=user2)
        book_url2 = f'/api/seats/{self.seat2.id}/book/'
        book_data2 = {'movie_id': self.movie.id}
        response2 = self.client.post(book_url2, book_data2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # Verify both bookings exist
        self.assertEqual(Booking.objects.count(), 2)
        
        # Verify each user sees only their own booking
        self.client.force_authenticate(user=self.user)
        history_response1 = self.client.get('/api/bookings/history/')
        if 'results' in history_response1.data:
            user1_bookings = history_response1.data['results']
        else:
            user1_bookings = history_response1.data
        self.assertEqual(len(user1_bookings), 1)
        
        self.client.force_authenticate(user=user2)
        history_response2 = self.client.get('/api/bookings/history/')
        if 'results' in history_response2.data:
            user2_bookings = history_response2.data['results']
        else:
            user2_bookings = history_response2.data
        self.assertEqual(len(user2_bookings), 1)

    def test_movie_available_seats_endpoint(self):
        """Test movie-specific available seats endpoint"""
        self.client.force_authenticate(user=self.user)
        
        # Get available seats for specific movie
        url = f'/api/movies/{self.movie.id}/available_seats/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should show both seats as available
        self.assertEqual(len(response.data), 2)
        
        # Book one seat
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat1,
            user=self.user
        )
        self.seat1.booking_status = 'booked'
        self.seat1.save()
        
        # Check available seats again
        response_after = self.client.get(url)
        self.assertEqual(response_after.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_after.data), 1)  # Only one seat left


class AdminInterfaceTests(TestCase):
    """Tests for Django admin interface"""
    
    def setUp(self):
        """Set up admin test data"""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.movie = Movie.objects.create(
            title='Admin Test Movie',
            description='Movie for admin testing',
            release_date=date.today(),
            duration=120
        )
        self.seat = Seat.objects.create(
            seat_number='B1',
            booking_status='available'
        )
        self.client = Client()

    def test_admin_login(self):
        """Test admin interface login"""
        response = self.client.post('/admin/login/', {
            'username': 'admin',
            'password': 'admin123'
        })
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)

    def test_admin_movie_list(self):
        """Test admin movie list page"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/bookings/movie/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Test Movie')

    def test_admin_seat_list(self):
        """Test admin seat list page"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/bookings/seat/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'B1')

    def test_admin_booking_list(self):
        """Test admin booking list page"""
        # Create a booking first
        user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=user
        )
        
        self.client.login(username='admin', password='admin123')
        response = self.client.get('/admin/bookings/booking/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')


# Custom test runner command to run specific test categories
class TestCategories:
    """Helper class to organize test categories for running specific test groups"""
    
    UNIT_TESTS = [
        'bookings.tests.ModelTests',
        'bookings.tests.ViewTests',
        'bookings.tests.APITests'
    ]
    
    INTEGRATION_TESTS = [
        'bookings.tests.IntegrationTests'
    ]
    
    ADMIN_TESTS = [
        'bookings.tests.AdminInterfaceTests'
    ]
    
    ALL_TESTS = UNIT_TESTS + INTEGRATION_TESTS + ADMIN_TESTS
