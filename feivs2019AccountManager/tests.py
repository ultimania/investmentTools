from django.test import TestCase
from unittest import mock
from .models import  UsersManager

'''--------------------------
    ダミークラス
--------------------------'''
class DummyTweet():
    def __init__(self, value):
        self.id = value
        self.id_str = value
        self.name = value
        self.screen_name = value
        self.description = value
        self.friends_count = value
        self.followers_count = value
        self.listed_count = value
        self.statuses_count = value
        self.user = DummyUser(value)

class DummyUser():
    def __init__(self, value):
        self.id = value
        self.id_str = value
        self.name = value
        self.screen_name = value
        self.description = value
        self.friends_count = value
        self.followers_count = value
        self.listed_count = value
        self.statuses_count = value

'''--------------------------
    ダミーメソッド
--------------------------'''
def dummyReturnList(self, id=0):
    return [0]

def dummyReturnTrue(self, id=0):
    return True

def dummyReturnItems(self, id=0, count=0):
    return [DummyTweet(value) for value in range(1)]

def dummyReturnItem(self, id=0, count=0):
    return DummyTweet(1)

class TestUsersManager(TestCase):
    @mock.patch("feivs2019AccountManager.models.UsersManager.authTwitterAPI", dummyReturnTrue)
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self,*args,**kwargs)
        self.usersmanager = UsersManager()

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCreateFavorite', dummyReturnTrue)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnItems)
    @mock.patch('feivs2019AccountManager.models.UsersManager.getUserIDList', dummyReturnList)
    def test_Case1_01_refavorite_ohayousentai(self):
        mode = 'ohayousentai'
        self.assertTrue(self.usersmanager.refavorite(mode=mode))

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorSearch', dummyReturnItems)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCreateFavorite', dummyReturnTrue)
    def test_Case1_02_favorite_progate(self):
        keyword = 'progate'
        self.assertTrue(self.usersmanager.favorite(keyword=keyword))

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorSearch', dummyReturnItems)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCreateFavorite', dummyReturnTrue)
    def test_Case1_03_favorite_studyprogram(self):
        keyword = '#studyprogram'
        self.assertTrue(self.usersmanager.favorite(keyword=keyword))

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiDestroyFriendship', dummyReturnTrue)
    def test_Case1_04_arrangeFollow(self):
        self.usersmanager.arrangeFollow()

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFollowersIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnItem)
    def test_Case1_05_getUsers_follower_diff(self):
        self.usersmanager.getUsers(
            user_flg=True
            , diff_mode=True
        )
    
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFollowersIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnItem)
    def test_Case1_06_getUsers_follower_nodiff(self):
        self.usersmanager.getUsers(
            user_flg=True
            , diff_mode=False
        )

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFriendsIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnItem)
    def test_Case1_07_getUsers_friend_diff(self):
        self.usersmanager.getUsers(
            user_flg=False
            , diff_mode=True
        )

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiCursorFriendsIds', dummyReturnList)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiGetUser', dummyReturnItem)
    def test_Case1_08_getUsers_friend_nodiff(self):
        self.usersmanager.getUsers(
            user_flg=False
            , diff_mode=False
        )

    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiUserTimeline', dummyReturnItems)
    @mock.patch('feivs2019AccountManager.models.UsersManager.myapiRetweets', dummyReturnItems)
    @mock.patch('feivs2019AccountManager.models.UsersManager.getUserIDList', dummyReturnList)
    def test_Case1_09_getUsersStatics(self):
        self.usersmanager.getUsersStatics()
