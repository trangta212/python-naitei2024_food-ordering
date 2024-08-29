from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from app.models import (
    MenuItem,
    Order,
    Payment,
    Profile,
    Review,
    User,
    Restaurant,
    Order,
    Payment,
    OrderItem,
)
from django.utils.translation import gettext_lazy as _
import json
from django.core import mail
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from app.tokens import account_activation_token  

class AddReviewTestCase(TestCase):
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
        review = Review.objects.get(item=self.item)

        self.assertTrue(response.json().get("bool"))
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
        reviews_count = Review.objects.filter(
            item=self.item, user=self.profile
        ).count()

        self.assertFalse(response.json().get("bool"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json().get("error"),
            "You have already submitted a review for this item.",
        )
        self.assertEqual(reviews_count, 1)


class DashboardTestCase(TestCase):
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
        self.client.login(email="testuser@example.com", password="password123")
        MenuItem.objects.create(
            restaurant=self.restaurant, name="Item 1", price=10
        )
        MenuItem.objects.create(
            restaurant=self.restaurant, name="Item 2", price=15
        )
        for i in range(5):
            payment = Payment.objects.create(
                payment_id=i, payment_date=timezone.now(), amount=50
            )
            order = Order.objects.create(
                user=self.profile,
                restaurant=self.restaurant,
                total_price=50,
                payment=payment,
            )

    def test_dashboard_view(self):
        response = self.client.get(reverse("app:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurant/dashboard.html")
        self.assertEqual(response.context["total_revenue"], 250)
        self.assertEqual(response.context["menu_item"], 2)
        self.assertEqual(response.context["total_order"], 5)
        self.assertEqual(len(response.context["recent_orders"]), 5)


class ResOrderViewTestCase(TestCase):
    def setUp(self):
        self.user_restaurant = User.objects.create_user(
            username="restaurant_user",
            password="password123",
            email="restaurant@example.com",
            role="Restaurant",
        )
        self.profile_restaurant = Profile.objects.create(
            user=self.user_restaurant,
            name="Restaurant User",
            email="restaurant@example.com",
            phone_number="1234567890",
            address="123 Restaurant St",
            profile_type="Restaurant",
        )
        self.restaurant = Restaurant.objects.create(
            profile=self.profile_restaurant,
            image_url="http://example.com/image.jpg",
            opening_hours={},
        )

        self.payment = Payment.objects.create(
            payment_id="pay_123456789",
            payment_date="2024-08-27T12:00:00Z",
            amount=100.00,
            method="Credit Card",
        )

        self.order = Order.objects.create(
            user=self.profile_restaurant,
            restaurant=self.restaurant,
            total_price=100.00,
            status="Pending",
            payment=self.payment,
        )

        self.user_non_restaurant = User.objects.create_user(
            username="non_restaurant_user",
            password="password123",
            email="non_restaurant@example.com",
        )
        self.profile_non_restaurant = Profile.objects.create(
            user=self.user_non_restaurant,
            name="Non-Restaurant User",
            email="non_restaurant@example.com",
            phone_number="0987654321",
            address="456 Non-Restaurant Ave",
            profile_type="Customer",
        )

        self.client = Client()

    def test_res_order_view_as_restaurant(self):
        self.client.login(
            username="restaurant@example.com", password="password123"
        )
        response = self.client.get(reverse("app:res_order"))
        self.assertEqual(response.status_code, 200)

    def test_res_order_view_as_non_restaurant(self):
        self.client.login(
            username="non_restaurant_user@example.com", password="password123"
        )
        response = self.client.get(reverse("app:res_order"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("app:res_order")}'
        )

    def test_res_order_view_empty_queryset(self):
        self.client.login(
            username="restaurant@example.com", password="password123"
        )
        self.order.delete()
        response = self.client.get(reverse("app:res_order"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Orders: 0")


class ResOrderDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            email="user@example.com", password="password", username="user"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            name="User Profile",
            email="user@example.com",
            phone_number="1234567890",
            address="123 Street",
            profile_type="Type",
        )

        self.restaurant_user = User.objects.create_user(
            email="restaurant@example.com",
            password="password",
            username="restaurant",
        )
        self.restaurant_profile = Profile.objects.create(
            user=self.restaurant_user,
            name="Restaurant Owner",
            email="restaurant@example.com",
            phone_number="0987654321",
            address="456 Avenue",
            profile_type="Restaurant",
        )
        self.restaurant = Restaurant.objects.create(
            profile=self.restaurant_profile
        )
        self.item = MenuItem.objects.create(
            name="Item", price=10.00, restaurant=self.restaurant
        )

        self.payment = Payment.objects.create(
            payment_id="PAY123",
            payment_date=timezone.now(),
            amount=10.00,
            method="Credit Card",
        )

        self.order = Order.objects.create(
            user=self.profile,
            restaurant=self.restaurant,
            total_price=10.00,
            status="Pending",
            payment=self.payment,
        )
        self.order_item = OrderItem.objects.create(
            order=self.order, item=self.item, quantity=1, price=10.00
        )

        self.client.login(email="user@example.com", password="password")

    def test_order_detail_view_success(self):
        self.client.logout()
        self.client.login(email="restaurant@example.com", password="password")
        response = self.client.get(
            reverse(
                "app:res_order_detail",
                kwargs={"order_id": self.order.order_id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.item.name)
        self.assertContains(response, "Pending")

    def test_order_detail_view_permission_denied(self):
        self.client.logout()
        self.client.login(email="user@example.com", password="password")
        response = self.client.get(
            reverse(
                "app:res_order_detail",
                kwargs={"order_id": self.order.order_id},
            )
        )
        self.assertEqual(response.status_code, 403)


class ChangeStatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.restaurant_user = User.objects.create_user(
            email="restaurant@example.com",
            password="restaurantpass",
            username="restaurant_user",
            role="Restaurant",
        )
        self.regular_user = User.objects.create_user(
            email="user@example.com",
            password="userpass",
            username="regular_user",
        )
        self.profile = Profile.objects.create(
            user=self.restaurant_user,
            name="Restaurant Owner",
            email="restaurant@example.com",
            phone_number="123456789",
            address="123 Restaurant St",
            profile_type="Restaurant",
        )
        self.restaurant = Restaurant.objects.create(
            profile=self.profile,
            image_url="http://example.com/image.jpg",
            opening_hours={},
        )
        self.payment = Payment.objects.create(
            payment_id="pay123",
            payment_date="2024-08-28T18:08:38Z",
            amount=10.00,
            method="Credit Card",
        )
        self.order = Order.objects.create(
            user=self.profile,
            restaurant=self.restaurant,
            total_price=10.00,
            status="Pending",
            payment=self.payment,
        )

    def test_change_status_view_permission_denied_for_non_restaurant_user(
        self,
    ):
        self.client.login(email="user@example.com", password="userpass")
        response = self.client.post(
            reverse("app:change_status"),
            json.dumps(
                {"order_id": self.order.order_id, "status": "Delivered"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"error": _("You are not authorized to view this page.")},
        )

    def test_change_status_view_permission_denied_for_wrong_restaurant(self):
        self.client.login(email="user@example.com", password="userpass")
        response = self.client.post(
            reverse("app:change_status"),
            json.dumps(
                {"order_id": self.order.order_id, "status": "Delivered"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"error": _("You are not authorized to view this page.")},
        )

    def test_change_status_view_success(self):
        self.client.login(
            username="restaurant@example.com", password="restaurantpass"
        )
        response = self.client.post(
            reverse('app:change_status'),
            json.dumps(
                {"order_id": self.order.order_id, "status": "Delivered"}
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "order_id": self.order.order_id,
                "success": True,
                "status": _("Order has been updated successfully"),
                "order_status": "Delivered",
            },
        )

User = get_user_model()

class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword', is_active=True)

    def test_enter_otp_incorrect(self):
        self.client.login(username='testuser@example.com', password='securepassword')
        session = self.client.session
        session['email'] = self.user.email
        session.save()
        response = self.client.post(reverse('app:enter_otp'), {
            'otp': 'incorrect_otp'
        })
        print(response.content.decode()) 
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'Invalid OTP')

    def test_password_reset_current_password(self):
        self.client.login(username='testuser@example.com', password='securepassword')
        session = self.client.session
        session['email'] = self.user.email
        session.save()
        response = self.client.post(reverse('app:password_reset'), {
            'new_password': 'securepassword',
            'confirm_new_password': 'securepassword'
        })
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'This password is already used')

    def test_send_otp_email_not_exists(self):
        response = self.client.post(reverse('app:send_otp'), {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, 'Email does not exist')

    def test_password_change_successful(self):
        session = self.client.session
        session['email'] = self.user.email
        session.save()
        response = self.client.post(reverse('app:password_reset'), {
            'new_password': 'newsecurepassword',
            'confirm_new_password': 'newsecurepassword'
        })
        
        self.assertEqual(response.status_code, 302)      
        follow_response = self.client.get(response.url, follow=True)
        print(follow_response.content.decode())

        self.client.logout()
        login_successful = self.client.login(username='testuser@example.com', password='newsecurepassword')
        self.assertTrue(login_successful)
        
class ActivationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword', is_active=False)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activate_success(self):
        response = self.client.get(reverse('app:activate', kwargs={'uidb64': self.uid, 'token': self.token}))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertRedirects(response, reverse('app:index'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Account activated successfully")
        self.assertEqual(messages[0].level_tag, "success")

    def test_activate_invalid_token(self):
        response = self.client.get(reverse('app:activate', kwargs={'uidb64': self.uid, 'token': 'invalid-token'}))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertRedirects(response, reverse('app:index'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Activation link is invalid!")
        self.assertEqual(messages[0].level_tag, "error")

    def test_activate_invalid_uid(self):
        invalid_uid = urlsafe_base64_encode(force_bytes(999))
        response = self.client.get(reverse('app:activate', kwargs={'uidb64': invalid_uid, 'token': self.token}))
        self.assertRedirects(response, reverse('app:index'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "Activation link is invalid!")
        self.assertEqual(messages[0].level_tag, "error")


class ResMenuViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            name="Test Restaurant",
            email="testuser@example.com",
            phone_number="0123456789",
            address="123 Test Street",
            profile_type="Restaurant",
        )
        self.restaurant = Restaurant.objects.create(
            profile=self.profile, image_url="http://example.com/image.jpg"
        )

        self.menu_item1 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Pizza",
            description="Delicious cheese pizza",
            price=10.0,
            rate_avg=4.5,
        )
        self.menu_item2 = MenuItem.objects.create(
            restaurant=self.restaurant,
            name="Burger",
            description="Juicy beef burger",
            price=8.0,
            rate_avg=4.0,
        )

        self.client = Client()

    def test_res_menu_view(self):
        response = self.client.get(
            reverse(
                "app:res_menu",
                kwargs={"restaurant_id": self.restaurant.restaurant_id},
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn("items", response.context)
        self.assertEqual(len(response.context["items"]), 2)
        self.assertIn(self.menu_item1, response.context["items"])
        self.assertIn(self.menu_item2, response.context["items"])

        self.assertIn("restaurant_name", response.context)
        self.assertEqual(
            response.context["restaurant_name"], self.profile.name
        )

    def test_res_menu_view_no_items(self):
        MenuItem.objects.all().delete()
        response = self.client.get(
            reverse(
                "app:res_menu",
                kwargs={"restaurant_id": self.restaurant.restaurant_id},
            )
        )

        self.assertEqual(len(response.context["items"]), 0)
