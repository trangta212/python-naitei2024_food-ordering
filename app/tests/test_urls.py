from django.test import SimpleTestCase
from django.urls import reverse, resolve
from app.views import add_review

class TestUrls(SimpleTestCase):
    
    def test_addreview_url_resolved(self):
        url = reverse('app:add-review', args=['1'])
        self.assertEquals(resolve(url).func, add_review)
