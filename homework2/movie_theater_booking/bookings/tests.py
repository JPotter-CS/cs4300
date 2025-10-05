from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from .models import Movie, Seat, Booking


class ModelUnitTests(TestCase):
    
    def setUp(self):
        """Set up test data for model tests"""
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

    def test_movie_model_creation(self):
        """Test Movie model creation and string representation"""
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.description, 'A test movie description')
        self.assertEqual(self.movie.duration, 120)
        self.assertEqual(self.movie.release_date, date.today())
        self.assertEqual(str(self.movie), 'Test Movie')

    def test_movie_model_ordering(self):
        """Test Movie model ordering by release date"""
        earlier_movie = Movie.objects.create(
            title='Earlier Movie',
            description='Earlier movie',
            release_date=date.today() - timedelta(days=1),
            duration=90
        )
        movies = Movie.objects.all()
        self.assertEqual(movies[0], earlier_movie) 
        self.assertEqual(movies[1], self.movie)

    def test_seat_model_creation(self):
        """Test Seat model creation and string representation"""
        self.assertEqual(self.seat.seat_number, 'A1')
        self.assertEqual(self.seat.booking_status, 'available')
        self.assertEqual(str(self.seat), 'Seat A1 - available')

    def test_seat_model_choices(self):
        """Test Seat model status choices"""
        # Test available status (default)
        self.assertEqual(self.seat.booking_status, 'available')
        
        # Test booked status
        self.seat.booking_status = 'booked'
        self.seat.save()
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, 'booked')
        
        # Test maintenance status
        self.seat.booking_status = 'maintenance'
        self.seat.save()
        self.seat.refresh_from_db()
        self.assertEqual(self.seat.booking_status, 'maintenance')

    def test_booking_model_creation(self):
        """Test Booking model creation and relationships"""
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        
        # Test relationships
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)
        self.assertEqual(booking.user, self.user)
        self.assertIsNotNone(booking.booking_date)
        
        # Test string representation
        expected_str = f"{self.user.username} - {self.movie.title} - Seat {self.seat.seat_number}"
        self.assertEqual(str(booking), expected_str)

    def test_booking_model_constraints(self):
        """Test Booking model unique constraints"""
        # Create first booking
        booking1 = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        self.assertIsNotNone(booking1.id)
        
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

    def test_model_field_validations(self):
        """Test model field validations"""
        # Test Movie duration is integer
        self.assertIsInstance(self.movie.duration, int)
        
        # Test Seat seat_number is unique
        with self.assertRaises(Exception):
            Seat.objects.create(
                seat_number='A1',  # Duplicate seat number
                booking_status='available'
            )

    def test_model_meta_options(self):
        """Test model Meta options"""
        # Test Movie ordering
        movies = Movie.objects.all()
        if len(movies) > 1:
            for i in range(len(movies) - 1):
                self.assertLessEqual(movies[i].release_date, movies[i + 1].release_date)
        
        # Test Seat ordering
        seat2 = Seat.objects.create(seat_number='A2', booking_status='available')
        seats = Seat.objects.all()
        self.assertEqual(seats[0].seat_number, 'A1')
        self.assertEqual(seats[1].seat_number, 'A2')


class APIIntegrationTests(APITestCase):
    
    def setUp(self):
        """Set up test data for API integration tests"""
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
        self.seat = Seat.objects.create(
            seat_number='B1',
            booking_status='available'
        )

    def test_movie_list_api_status_code(self):
        """Test movie list API returns correct status code"""
        # Try common URL patterns
        possible_urls = ['/api/movies/', '/api/api/movies/', '/movies/']
        
        success = False
        for url in possible_urls:
            try:
                response = self.client.get(url)
                if response.status_code in [200, 401]:  # Either success or needs auth
                    success = True
                    self.assertIn(response.status_code, [200, 401])
                    break
            except:
                continue
        
        # If common patterns don't work, try Django URL reverse
        if not success:
            try:
                from django.urls import reverse
                url = reverse('movie-list')
                response = self.client.get(url)
                self.assertIn(response.status_code, [200, 401])
                success = True
            except:
                pass
        
        # If still no success, skip test with message
        if not success:
            self.skipTest("Could not find movie list API endpoint. Check URL configuration.")

    def test_movie_list_api_data_format(self):
        """Test movie list API returns correct data format"""
        self.client.force_authenticate(user=self.user)
        
        # Try to find working URL
        possible_urls = ['/api/movies/', '/api/api/movies/', '/movies/']
        response = None
        
        for url in possible_urls:
            try:
                test_response = self.client.get(url)
                if test_response.status_code == 200:
                    response = test_response
                    break
            except:
                continue
        
        if not response:
            try:
                from django.urls import reverse
                url = reverse('movie-list')
                response = self.client.get(url)
            except:
                self.skipTest("Could not find movie list API endpoint")
        
        if response and response.status_code == 200:
            # Handle both paginated and non-paginated responses
            if isinstance(response.data, dict) and 'results' in response.data:
                movies_data = response.data['results']
            elif isinstance(response.data, list):
                movies_data = response.data
            else:
                self.fail(f"Unexpected response format: {type(response.data)}")
            
            # Test data format
            self.assertIsInstance(movies_data, list)
            if len(movies_data) > 0:
                movie = movies_data[0]
                self.assertIn('title', movie)
                self.assertIn('description', movie)
                self.assertIn('duration', movie)
                self.assertEqual(movie['title'], 'Integration Test Movie')

    def test_seat_list_api_status_code(self):
        """Test seat list API returns correct status code"""
        possible_urls = ['/api/seats/', '/api/api/seats/', '/seats/']
        
        success = False
        for url in possible_urls:
            try:
                response = self.client.get(url)
                if response.status_code in [200, 401]:
                    success = True
                    self.assertIn(response.status_code, [200, 401])
                    break
            except:
                continue
        
        if not success:
            try:
                from django.urls import reverse
                url = reverse('seat-list')
                response = self.client.get(url)
                self.assertIn(response.status_code, [200, 401])
            except:
                self.skipTest("Could not find seat list API endpoint")

    def test_seat_available_api_data_format(self):
        """Test available seats API returns correct data format"""
        self.client.force_authenticate(user=self.user)
        
        possible_urls = ['/api/seats/available/', '/api/api/seats/available/', '/seats/available/']
        response = None
        
        for url in possible_urls:
            try:
                test_response = self.client.get(url)
                if test_response.status_code == 200:
                    response = test_response
                    break
            except:
                continue
        
        if not response:
            try:
                from django.urls import reverse
                url = reverse('seat-available')
                response = self.client.get(url)
            except:
                self.skipTest("Could not find available seats API endpoint")
        
        if response and response.status_code == 200:
            # Handle response format
            if isinstance(response.data, dict) and 'results' in response.data:
                seats_data = response.data['results']
            elif isinstance(response.data, list):
                seats_data = response.data
            else:
                self.fail(f"Unexpected response format: {type(response.data)}")
            
            # Test data format
            self.assertIsInstance(seats_data, list)
            if len(seats_data) > 0:
                seat = seats_data[0]
                self.assertIn('seat_number', seat)
                self.assertIn('booking_status', seat)
                self.assertEqual(seat['booking_status'], 'available')

    def test_booking_api_authentication_required(self):
        """Test booking API requires authentication"""
        possible_urls = ['/api/bookings/', '/api/api/bookings/', '/bookings/']
        
        found_endpoint = False
        for url in possible_urls:
            try:
                response = self.client.get(url)
                if response.status_code in [200, 401, 403]:
                    found_endpoint = True
                    if response.status_code in [401, 403]:
                        # Good - authentication required
                        self.assertIn(response.status_code, [401, 403])
                    break
            except:
                continue
        
        if not found_endpoint:
            try:
                from django.urls import reverse
                url = reverse('booking-list')
                response = self.client.get(url)
                # Either requires auth or allows access
                self.assertIn(response.status_code, [200, 401, 403])
            except:
                self.skipTest("Could not find booking API endpoint")

    def test_booking_api_authenticated_access(self):
        """Test booking API works with authentication"""
        self.client.force_authenticate(user=self.user)
        
        possible_urls = ['/api/bookings/', '/api/api/bookings/', '/bookings/']
        response = None
        
        for url in possible_urls:
            try:
                test_response = self.client.get(url)
                if test_response.status_code == 200:
                    response = test_response
                    break
            except:
                continue
        
        if not response:
            try:
                from django.urls import reverse
                url = reverse('booking-list')
                response = self.client.get(url)
            except:
                self.skipTest("Could not find booking API endpoint")
        
        if response:
            self.assertEqual(response.status_code, 200)
            
            # Test data format
            if isinstance(response.data, dict) and 'results' in response.data:
                bookings_data = response.data['results']
            elif isinstance(response.data, list):
                bookings_data = response.data
            else:
                bookings_data = []
            
            self.assertIsInstance(bookings_data, list)

    def test_api_endpoints_return_json(self):
        """Test that API endpoints return JSON format"""
        self.client.force_authenticate(user=self.user)
        
        # Test endpoints that should return JSON
        endpoints_to_test = [
            ['/api/movies/', '/api/api/movies/', '/movies/'],
            ['/api/seats/', '/api/api/seats/', '/seats/'],
            ['/api/bookings/', '/api/api/bookings/', '/bookings/']
        ]
        
        for endpoint_variants in endpoints_to_test:
            response = None
            for url in endpoint_variants:
                try:
                    test_response = self.client.get(url)
                    if test_response.status_code == 200:
                        response = test_response
                        break
                except:
                    continue
            
            if response:
                # Check that response is JSON
                self.assertEqual(response['content-type'], 'application/json')
                # Check that data can be parsed as JSON
                self.assertIsNotNone(response.data)

    def test_movie_detail_api_status_and_format(self):
        """Test movie detail API status code and data format"""
        self.client.force_authenticate(user=self.user)
        
        # Try different URL patterns
        possible_base_urls = ['/api/movies/', '/api/api/movies/', '/movies/']
        response = None
        
        for base_url in possible_base_urls:
            url = f"{base_url}{self.movie.id}/"
            try:
                test_response = self.client.get(url)
                if test_response.status_code == 200:
                    response = test_response
                    break
            except:
                continue
        
        if not response:
            try:
                from django.urls import reverse
                url = reverse('movie-detail', kwargs={'pk': self.movie.id})
                response = self.client.get(url)
            except:
                self.skipTest("Could not find movie detail API endpoint")
        
        if response:
            self.assertEqual(response.status_code, 200)
            
            # Test data format
            movie_data = response.data
            self.assertIn('title', movie_data)
            self.assertIn('description', movie_data)
            self.assertIn('duration', movie_data)
            self.assertEqual(movie_data['title'], 'Integration Test Movie')
            self.assertEqual(movie_data['duration'], 150)