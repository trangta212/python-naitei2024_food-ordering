from django.test import SimpleTestCase

from app.forms import ReviewForm


class TestForm(SimpleTestCase):

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
        self.assertEqual(len(form.errors), 2)       
