from django.db import models
import tweepy
import urllib.request
import re
import copy
import time

# Create your models here.
API_KEY='RdxefpHsrHg1h4ijekZ2lKitJ'
API_KEY_SECRET='feNXoBBFE0sGgxHr9nGcyb9dQabHszdrQL70R6ncu7LhPA9PYj'
API_TOKEN='1144832203748102144-A0Wil7DdPpws8uOwUhSdZJAHWYgf2T'
API_TOKEN_SECRET='EtQaNG0yg0FkN5RNp3Ad744GW7cwNQsJhZlmj3ONc2iQX'

# TwitterAPIの認証
class MyTweets(models.Model):
    tweet_id                    = models.BigIntegerField(null=False,default=0)
    tweet_string                = models.CharField(max_length=280)
    bot_retweet_cnt             = models.IntegerField(null=True,default=0)
    reply_to_id                 = models.BigIntegerField(null=True)

class MyTweetsManager(models.Manager):
    # API認証    
    def authTwitterAPI(self):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(API_TOKEN, API_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    # コンストラクタ
    def __init__(self, account_name='feivs2019'):
        self.authTwitterAPI()
        self.account_name = account_name

    # ツイートの取得とモデルの更新
    def retweetMytweet(self):
        model_data = {}
        # 自分のツイートIDのリストを取得 [API statuses/home_timeline 15]
        mytweets = self.api.user_timeline(id=self.account_name, count=100)
        for mytweet in mytweets :
            model_data = {'tweet_id': mytweet.id, 'tweet_string': mytweet.text , 'reply_to_id': mytweet.in_reply_to_status_id}
            try:
                if MyTweets.objects.filter(tweet_id=mytweet.id).update(**model_data) == 0:
                    MyTweets.objects.filter(tweet_id=mytweet.id).create(**model_data)
            except :
                import traceback; traceback.print_exc()
                pass
        # 除外ワードのないツイートかつBotリツイート数が最少の1件を取得する
        exclude_word = ''
        retweet_id = MyTweets.objects.exclude(tweet_string=exclude_word).filter(reply_to_id__isnull=True).order_by('bot_retweet_cnt','tweet_id').first()
        #import pdb;pdb.set_trace()
        self.api.retweet(retweet_id.tweet_id)

class Users(models.Model):
    user_id                     = models.CharField(max_length=128, null=True)
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
    follow_flg                  = models.BooleanField(default=False)
    follower_flg                = models.BooleanField(default=False)
    cmn_follow_cnt              = models.IntegerField(null=True)
    cmn_followers_cnt           = models.IntegerField(null=True)
    statuses_count              = models.IntegerField(null=True)

class UsersManager(models.Manager):
    # 共通のフォロワーの抽出
    def extractCommonAccount(self, user_info, my_followers_copy):
        my_followers   = list(my_followers_copy)
        user_followers = list(tweepy.Cursor(self.api.followers_ids, id=user_info.screen_name, cursor=-1).items())
        return set(my_followers) & set(user_followers)

    # 特定のユーザに対してリプライした数の取得
    def extractStaticReply(self, tweet_id_list, user_id):
        statics = 0
        for tweet_id in tweet_id_list:
            reply_to_id = tweet_id.in_reply_to_user_id_str
            if reply_to_id == user_id:
                statics = statics + 1
        return statics

    # ツイートに対していいねしたアカウントのリストを取得
    def getUserIDList(self,tweet_id):
        time.sleep(1)
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
        for tweet_id in tweet_id_list:
            favoriters = self.getUserIDList(tweet_id=tweet_id.id_str) # 最大100件
            for favoriter in favoriters:
                if str(favoriter) not in statics:
                    statics[str(favoriter)] = 1
                else:
                    statics[str(favoriter)] = statics[str(favoriter)] + 1
        return statics

    # リツイート統計値の取得
    def extractStaticRetweet(self, tweet_id_list):
        statics = {}
        for tweet_id in tweet_id_list:
            retweeters = self.api.retweets(id=tweet_id.id_str) # 最大100件
            for retweeter in retweeters:
                if retweeter.user.id_str not in statics:
                    statics[retweeter.user.id_str] = 1
                else:
                    statics[retweeter.user.id_str] = statics[retweeter.user.id_str] + 1
        return statics

    # 基本情報の取得
    def extractBaseInfo(self, user_model_data, user_info):
        user_model_data['user_id']         = user_info.id_str
        user_model_data['name']            = user_info.name
        user_model_data['screen_name']     = user_info.screen_name
        user_model_data['description']     = user_info.description
        user_model_data['follows_cnt']     = user_info.friends_count
        user_model_data['followers_cnt']   = user_info.followers_count
        if self.get_flg:
            user_model_data['follower_flg']    = True
        else:
            user_model_data['follow_flg']    = True
        user_model_data['listed_cnt']      = user_info.listed_count
        user_model_data['statuses_count']  = user_info.statuses_count

    # ユーザに関する情報の取得
    # get_flg  True: follower  , False: friend
    def getUsers(self, cursor, user_model_data, get_flg):
        self.get_flg = get_flg
        # [API users/show 900] フォロワー情報の取得
        if get_flg:
            self.my_users = tweepy.Cursor(self.api.followers_ids, id=self.account_name, cursor=cursor).pages(1)
        else:
            self.my_users = tweepy.Cursor(self.api.friends_ids, id=self.account_name, cursor=cursor).pages(1)
        my_users = copy.deepcopy(self.my_users)
        # 各ユーザの基本情報を取得
        for my_user in my_users.next():
            try:
                # [API users/show 900] アカウント情報の取得
                user_info = self.api.get_user(my_user)
                print(user_info.id_str)
                tmp_dict = {}
                # 基本情報の取得
                self.extractBaseInfo(tmp_dict, user_info)
                # 共通アカウント統計値の取得
                # tmp_dict['cmn_followers_cnt'] = len(self.extractCommonAccount(user_info, copy.deepcopy(self.my_users)))
                user_model_data.append(tmp_dict)
                # break
            except tweepy.error.TweepError as e:
                print(e.reason)
                pass
        return my_users.next_cursor

    # API認証    
    def authTwitterAPI(self):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(API_TOKEN, API_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    # データ正規化    
    def normalizeStatics(self, user_model_data, tmp_dict, my_users):
        for my_user in my_users.next():
            user_model = {} # 各ユーザのデータ格納用
            my_user = str(my_user)
            # いいね正規化
            if my_user in tmp_dict['statics_favorite']:
                user_model['favourites_cnt_for_me'] = tmp_dict['statics_favorite'][my_user]
            if my_user in tmp_dict['statics_retweet']:
                user_model['retweets_cnt_for_me'] = tmp_dict['statics_retweet'][my_user]
            if my_user in tmp_dict['statics_reply']:
                user_model['my_replies_cnt'] = tmp_dict['statics_reply'][my_user]
            user_model_data[my_user] = user_model

    # 統計に関する情報の取得    
    def getUsersStatics(self, user_model_data):
        tmp_dict = {}
        # 自分のツイートIDのリストを取得 [API statuses/home_timeline 15]  100件
        tweet_id_list = self.api.user_timeline(id=self.account_name, count=50)
        # 自分のツイートに対してのリツイートの統計 [API発行 statuses/retweeters/ids 300]
        tmp_dict['statics_retweet'] = self.extractStaticRetweet(tweet_id_list)
        # 自分のツイートに対してのいいねの統計
        tmp_dict['statics_favorite'] = self.extractStaticFavorite(tweet_id_list)
        # 自分がリプライした数の取得
        my_users = copy.deepcopy(self.my_users)
        tmp_dict['statics_reply'] = {}
        for my_user in my_users.next():
            reply_value = self.extractStaticReply(tweet_id_list, str(my_user))
            if reply_value != 0:
                tmp_dict['statics_reply'][str(my_user)] = reply_value
        # データ正規化
        self.normalizeStatics(user_model_data, tmp_dict, copy.deepcopy(self.my_users))


    # コンストラクタ
    def __init__(self, account_name='feivs2019'):
        self.authTwitterAPI()
        self.account_name = account_name
