# from django.test import TestCase
from unittest import TestCase
from unittest import mock
from .models import  UsersManager
import tweepy

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
        self.in_reply_to_status_id_str = '1'
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
def dummyReturnList(self, id=0):
    return [id for id in range(100)]

def dummyReturnTrue(self, id=0):
    return True

def dummyReturnTweets(self, id=0, count=0):
    return [DummyTweet(value) for value in range(5,5)]

def dummyReturnTweet(self, id=0, count=0):
    return DummyTweet(1)

def dummyReturnUsers(self, id=0, count=0):
    return [DummyUser(value) for value in range(5,5)]

def dummyReturnUser(self, id=0, count=0):
    return DummyUser(1)

'''--------------------------
    テストケースクラス
--------------------------'''
class TestUsersManager(TestCase):
    @mock.patch("feivs2019AccountManager.models.UsersManager.authTwitterAPI", dummyReturnTrue)
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self,*args,**kwargs)
        self.usersmanager = UsersManager()

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiDestroyFriendship', dummyReturnTrue)
    def test_Case1_04_arrangeFollow(self):
        self.usersmanager.arrangeFollow()

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFollowersIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnUser)
    def test_Case1_05_getUsers_follower_diff(self):
        self.usersmanager.getUsers(
            user_flg=True
            , diff_mode=True
        )
    
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFollowersIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnUser)
    def test_Case1_06_getUsers_follower_nodiff(self):
        self.usersmanager.getUsers(
            user_flg=True
            , diff_mode=False
        )

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFriendsIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnUser)
    def test_Case1_07_getUsers_friend_diff(self):
        self.usersmanager.getUsers(
            user_flg=False
            , diff_mode=True
        )

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFriendsIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnUser)
    def test_Case1_08_getUsers_friend_nodiff(self):
        self.usersmanager.getUsers(
            user_flg=False
            , diff_mode=False
        )

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnTweets)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiRetweets', dummyReturnTweets)
    @mock.patch('feivs2019AccountManager.models.UsersManager.getUserIDList', dummyReturnList)
    def test_Case1_09_getUsersStatics(self):
        self.usersmanager.getUsersStatics()

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCreateFavorite', dummyReturnTrue)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnTweets)
    @mock.patch('feivs2019AccountManager.models.UsersManager.getUserIDList', dummyReturnList)
    def test_Case1_01_refavorite_ohayousentai(self):
        mode = 'ohayousentai'
        self.assertTrue(self.usersmanager.refavorite(mode=mode))

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorSearch', dummyReturnTweets)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCreateFavorite', dummyReturnTrue)
    def test_Case1_02_favorite_progate(self):
        keyword = 'progate'
        self.assertTrue(self.usersmanager.favorite(keyword=keyword))

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorSearch', dummyReturnTweets)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCreateFavorite', dummyReturnTrue)
    def test_Case1_03_favorite_studyprogram(self):
        keyword = '#studyprogram'
        self.assertTrue(self.usersmanager.favorite(keyword=keyword))

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorSearch', dummyReturnTweets)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCreateFavorite', mock.MagicMock(side_effect=tweepy.error.TweepError('dummy')))
    def test_Case1_10_favorite_Error(self):
        keyword = '#studyprogram'
        self.assertRaises(tweepy.error.TweepError('dummy'), self.usersmanager.favorite(keyword=keyword))
