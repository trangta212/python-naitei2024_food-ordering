from django.test import TestCase

from app.models import MenuItem, Profile, Review, User, Restaurant


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)
        self.restaurant = Restaurant.objects.create(restaurant_id=1, profile=self.profile)
        self.menu_item = MenuItem.objects.create(restaurant=self.restaurant, name="Test Dish", description="Test Description", price=10.0)

    def test_add_review(self):
        review = Review.objects.create(
            user=self.profile,
            item=self.menu_item,
            rating=4,
            comment="Great dish!"
        )

        review_from_db = Review.objects.get(pk=review.review_id)

        self.assertEqual(review_from_db.user, self.profile)
        self.assertEqual(review_from_db.item, self.menu_item)
        self.assertEqual(review_from_db.rating, 4)
        self.assertEqual(review_from_db.comment, "Great dish!")
    
    def test_review_without_comment(self):
        review = Review.objects.create(
            user=self.profile,
            item=self.menu_item,
            rating=5,
            comment=""
        )

        review_from_db = Review.objects.get(pk=review.review_id)
        
        self.assertEqual(review_from_db.comment, "")
