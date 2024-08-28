from django.test import TestCase, Client
from django.urls import reverse
from app.models import MenuItem, Profile, Review, User, Restaurant, Order, Payment
from django.utils.translation import gettext_lazy as _

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.restaurant = Restaurant.objects.create(
            restaurant_id=1, profile=self.profile
        )
        self.item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Test Item",
            description="Test Item Description",
            price=10.00,
            quantity=100,
        )

        self.client.login(email="testuser@example.com", password="password123")
        self.addreview_url = reverse(
            "app:add-review", args=[self.item.item_id]
        )

    def test_addreview_POST(self):
        response = self.client.post(
            self.addreview_url, {"rating": 5, "comment": "Great dish!"}
        )
        self.assertTrue(response.json().get("bool"))
        review = Review.objects.get(item=self.item)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great dish!")

    def test_add_review_duplicate(self):
        Review.objects.create(
            user=self.profile, item=self.item, rating=5, comment="First review"
        )

        response = self.client.post(
            self.addreview_url,
            {"rating": 4, "comment": "Second review attempt"},
        )

        self.assertFalse(response.json().get("bool"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get("error"),
            "You have already submitted a review for this item.",
        )

        reviews_count = Review.objects.filter(
            item=self.item, user=self.profile
        ).count()
        self.assertEqual(reviews_count, 1)

class ResOrderViewTestCase(TestCase):
    def setUp(self):
        self.user_restaurant = User.objects.create_user(
            username='restaurant_user',
            password='password123',
            email='restaurant@example.com',
            role='Restaurant',
        )
        self.profile_restaurant = Profile.objects.create(
            user=self.user_restaurant,
            name='Restaurant User',
            email='restaurant@example.com',
            phone_number='1234567890',
            address='123 Restaurant St',
            profile_type='Restaurant'
        )
        self.restaurant = Restaurant.objects.create(
            profile=self.profile_restaurant,
            image_url='http://example.com/image.jpg',
            opening_hours={}
        )

        self.payment = Payment.objects.create(
            payment_id='pay_123456789',
            payment_date='2024-08-27T12:00:00Z',
            amount=100.00,
            method='Credit Card'
        )

        self.order = Order.objects.create(
            user=self.profile_restaurant,
            restaurant=self.restaurant,
            total_price=100.00,
            status='Pending',
            payment=self.payment
        )

        self.user_non_restaurant = User.objects.create_user(
            username='non_restaurant_user',
            password='password123',
            email='non_restaurant@example.com'
        )
        self.profile_non_restaurant = Profile.objects.create(
            user=self.user_non_restaurant,
            name='Non-Restaurant User',
            email='non_restaurant@example.com',
            phone_number='0987654321',
            address='456 Non-Restaurant Ave',
            profile_type='Customer'
        )

        self.client = Client()

    def test_res_order_view_as_restaurant(self):
        self.client.login(username='restaurant@example.com', password='password123')
        response = self.client.get(reverse('app:res_order'))
        self.assertEqual(response.status_code, 200)

    def test_res_order_view_as_non_restaurant(self):
        self.client.login(username='non_restaurant_user@example.com', password='password123')
        response = self.client.get(reverse('app:res_order'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("app:res_order")}')

    def test_res_order_view_empty_queryset(self):
        self.client.login(username='restaurant@example.com', password='password123')
        self.order.delete()
        response = self.client.get(reverse('app:res_order'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Orders: 0')
