from django.test import TestCase

# scraper Module
from models import user

# Create your tests here.
if __name__ == "__main__":
    # インスタンス生成
    model = user()
    model.getFollowers()
    