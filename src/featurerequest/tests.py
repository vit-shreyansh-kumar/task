from django.test import TestCase
import datetime
from .models import Features, Clients, ProductArea
from .forms import FeatureForm


class FeatureModelTestCase(TestCase):
    """
    Inheriting from django.test.TestCase. it creates a blank database for tests.
    Regardless of whether the tests pass or fail, the test databases are destroyed when all the tests have been executed.
    We can prevent the test databases from being destroyed by using the test --keepdb option
    """
    def setUp(self):
        c1 = Clients.objects.create(name="ClientA", address="Noida", enddate="2019-12-02", status="A")
        p1 = ProductArea.objects.create(name="Billing", description="Billing", status="A")
        f1 = Features.objects.create(title="Test1", description="This is description", client=c1, priority=1,
                                     target_date="2018-12-02", product_area=p1, status="A")
        f2 = Features.objects.create(title="Test2", description="This is description", client=c1, priority=2,
                                     target_date="2018-12-02", product_area=p1, status="A")

    def test_feature_start_date(self):
        f1 = Features.objects.get(title="Test1")
        self.assertEqual(f1.start_date.strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d'))


class FeatureFromTestCase(TestCase):
    def setUp(self):

        self.future_date = datetime.date.today() + datetime.timedelta(days=15)
        self.past_date = datetime.date.today() - datetime.timedelta(days=5)
        self.future_date_str = self.future_date.strftime('%d/%m/%Y')
        self.past_date_str = self.past_date.strftime('%d/%m/%Y')

        self.c2 = Clients.objects.create(name="ClientA", address="Noida", enddate=self.future_date, status="A")
        self.p2 = ProductArea.objects.create(name="Billing", description="Billing", status="A")

    def test_negative_priority(self):
        form = FeatureForm(data={'title': 'This is test title', 'description': 'This is test description',
                                 'client': self.c2.pk, 'priority': '-90', 'target_date': self.future_date,
                                 'product_area': self.p2.pk, 'status': 'A'})
        self.assertFalse(form.is_valid(), msg=form.errors)

    def test_past_targetdate_with_status_active(self):
        form = FeatureForm(data={'title': 'This is test title', 'description': 'This is test description',
                                 'client': '1', 'priority': '1', 'target_date': self.past_date,
                                 'product_area': self.p2.pk, 'status': 'A'})
        self.assertFalse(form.is_valid(), msg=form.errors)

    def test_past_targetdate_with_status_notactive(self):
        form = FeatureForm(data={'title': 'This is test title', 'description': 'This is test description',
                                 'client': '1', 'priority': '1', 'target_date': self.past_date,
                                 'product_area': self.p2.pk, 'status': 'D'})
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_future_targetdate_with_status_active(self):
        form = FeatureForm(data={'title': 'This is test title', 'description': 'This is test description',
                                 'client': self.c2.pk, 'priority': 1, 'target_date': self.future_date,
                                 'product_area': self.p2.pk, 'status': 'A'})
        self.assertTrue(form.is_valid(), msg=form.errors)
