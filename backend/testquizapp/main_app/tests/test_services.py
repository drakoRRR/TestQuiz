from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from main_app.models import TestQuiz
from main_app.services import get_ids_to_search

class SearchTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.test1 = TestQuiz.objects.create(
            user=self.user,
            name='How good you are',
            description='Test description',
            complexity=7
        )
        self.test2 = TestQuiz.objects.create(
            user=self.user,
            name='Are you good enough to be a programmer',
            description='Test description',
            complexity=4
        )
        self.test3 = TestQuiz.objects.create(
            user=self.user,
            name='Is it sunny today ?',
            description='Test description',
            complexity=4
        )

    def test_common_search(self):
        """Test elasticsearch search by search queries."""

        search_query = 'are you'
        ids = get_ids_to_search(search_query)
        self.assertEquals(sorted(ids, reverse=True), sorted([self.test2.id, self.test1.id], reverse=True))
        self.assertNotEquals(sorted(ids, reverse=True), sorted([self.test3.id], reverse=True))

        search_query = 'is it'
        ids = get_ids_to_search(search_query)
        self.assertEquals(sorted(ids, reverse=True), sorted([self.test3.id], reverse=True))
        self.assertNotEquals(sorted(ids, reverse=True), sorted([self.test2.id, self.test1.id], reverse=True))

    def test_search_by_full_name(self):
        """Test elasticsearch search by full search queries."""

        search_query = self.test1.name
        ids = get_ids_to_search(search_query)
        self.assertEquals(sorted(ids, reverse=True), sorted([self.test1.id, self.test2.id], reverse=True))
        self.assertNotEquals(sorted(ids, reverse=True), sorted([self.test3.id, self.test2.id], reverse=True))
