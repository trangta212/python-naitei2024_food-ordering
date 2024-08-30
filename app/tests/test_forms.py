from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse

from app.forms import MenuItemForm, ReviewForm
from app.models import Category, MenuItem, Profile, Restaurant, User
from django.core.files.uploadedfile import SimpleUploadedFile


class ReviewFormTestCase(SimpleTestCase):

    def test_review_form_valid_data(self):
        form = ReviewForm(data={
            'comment': 'Great dish!',
            'rating': '5'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['comment'], 'Great dish!')
        self.assertEqual(form.cleaned_data['rating'], '5')

    def test_review_form_no_data(self):
        form = ReviewForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)       

class MenuItemFormTestCase(TestCase):
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
        self.category1 = Category.objects.create(category_name='Appetizer', description='Starter dishes')
        self.category2 = Category.objects.create(category_name='Main Course', description='Main dishes')
        self.client = Client()
        self.client.login(username='restaurant@example.com', password='password123')

    def test_form_valid_data(self):
        form_data = {
            'name': 'Test Item',
            'description': 'A delicious test item',
            'price': 12.99,
            'quantity': 5,
            'categories': [self.category1.pk, self.category2.pk],
        }
        image = SimpleUploadedFile('test_image.jpg', b'file_content', content_type='image/jpeg')

        form = MenuItemForm(data=form_data, files={'image_url': image})
        self.assertTrue(form.is_valid())

    def test_form_invalid_price(self):
        form_data = {
            'name': 'Invalid Item',
            'description': 'This should fail',
            'price': -10.00, 
            'quantity': 2,
            'categories': [self.category1.pk]
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_form_invalid_quantity(self):
        form_data = {
            'name': 'Another Invalid Item',
            'description': 'This should also fail',
            'price': 10.00,
            'quantity': -3, 
            'categories': [self.category1.pk]
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_form_required_fields(self):
        form_data = {
            'name': '',  
            'description': '',
            'price': '',
            'quantity': ''
        }
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('quantity', form.errors)

    def test_form_empty_categories(self):
        form_data = {
            'name': 'Item with No Categories',
            'description': 'A test item with no categories',
            'price': 5.99,
            'quantity': 10,
            'categories': []  
        }
        form = MenuItemForm(data=form_data)
        self.assertTrue(form.is_valid())
