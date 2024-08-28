from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import add_review, dashboard, ResOrderView

class TestUrls(SimpleTestCase):
    
    def test_addreview_url_resolved(self):
        url = reverse('app:add-review', args=['1'])
        self.assertEquals(resolve(url).func, add_review)

    def test_dashboard_url_resolved(self):
        url = reverse('app:dashboard')
        self.assertEquals(resolve(url).func, dashboard)

    def test_res_order_url_resolves_to_res_order_view(self):
        url = reverse('app:res_order')
        self.assertEqual(resolve(url).func.view_class, ResOrderView)
