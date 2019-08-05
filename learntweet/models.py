from django.db import models
from feivs2019AccountManager.models import *
from .utils import stems
import pandas as pd
import MeCab
import copy
import gensim
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Create your models here.
class UserAnalistics(models.Model):
    screen_name                 = models.CharField(max_length=128, null=True)
    name                        = models.CharField(max_length=128, null=True)
    similarity                  = models.FloatField(null=True)

class LearnManager(models.Manager):
    '''----------------------------------------
    getLDA: LDAの分類機を作成（学習させる）
        [ パラメータ ]
            ・corpus_tfidf: TFIDF分析したコーパス
            ・dictionary: 辞書
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def getLDA(self, corpus_tfidf, dictionary):
        lda = gensim.models.LdaModel(
            corpus=corpus_tfidf
            , id2word=dictionary
            , num_topics=50
            , minimum_probability=0.001
            , passes=20
            , update_every=0
            , chunksize=10000
        )
        lda.save('saves/mytweets.lda')
        return lda

    '''----------------------------------------
    createDictionary: 単語群からLDA用の辞書を作成する
        [ パラメータ ]
            ・docs: 単語一覧のリスト
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def createCorpus(self, dictionary, docs):
        corpus = [dictionary.doc2bow(doc) for doc in docs]
        gensim.corpora.MmCorpus.serialize('saves/mytweets.mm', corpus)
        return corpus

    '''----------------------------------------
    createDictionary: 単語群からLDA用の辞書を作成する
        [ パラメータ ]
            ・docs: 単語一覧のリスト
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def createDictionary(self, docs):
        dictionary = gensim.corpora.Dictionary(docs)
        dictionary.save_as_text('saves/mytweets.dict')
        return dictionary

    '''----------------------------------------
    getdocs: 自分のタイムラインのツイートの単語群を取得する
        [ パラメータ ]
        なし
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def getDocs(self):
        mecab = MeCab.Tagger("-Owakati")
        # ツイートを分かち書き
        strings = [mecab.parse(tweet.text) for tweet in copy.deepcopy(self.my_timelines)]
        return [stems(row) for row in strings]

    '''----------------------------------------
    createLDA: 自分のツイートからLDA分類機を作成する
        [ パラメータ ]
        なし
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def createLDA(self):
        my_tweets_manager = MyTweetsManager()
        # 自分のタイムラインを取得して単語解析
        self.my_timelines = my_tweets_manager.myapiUserTimeline(id='feivs2019',count=100)
        docs = self.getDocs()
        # 辞書を作成
        self.dictionary = self.createDictionary(docs)
        # コーパスを作成
        corpus = self.createCorpus(self.dictionary, docs)
        # TFIDFを取得
        tfidf = gensim.models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        with open('saves/mytweets.dump', mode='wb') as f:
            pickle.dump(corpus_tfidf, f)
        # LDAの分類機を作成（学習させる）
        self.lda = self.getLDA(corpus_tfidf, self.dictionary)

    '''----------------------------------------
    calc_vecs: アカウントリストから各アカウント名とLDA計算値のセットリストを返す
        [ パラメータ ]
            ・mode(boolean): アカウント取得モード
                True: フォロワー情報の取得
                False: フォロー情報の取得 
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def calc_vecs(self, mode):
        result_screen_names = []
        result_names = []
        result_vecs = []
        my_tweets_manager = MyTweetsManager()
        my_timeline_text = ''.join([tweet.text for tweet in copy.deepcopy(self.my_timelines)])
        myvec = self.dictionary.doc2bow(stems(my_timeline_text))

        if mode:
            users = Users.objects.all().filter(follower_flg=1).values('user_id', 'screen_name', 'name')
        else:
            users = Users.objects.all().filter(follow_flg=1).values('user_id', 'screen_name', 'name')

        # アカウントごとに分析していく
        for user in users:
            # 対象アカウントのタイムラインのテキストを取得して連結
            target_timeline = my_tweets_manager.myapiUserTimeline(id=user['user_id'],count=10)
            timeline_text = ''.join([tweet.text for tweet in target_timeline])
            # LDAトピック計算
            vecs = self.dictionary.doc2bow(stems(timeline_text))
            similarity = sum(cosine_similarity(self.lda[myvec], self.lda[vecs])[0])

            result_vecs.append(similarity)
            result_screen_names.append(user['screen_name'])
            result_names.append(user['name'])
        
        return (result_screen_names, result_names, result_vecs)


    '''----------------------------------------
    analysTweets: 特定のアカウントのツイートを潜在意味解析して類似度を出す
        [ パラメータ ]
            ・mode(String): アカウントの選定モード
                follower: フォロワー
                friend: フォロー
            ・MIN_SIMILARITY: 類似度しきい値
            ・RELATE_STORE_NUM: アカウント抽出数
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def analysTweets(self, mode, MIN_SIMILARITY, RELATE_STORE_NUM):
        # import pdb;pdb.set_trace()
        (screen_names, names, similarities) = self.calc_vecs(mode)

        df = pd.DataFrame({
            'screen_name'  : screen_names
            , 'name'       : names
            , 'similarity' : similarities
        })
        for user in df.itertuples():
            if UserAnalistics.objects.filter(screen_name=user.screen_name).update(screen_name=user.screen_name, name=user.name, similarity=user.similarity) == 0:
                UserAnalistics.objects.filter(screen_name=user.screen_name).create(screen_name=user.screen_name, name=user.name, similarity=user.similarity)

        # relate_store_list = df[df.similarity > MIN_SIMILARITY].sort_values(by="similarity", ascending=False).head(RELATE_STORE_NUM)
        # print(relate_store_list)

