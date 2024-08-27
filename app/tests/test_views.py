from django.test import TestCase, Client
from django.urls import reverse
from app.models import MenuItem, Profile, Review, User, Restaurant

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )
        self.profile = Profile.objects.create(user=self.user)
        self.restaurant = Restaurant.objects.create(
            restaurant_id=1,
            profile = self.profile
        )
        self.item = MenuItem.objects.create(
            restaurant=self.restaurant,
            name='Test Item',
            description='Test Item Description',
            price=10.00,
            quantity=100
        )
        
        self.client.login(email='testuser@example.com', password='password123')
        self.addreview_url = reverse('app:add-review', args=[self.item.item_id])

    def test_addreview_POST(self):
        response = self.client.post(self.addreview_url, {
            'rating': 5,
            'comment': 'Great dish!'
        })
        self.assertTrue(response.json().get('bool'))
        review = Review.objects.get(item=self.item)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great dish!')

    def test_add_review_duplicate(self):
        Review.objects.create(user=self.profile, item=self.item, rating=5, comment='First review')
        
        response = self.client.post(self.addreview_url, {
            'rating': 4,
            'comment': 'Second review attempt'
        })

        self.assertFalse(response.json().get('bool'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'You have already submitted a review for this item.')

        reviews_count = Review.objects.filter(item=self.item, user=self.profile).count()
        self.assertEqual(reviews_count, 1)
