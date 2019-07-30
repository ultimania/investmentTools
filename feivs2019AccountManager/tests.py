from django.test import TestCase
from .models import UsersManager()

# Create your tests here.
class TestUsersManager(TestCase)
    def __init__(self):
        self.usermanager = UsersManager()

    def test_favorite(self):
        model_manager.favorite(keyword=keyword)