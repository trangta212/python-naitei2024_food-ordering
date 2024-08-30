from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import add_item, add_review, ResOrderView, dashboard, delete_item, manage_item, update_item
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

    def test_manage_item_url_resolved(self):
        url = reverse('app:manage_item')
        self.assertEquals(resolve(url).func, manage_item)
    
    def test_add_item_url_resolved(self):
        url = reverse('app:add_item')
        self.assertEquals(resolve(url).func, add_item)

    def test_delete_item_url_resolved(self):
        url = reverse('app:delete_item', args=['1'])
        self.assertEquals(resolve(url).func, delete_item)
    
    def test_update_item_url_resolved(self):
        url = reverse('app:update_item', args=['1'])
        self.assertEquals(resolve(url).func, update_item)
