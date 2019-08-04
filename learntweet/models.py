from django.db import models
from feivs2019AccountManager.models import *
import pandas as pd
import MeCab
import copy
from gensim import corpora, models
from utils import stems
import pickle

# Create your models here.
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
        mecab = MeCab.Tagger ("-Owakati")
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
        dictionary = self.createDictionary(docs)
        # コーパスを作成
        corpus = self.createCorpus(dictionary, docs)
        # TFIDFを取得
        tfidf = gensim.models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        with open('saves/mytweets.dump', mode='wb') as f:
            pickle.dump(corpus_tfidf, f)
        # LDAの分類機を作成（学習させる）
        self.lda = self.getLDA(corpus_tfidf, dictionary)

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
        # 対象のタイムラインリストを取得
        target_timelines = MyTweetsManager.getTimelines(mode)
        # 自分のタイムラインのLDA計算
        (myname, mypref, myvec) = self.calc_vecs(self.my_timelines, self.lda, dictionary)
        # 取得したタイムラインのLDA計算
        (names, prefs, vecs) = self.calc_vecs(target_timelines, self.lda, dictionary)
        # 類似度を計算
        similarities = self.cosine_similarity(myvec, vecs)
        # 結果を表示
        self.printResult()

