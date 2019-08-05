# from django.test import TestCase
from unittest import TestCase
from unittest import mock
from .models import  UsersManager
from . import views
import tweepy
from django.test import Client

'''--------------------------
    ダミークラス
--------------------------'''
class DummyTweet():
    def __init__(self, value):
        self.id = value
        self.id_str = str(value)
        self.name = 'DummyTweet'
        self.source = 'DummyTweet'
        self.text = 'This is DummyTweet'
        self.in_reply_to_status_id = 1
        self.in_reply_to_status_id_str = '0'
        self.in_reply_to_user_id = 10
        self.in_reply_to_user_id_str = '10'
        self.in_reply_to_screen_name = 'DummyUser'
        self.user = DummyUser(1)
        self.quoted_status_id = 2
        self.quoted_status_id_str = '2'
        self.is_quote_status = True
        self.reply_count = 10
        self.retweet_count = 10
        self.favorite_count = 10
        self.entities = {
            "hashtags":['Dummyhashtag']
            , "urls":['Dummyurl']
            , "user_mentions":[]
            ,"media":[]
            ,"symbols":[]
            , "polls":[]
        }
        self.favorited = True
        self.retweeted = True
        
class DummyUser():
    def __init__(self, value):
        self.id = value
        self.id_str = str(value)
        self.name = 'DummyUser'
        self.screen_name = 'DummyUser'
        self.description = 'This is DummyTweet'
        self.friends_count = 10
        self.followers_count = 10
        self.listed_count = 10
        self.statuses_count = 10

'''--------------------------
    ダミーメソッド
--------------------------'''
def dummyReturnList1(self, id=0):
    return [id for id in range(3)]

def dummyReturnList2(self, id=0):
    return [id for id in range(2,4)]

def dummyReturnTrue(self, id=0):
    return True

def dummyReturnTweets(self, id=0, count=0):
    return [DummyTweet(value) for value in range(2,4)]

def dummyReturnTweet(self, id=0, count=0):
    return DummyTweet(1)

def dummyReturnUsers(self, id=0, count=0):
    return [DummyUser(value) for value in range(2,4)]

def dummyReturnUser(self, user_id=1, id=0, count=0):
    return DummyUser(user_id)

'''--------------------------
    テストケースクラス
--------------------------'''
class TestLearnManager(TestCase):
    pass

'''--------------------------
    テストケースクラス
--------------------------'''
class TestViews(TestCase):
    @mock.patch("feivs2019AccountManager.models.MyTweetsManager.authTwitterAPI", dummyReturnTrue)
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self,*args,**kwargs)
        self.client = Client()

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnTweets)
    def test_Case1_01_learningView_follow_relearn(self):
        response = self.client.get('/learn/learning/?user=follow&relearn=True')
        self.assertEqual(response.status_code, 200)

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnTweets)
    def test_Case1_02_learningView_follow_norelearn(self):
        response = self.client.get('/learn/learning/?user=follow&relearn=False')
        self.assertEqual(response.status_code, 200)

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnTweets)
    def test_Case1_03_learningView_friend_relearn(self):
        response = self.client.get('/learn/learning/?user=friend&relearn=True')
        self.assertEqual(response.status_code, 200)

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnTweets)
    def test_Case1_04_learningView_friend_norelearn(self):
        response = self.client.get('/learn/learning/?user=friend&relearn=False')
        self.assertEqual(response.status_code, 200)


