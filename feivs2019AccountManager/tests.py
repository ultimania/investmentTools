from django.test import TestCase
from unittest import mock
import sys

sys.path.append('/opt/investmentTools/feivs2019AccountManager/')
from models import UsersManager

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

'''--------------------------
    ダミーメソッド
--------------------------'''
def dummyReturnTrue():
    return True

def dummyReturnItems():
    return [DummyTweet(value) for value in range(10)]

class TestUsersManager(TestCase):
    @mock.patch('models.UsersManager.authTwitterAPI', dummyReturnTrue)
    def __init__(self, *args, **kwargs):
        TestCase.__init__(self,*args,**kwargs)
        self.usersmanager = UsersManager()

    @mock.patch('UsersManager.myapiCreateFavorite', dummyReturnTrue)
    @mock.patch('UsersManager.myapiUserTimeline', dummyReturnItems)
    def test_Case1_01_refavorite_ohayousentai(self):
        mode = 'ohayousentai'
        assertTrue(self.usersmanager.refavorite(mode=keyword))

    @mock.patch('UsersManager.myapiCursorSearch', dummyReturnItems)
    @mock.patch('UsersManager.myapiCreateFavorite', dummyReturnTrue)
    def test_Case1_02_favorite_progate(self):
        keyword = 'progate'
        assertTrue(self.usersmanager.favorite(keyword=keyword))

    @mock.patch('UsersManager.myapiCursorSearch', dummyReturnItems)
    @mock.patch('UsersManager.myapiCreateFavorite', dummyReturnTrue)
    def test_Case1_03_favorite_studyprogram(self):
        keyword = '#studyprogram'
        assertTrue(self.usersmanager.favorite(keyword=keyword))

    @mock.patch('UsersManager.myapiDestroyFriendship', dummyReturnTrue)
    def test_Case1_04_arrangeFollow(self):
        model_manager.arrangeFollow()

    @mock.patch('UsersManager.myapiCursorFollowersIds', dummyReturnItems)
    @mock.patch('UsersManager.myapiGetUser', dummyReturnItems)
    def test_Case1_05_getUsers_follower_diff(self):
        model_manager.getUsers(
            user_flg='follower'
            , diff_mode=True
        )
    
    @mock.patch('UsersManager.myapiCursorFollowersIds', dummyReturnItems)
    @mock.patch('UsersManager.myapiGetUser', dummyReturnItems)
    def test_Case1_06_getUsers_follower_nodiff(self):
        model_manager.getUsers(
            user_flg='follower'
            , diff_mode=False
        )

    @mock.patch('UsersManager.myapiCursorFollowersIds', dummyReturnItems)
    @mock.patch('UsersManager.myapiGetUser', dummyReturnItems)
    def test_Case1_07_getUsers_friend_diff(self):
        model_manager.getUsers(
            user_flg='friend'
            , diff_mode=True
        )

    @mock.patch('UsersManager.myapiCursorFollowersIds', dummyReturnItems)
    @mock.patch('UsersManager.myapiGetUser', dummyReturnItems)
    def test_Case1_08_getUsers_friend_nodiff(self):
        model_manager.getUsers(
            user_flg='friend'
            , diff_mode=False
        )
