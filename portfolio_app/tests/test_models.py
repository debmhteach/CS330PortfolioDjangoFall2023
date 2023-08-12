from django.test import TestCase

from portfolio_app.models import Portfolio

# Create your tests here.

class PortfolioModelClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        Portfolio.objects.create(title='my portfolio')

    def test_first_name_label(self):
        author = Portfolio.objects.get(id=1)
        field_label = Portfolio._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    

    def test_get_absolute_url(self):
        author = Portfolio.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/portfolio/1')


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)
