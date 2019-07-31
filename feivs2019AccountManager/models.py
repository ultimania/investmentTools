from django.db import models
import tweepy
import urllib.request
import re
import copy
import time
import traceback

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
    hashtags                    = models.CharField(max_length=280,null=True)
    urls                        = models.CharField(max_length=1024,null=True)
    #created_at                  = models.CharField(max_length=64,null=True)

class MyTweetsManager(models.Manager):
    '''
        TwitterAPI連携用ラッパー
    '''
    # API認証    
    def authTwitterAPI(self):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(API_TOKEN, API_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    # コンストラクタ
    def __init__(self, account_name='feivs2019'):
        self.authTwitterAPI()
        self.account_name = account_name

    # リツイートの実行とツイート情報の更新
    def retweetMytweet(self):
        model_data = {}
        # 自分のツイートIDのリストを取得 [API statuses/home_timeline 15]
        mytweets = self.api.user_timeline(id=self.account_name, count=100)
        for mytweet in mytweets :
            model_data = {
                'tweet_id'      : mytweet.id
                ,'tweet_string' : mytweet.text 
                ,'reply_to_id'  : mytweet.in_reply_to_status_id
                ,'hashtags'     : mytweet.entities['hashtags']
                ,'urls'         : mytweet.entities['urls']
                #,'created_at'   : mytweet.created_at
            }
            try:
                if MyTweets.objects.filter(tweet_id=mytweet.id).update(**model_data) == 0:
                    MyTweets.objects.filter(tweet_id=mytweet.id).create(**model_data)
            except :
                import traceback; traceback.print_exc()
                pass
        # 除外ワードのないツイートかつBotリツイート数が最少の1件を取得する
        exclude_word = 'おはようございます'
        retweet_id = MyTweets.objects.exclude(tweet_string__contains=exclude_word).exclude(reply_to_id__isnull=False).order_by('bot_retweet_cnt','tweet_id').first()
        # Botツイート数をカウントアップする
        MyTweets.objects.filter(tweet_id=retweet_id.tweet_id).update(bot_retweet_cnt=retweet_id.bot_retweet_cnt+1)
        # import pdb;pdb.set_trace()
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
    '''
        TwitterAPI連携用ラッパー
    '''
    def authTwitterAPI(self):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(API_TOKEN, API_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def myapiCreateFavorite(self,tweet_id):
        time.sleep(10)
        return self.api.create_favorite(tweet_id)

    def myapiUserTimeline(self,id, count):
        return self.api.user_timeline(id=id, count=count)

    def myapiDestroyFriendship(self,user_id):
        return self.api.destroy_friendship(user_id)

    def myapiRetweets(self,id):
        return self.api.retweets(id=id)

    def myapiGetUser(self,user_id):
        return self.api.get_user(user_id)

    def myapiCursorSearch(self):
        return tweepy.Cursor(self.api.search, q=keyword, count=10, tweet_mode='extended').items()

    def myapiCursorFollowersIds(self):
        return tweepy.Cursor(self.api.followers_ids, id=self.account_name, cursor=-1).items()

    def myapiCursorFriendsIds(self):
        return tweepy.Cursor(self.api.friends_ids, id=self.account_name, cursor=-1).items()


    '''----------------------------------------
    favorite: 特定のキーワードのツイートに対していいねする
        [ パラメータ ]
        keyword(String): 検索ワード
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def favorite(self, keyword):
        model_data = {}
        # キーワード検索して対象のツイートIDを取得 [API発行 GET search/tweets 450]
        for tweet in self.myapiCursorSearch():
            # 取得したツイートにいいねする
            try:
                # [API発行 POST favorites/create 1000 per user; 1000 per app]
                self.myapiCreateFavorite(tweet.id)
                time.sleep(10)
            except tweepy.error.TweepError as e:
                import traceback; traceback.print_exc()
        return True

    '''----------------------------------------
    refavorite: ユーザにいいねを返す
        [ パラメータ ]
        mode(String): モード
            ohayousentai: おはよう戦隊ツイート
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def refavorite(self, mode):
        model_data = {}
        keyword = {'ohayousentai': 'おはよう戦隊', 'studyprogram': 'プログラミング学習'}
        # ハッシュタグからキーワード検索して対象のツイートIDを取得
        tweet_id = MyTweets.objects.filter(hashtags__contains=keyword[mode]).order_by('-tweet_id').values_list('tweet_id', flat=True).first()
        # いいねしたアカウントリストを取得
        favoriter_ids = self.getUserIDList(tweet_id)
        for favoriter_id in favoriter_ids:
            # 各アカウントの最新のツイートを取得
            tweets = self.myapiUserTimeline(id=favoriter_id, count=1)
            # 取得したツイートにいいねする
            for tweet in tweets:
                try:
                    # [API発行 POST favorites/create 1000 per user; 1000 per app]
                    self.myapiCreateFavorite(tweet.id)
                except :
                    import traceback; traceback.print_exc()
                    pass
        return True

    '''----------------------------------------
    arrangeFollow: フォロワー情報の整理
        [ パラメータ ]
        なし
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def arrangeFollow(self):
        model_data = {}
        # 片思いしてるアカウントを取得
        accounts = Users.objects.filter(follow_flg=True, follower_flg=False).values()
        # フォロー解除とユーザ情報の更新
        for account in accounts:
            self.myapiDestroyFriendship(account['user_id'])
            Users.objects.filter(user_id=account['user_id']).update(follow_flg=False)
        Users.objects.filter(follow_flg=False, follower_flg=False).delete()
        return True

    # 共通のフォロワーの抽出
    def extractCommonAccount(self, user_info, my_followers_copy):
        my_followers   = list(my_followers_copy)
        user_followers = list(self.myapiCursorFollowersIds())
        return set(my_followers) & set(user_followers)

    # 特定のユーザに対してリプライした数の取得
    def extractStaticReply(self, api_tweets, user_id):
        statics = 0
        for tweet_id in api_tweets:
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
    def extractStaticFavorite(self, tweet_ids):
        statics = {}
        for tweet_id in tweet_ids:
            favoriters = self.getUserIDList(tweet_id) # 最大100件
            for favoriter in favoriters:
                if str(favoriter) not in statics:
                    statics[str(favoriter)] = 1
                else:
                    statics[str(favoriter)] = statics[str(favoriter)] + 1
        return statics

    # リツイート統計値の取得
    def extractStaticRetweet(self, tweet_ids):
        statics = {}
        for tweet_id in tweet_ids:
            retweeters = self.myapiRetweets(id=tweet_id) # 最大100件
            for retweeter in retweeters:
                if retweeter.user.id_str not in statics:
                    statics[retweeter.user.id_str] = 1
                else:
                    statics[retweeter.user.id_str] = statics[retweeter.user.id_str] + 1
        return statics

    # 基本情報の取得
    def extractBaseInfo(self, user_info):
        user_model_data = {}
        user_model_data['user_id']         = user_info.id_str
        user_model_data['name']            = user_info.name
        user_model_data['screen_name']     = user_info.screen_name
        user_model_data['description']     = user_info.description
        user_model_data['follows_cnt']     = user_info.friends_count
        user_model_data['followers_cnt']   = user_info.followers_count
        user_model_data['listed_cnt']      = user_info.listed_count
        user_model_data['statuses_count']  = user_info.statuses_count
        if self.user_flg:
            user_model_data['follower_flg']    = True
        else:
            user_model_data['follow_flg']    = True
        return user_model_data

    '''----------------------------------------
    getUsers: ユーザ情報の取得
        [ パラメータ ]
        user_flg(Boolean): ユーザ分類フラグ
            True: フォロワー情報の取得
            False: フォロー情報の取得 
        diff_mode(Boolean): 差分反映モード
            True: 新規登録のみ
            False: 全件更新
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def getUsers(self, user_flg, diff_mode=True):
        self.user_flg = user_flg
        user_model_data = []

        # [API followers/ids friends/ids 15] フォロー/フォロワー情報の取得
        if user_flg: 
            api_users = self.myapiCursorFollowersIds()
        else:
            api_users = self.myapiCursorFriendsIds()
        api_users = set(str(id) for id in copy.deepcopy(api_users))
        if diff_mode:
            master_ids = set(Users.objects.values_list('user_id', flat=True))
        else:
            master_ids = set({})
        
        self.my_users = master_ids ^ api_users
        
        for my_user in self.my_users:
            if my_user not in api_users:
                Users.objects.filter(user_id=my_user).delete()
                self.my_users.pop(my_user)
                continue
            try:
                # [API users/show 900] アカウント情報の取得
                user_info = self.myapiGetUser(int(my_user))
                user_model_data.append(self.extractBaseInfo(user_info))
                # tmp_dict['cmn_followers_cnt'] = len(self.extractCommonAccount(user_info, copy.deepcopy(self.my_users)))
                # break
            except:
                traceback.print_exc()
                pass

        for data in user_model_data :
            try:
                if Users.objects.filter(user_id=data['user_id']).update(**data) == 0:
                    Users.objects.filter(user_id=data['user_id']).create(**data)
            except :
                traceback.print_exc()
                pass
        return True

    # データ正規化    
    def normalizeStatics(self, user_model_data, tmp_dict):
        users_master = Users.objects.all()
        for my_user in self.my_users:
            user_model = {} # 各ユーザのデータ格納用
            if my_user in tmp_dict['statics_favorite']:
                tmp = users_master.filter(user_id=my_user).values_list('favourites_cnt_for_me',flat=True).get()
                org = 0 if tmp is None else tmp
                user_model['favourites_cnt_for_me'] = tmp_dict['statics_favorite'][my_user] + org
            if my_user in tmp_dict['statics_retweet']:
                tmp = users_master.filter(user_id=my_user).values_list('retweets_cnt_for_me',flat=True).get()
                org = 0 if tmp is None else tmp
                user_model['retweets_cnt_for_me'] = tmp_dict['statics_retweet'][my_user] + org
            if my_user in tmp_dict['statics_reply']:
                tmp = users_master.filter(user_id=my_user).values_list('my_replies_cnt',flat=True).get()
                org = 0 if tmp is None else tmp
                user_model['my_replies_cnt'] = tmp_dict['statics_reply'][my_user] + org
            user_model_data[my_user] = user_model

    # 統計に関する情報の取得    
    def getUsersStatics(self):
        self.my_users = set(Users.objects.values_list('user_id', flat=True))
        user_model_data, tmp_dict = {}, {}
        # 自分のツイートIDのリストを取得 [API statuses/home_timeline 15]  100件
        api_tweets = self.myapiUserTimeline(id=self.account_name, count=100)
        api_ids = set(tweet.id for tweet in copy.deepcopy(api_tweets))
        master_ids = set(MyTweets.objects.values_list('tweet_id', flat=True).order_by('-tweet_id')[:200])
        tweet_ids = master_ids ^ api_ids
        for tweet_id in list(tweet_ids):
            if tweet_id in master_ids:
                tweet_ids.remove(tweet_id)
        # 自分のツイートに対してのリツイートの統計 [API発行 statuses/retweeters/ids 300]
        tmp_dict['statics_retweet'] = self.extractStaticRetweet(tweet_ids)
        # 自分のツイートに対してのいいねの統計
        tmp_dict['statics_favorite'] = self.extractStaticFavorite(tweet_ids)
        # 自分がリプライした数の取得
        tmp_dict['statics_reply'] = {}
        for my_user in self.my_users:
            reply_value = self.extractStaticReply(api_tweets, my_user)
            if reply_value != 0:
                tmp_dict['statics_reply'][my_user] = reply_value

        # データ正規化
        self.normalizeStatics(user_model_data, tmp_dict)
        # ユーザ情報更新
        for user_id, data in user_model_data.items():
            Users.objects.filter(user_id=user_id).update(**data)

    # コンストラクタ
    def __init__(self, account_name='feivs2019'):
        self.authTwitterAPI()
        self.account_name = account_name
