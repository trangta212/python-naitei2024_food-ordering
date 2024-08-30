from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import add_review, ResOrderView, dashboard
from app.views import activate
from app import views


class TestUrls(SimpleTestCase):
    
    def test_addreview_url_resolved(self):
        url = reverse('app:add-review', args=['1'])
        self.assertEqual(resolve(url).func, add_review)

    def test_dashboard_url_resolved(self):
        url = reverse('app:dashboard')
        self.assertEqual(resolve(url).func, dashboard)

    def test_res_order_url_resolves_to_res_order_view(self):
        url = reverse('app:res_order')
        self.assertEqual(resolve(url).func.view_class, ResOrderView)

    def test_activate_url_resolves(self):
        url = reverse('app:activate', kwargs={'uidb64': 'test-uidb64', 'token': 'test-token'})
        self.assertEqual(resolve(url).func, activate)
    def test_forgot_password_url_resolves(self):
        url = reverse('app:forgot_password')
        self.assertEqual(resolve(url).func, views.forgot_password)

    def test_send_otp_url_resolves(self):
        url = reverse('app:send_otp')
        self.assertEqual(resolve(url).func, views.send_otp)

    def test_enter_otp_url_resolves(self):
        url = reverse('app:enter_otp')
        self.assertEqual(resolve(url).func, views.enter_otp)

    def test_password_reset_url_resolves(self):
        url = reverse('app:password_reset')
        self.assertEqual(resolve(url).func, views.password_reset)
