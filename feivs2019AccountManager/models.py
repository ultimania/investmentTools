from django.db import models
import tweepy
import urllib.request
import re
import copy

# Create your models here.
class Users(models.Model):
    user_id                     = models.CharField(primary_key=True, max_length=128)
    name                        = models.CharField(max_length=128, null=True)
    screen_name                 = models.CharField(max_length=128, null=True)
    description                 = models.CharField(max_length=2048, null=True)
    retweets_cnt_for_me         = models.IntegerField(null=True)
    my_retweets_cnt             = models.IntegerField(null=True)
    favourites_cnt_for_me       = models.IntegerField(null=True)
    my_favourites_cnt           = models.IntegerField(null=True)
    replies_cnt_for_me          = models.IntegerField(null=True)
    my_replies_cnt              = models.IntegerField(null=True)
    last_tweet_date             = models.DateTimeField(null=True)
    follows_cnt                 = models.IntegerField(null=True)
    followers_cnt               = models.IntegerField(null=True)
    likes_cnt                   = models.IntegerField(null=True)
    listed_cnt                  = models.IntegerField(null=True)
    follow_flg                  = models.BooleanField(default=True)
    follower_flg                = models.BooleanField(default=True)
    cmn_follow_cnt              = models.IntegerField(null=True)
    cmn_followers_cnt           = models.IntegerField(null=True)
    statuses_count              = models.IntegerField(null=True)

class UsersManager(models.Manager):
    # 相互関係の取得
    def extractReciprocity(self, user_model_data, user_info, my_screen_name):
        friendship = self.api.show_friendship(source_screen_name=my_screen_name, target_screen_name=user_info.screen_name)
        user_model_data['follow_flg'] = friendship[0].following
        user_model_data['follower_flg'] = friendship[0].followed_by

    # 共通のフォロワーの抽出
    def extractCommonAccount(self, user_info, my_followers_copy):
        my_followers   = list(my_followers_copy)
        user_followers = list(tweepy.Cursor(self.api.followers_ids, id=user_info.screen_name, cursor=-1).items())
        return set(my_followers) & set(user_followers)

    # 特定のユーザに対してリプライした数の取得
    def extractStaticReply(self, tweet_id_list, user_id):
        statics = 0
        for tweet_id in tweet_id_list.next():
            reply_to_id = tweet_id.in_reply_to_user_id_str
            if reply_to_id == user_id:
                statics = statics + 1
        return statics

    # ツイートに対していいねしたアカウントのリストを取得
    def getUserIDList(self,tweet_id):
        sleep(1)
        try:
            json_data = urllib.request.urlopen(url='https://twitter.com/i/activity/favorited_popup?id=' + str(tweet_id)).read().decode("utf-8")
            found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
            unique_ids = list(set([re.findall(r'\d+', match)[0] for match in found_ids]))
            return unique_ids
        except urllib.request.HTTPError:
            return False

    # いいね統計値の取得
    def extractStaticFavorite(self, tweet_id_list):
        statics = {}
        for tweet_id in tweet_id_list.next():
            favoriters = getUserIDList(tweet_id=tweet_id.id_str) # 最大100件
            for favoriter in favoriters:
                if statics[str(favoriter)] is None:
                    statics[str(favoriter)] = 1
                else:
                    statics[str(favoriter)] = statics[str(favoriter)] + 1
        return statics

    # リツイート統計値の取得
    def extractStaticRetweet(self, tweet_id_list):
        statics = {}
        for tweet_id in tweet_id_list.next():
            retweeters = self.api.retweets(id=tweet_id.id_str) # 最大100件
            for retweeter in retweeters:
                if statics[str(retweeter.user.id)] is None:
                    statics[str(retweeter.user.id)] = 1
                else:
                    statics[str(retweeter.user.id)] = statics[str(retweeter.user.id)] + 1
        return statics

    # 基本情報の取得
    def extractBaseInfo(self, user_model_data, user_info):
        user_model_data['user_id']         = user_info.id_str
        user_model_data['name']            = user_info.name
        user_model_data['screen_name']     = user_info.screen_name
        user_model_data['description']     = user_info.description
        user_model_data['follows_cnt']     = user_info.friends_count
        user_model_data['followers_cnt']   = user_info.followers_count
        # user_model_data['favourites_cnt']  = user_info.favourites_count
        user_model_data['listed_cnt']      = user_info.listed_count
        user_model_data['statuses_count']  = user_info.statuses_count

    # TwitterAPIの認証
    def authTwitterAPI(self):
        auth = tweepy.OAuthHandler('RdxefpHsrHg1h4ijekZ2lKitJ', 'feNXoBBFE0sGgxHr9nGcyb9dQabHszdrQL70R6ncu7LhPA9PYj')
        auth.set_access_token('1144832203748102144-A0Wil7DdPpws8uOwUhSdZJAHWYgf2T', 'EtQaNG0yg0FkN5RNp3Ad744GW7cwNQsJhZlmj3ONc2iQX')
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    # フォロワーに関する情報の取得
    def getFollowers(self, cursor, user_model_data):
        self.my_followers = tweepy.Cursor(self.api.followers_ids, id=self.account_name, cursor=cursor).pages(1)
        my_followers = copy.deepcopy(self.my_followers)
        # 各フォロワーの情報を取得・統計してモデルに格納
        for my_follower in my_followers.next():
            try:
                # フォロワーのアカウント情報の取得
                user_info = self.api.get_user(my_follower)
                print(user_info.id_str)
                tmp_dict = {}
                # 基本情報の取得
                self.extractBaseInfo(tmp_dict, user_info)
                # 共通アカウント統計値の取得
                # tmp_dict['cmn_followers_cnt'] = len(self.extractCommonAccount(user_info, copy.deepcopy(self.my_followers)))
                # 相互関係の取得
                # self.extractReciprocity(tmp_dict, user_info, self.account_name)
                user_model_data.append(tmp_dict)
            except tweepy.error.TweepError as e:
                print(e.reason)
                pass
        return my_followers.next_cursor

    # 統計に関する情報の取得    
    def getFollowersStatics(self, rootflg=True):
        # 自分のツイートIDのリストを取得
        tweet_id_list = self.api.user_timeline(id=self.account_name, count=100)
        # 自分のツイートに対してのリツイートの統計
        statics_retweet = extractStaticRetweet(tweet_id_list)
        # 自分のツイートに対してのいいねの統計
        statics_favorite = extractStaticFavorite(tweet_id_list)
        # 自分に対してリプライした数の取得
        followers = tweepy.Cursor(self.api.followers_ids, id=self.account_name, cursor=-1).items()
        for follower in followers.next():
            statics_reply[follower.user_id_str] = extractStaticReply(tweet_id_list, follower.user_id_str)

    def __init__(self, account_name='feivs2019'):
        self.authTwitterAPI()
        self.account_name = account_name
