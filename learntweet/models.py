from django.db import models
from feivs2019AccountManager.models import *
from .utils import *
import pandas as pd
import MeCab
import copy
import gensim
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Create your models here.
class UserAnalistics(models.Model):
    screen_name                 = models.CharField(max_length=128, null=True)
    name                        = models.CharField(max_length=128, null=True)
    text                        = models.CharField(max_length=8000, null=True)
    vecs                        = models.CharField(max_length=8000, null=True)
    similarity                  = models.FloatField(null=True)

class LearnManager(models.Manager):



    '''----------------------------------------
    displayAnalistics: 分析結果を生成する
        [ パラメータ ]
        ・id(int): 取得対象のID
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def displayAnalistics(self, id):
        save_path = 'static/images/vecs_hist.png'

        # 分析データを取得する
        data = UserAnalistics.objects.filter(screen_name=id).values_list('vecs', flat=True).get()
        if len(data) == 0:
            return pd.DataFrame([])
        data_list = strings2list(data)
        # 取得したデータをデータフレーム化する
        df = pd.DataFrame(
            data_list
            , columns=['dict_index', 'freq']
        )
        # 辞書とマッピングさせる
        dictionary = self.createDictionary(None)
        dict_tokens = [ dictionary[int(index)] for index in df['dict_index'].values.tolist() ]
        # df['token']= dict_tokens
        df['dict_index'] = df['dict_index'].astype(int)
        df['freq'] = df['freq'].astype(float)

        return df


    '''----------------------------------------
    getLDA: LDAの分類機を作成（学習させる）
        [ パラメータ ]
            ・corpus_tfidf: TFIDF分析したコーパス
            ・dictionary: 辞書
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def getLDA(self, corpus_tfidf, dictionary):
        save_path = 'saves/mytweets.lda'
        if self.relearn_mode:
            lda = gensim.models.LdaModel(
                corpus=corpus_tfidf
                , id2word=dictionary
                , num_topics=50
                , minimum_probability=0.001
                , passes=20
                , update_every=0
                , chunksize=10000
            )
            lda.save(save_path)
        else:
            lda = gensim.models.LdaModel.load(save_path)
        return lda

    '''----------------------------------------
    getTFIFD: コーパスからTFIFDを取得する
        [ パラメータ ]
            ・corpus: コーパス
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def getTFIFD(self, corpus):
        save_path = 'saves/mytweets.dump'
        if self.relearn_mode:
            tfidf = gensim.models.TfidfModel(corpus)
            corpus_tfidf = tfidf[corpus]
            with open(save_path, mode='wb') as f:
                pickle.dump(corpus_tfidf, f)
        else:
            with open(save_path, mode='rb') as f:
                corpus_tfidf = pickle.load(f)
        return corpus_tfidf

    '''----------------------------------------
    createCorpus: 辞書からコーパスを作成する
        [ パラメータ ]
            ・dictionary: 辞書
            ・docs: 単語一覧のリスト
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def createCorpus(self, dictionary, docs):
        save_path = 'saves/mytweets.mm'
        if self.relearn_mode:
            corpus = [dictionary.doc2bow(doc) for doc in docs]
            gensim.corpora.MmCorpus.serialize(save_path, corpus)
        else:
            corpus = gensim.corpora.MmCorpus(save_path)
        return corpus

    '''----------------------------------------
    createDictionary: 単語群からLDA用の辞書を作成する
        [ パラメータ ]
            ・docs: 単語一覧のリスト
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def createDictionary(self, docs):
        save_path = 'saves/mytweets.dict'
        if self.relearn_mode:
            dictionary = gensim.corpora.Dictionary(docs)
            dictionary.save_as_text(save_path)
        else:
            dictionary = gensim.corpora.Dictionary.load_from_text(save_path)
        return dictionary

    '''----------------------------------------
    getdocs: 特定のトピックスから単語を取得する
        [ パラメータ ]
        ・topics(string[]): 辞書の作成元になるトピックス
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def getDocs(self, topics):
        # ツイートを分かち書き
        mecab = MeCab.Tagger("-Owakati")
        strings = [mecab.parse(topic) for topic in topics]
        # 単語解析したものを返す
        return [stems(row) for row in strings]


    '''----------------------------------------
    createLDA: 自分のツイートからLDA分類機を作成する
        [ パラメータ ]
        なし
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def createLDA(self):
        docs = None

        # 今回は自分のタイムラインから辞書を作成
        my_tweets_manager = MyTweetsManager()
        self.my_timelines = my_tweets_manager.myapiUserTimeline(id='feivs2019',count=100)

        # 辞書の元になるトピックスを生成
        topics = [tweet.text for tweet in copy.deepcopy(self.my_timelines)]
        if self.relearn_mode:
            # 自分のタイムラインを取得して単語解析
            docs = self.getDocs(topics)
        # 辞書を作成
        self.dictionary = self.createDictionary(docs)
        # コーパスを作成
        corpus = self.createCorpus(self.dictionary, docs)
        # TFIDFを取得
        corpus_tfidf = self.getTFIFD(corpus)
        # LDAの分類機を作成（学習させる）
        self.lda = self.getLDA(corpus_tfidf, self.dictionary)


    '''----------------------------------------
    createModelFromTopics: トピックスからモデルを作成する
        [ パラメータ ]
        ・topics(DataFrame{id,name,text,similarity}): 分析対象となるトピックス
            id: トピックID
            name: トピック名
            text: 分析対象となる文章
            similarity: 先頭データとの類似度
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def createModelFromTopics(self, topics):
        for user in topics.itertuples():
            if UserAnalistics.objects.filter(screen_name=user.id).update(screen_name=user.id, name=user.name, similarity=user.similarity, text=user.text, vecs=user.vecs) == 0:
                UserAnalistics.objects.filter(screen_name=user.id).create(screen_name=user.id, name=user.name, similarity=user.similarity, text=user.text, vecs=user.vecs)


    '''----------------------------------------
    calcVecs: トピックスをLDA分類機にかけて類似度を算出する
        [ パラメータ ]
            ・topics(DataFrame{id,name,text}): 分析対象となるトピックス（先頭要素が比較元となる）
                id: トピックID
                name: トピック名
                text: 分析対象となる文章
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def calcVecs(self, topics):
        similarities = []
        vecses = []
        # アカウントごとに分析していく
        for index, item in topics.iterrows():
            # LDAトピック計算
            vecs = self.dictionary.doc2bow(stems(item['text']))
            vecses.append(vecs)
            # 先頭行のLDA算出値は比較元として退避しておき、以降の行のLDA分析値との類似度を算出する
            if index != 0:
                similarities.append(sum(cosine_similarity(base_result, self.lda[vecs])[0]))
            else:
                base_result = self.lda[vecs]
                similarities.append(0)
                continue
       
        return (vecses, similarities)


    '''----------------------------------------
    getTopicsFromTweets: 各ユーザのタイムラインからトピックスを作成する
        [ パラメータ ]
            ・USER_COUNT(int): 対象のユーザ数
            ・TIMELINE_COUNT(int): 取得するタイムラインのツイート数
        [ 返り値 ]
            ・topics(DataFrame{id,name,text}): 分析対象となるトピックス
    ----------------------------------------'''
    def getTopicsFromTweets(self, USER_COUNT=100, TIMELINE_COUNT=50):
        my_tweets_manager = MyTweetsManager()
        base_account_id = 'feivs2019'
        if self.user_mode:
            # フォロワー情報を取得
            users = Users.objects.all().filter(follower_flg=1).values('user_id', 'screen_name', 'name')[:USER_COUNT]
        else:
            # フォロー情報を取得
            users = Users.objects.all().filter(follow_flg=1).values('user_id', 'screen_name', 'name')[:USER_COUNT]

        result_ids   = [ user['screen_name'] for user in users ]
        result_ids.insert(0, base_account_id)
        result_names = [ user['name'] for user in users ]
        result_names.insert(0, 'This is BaseAccount')
        result_texts = []
        for id in result_ids:
            # import pdb;pdb.set_trace()
            try:
                result_texts.append(''.join([
                    tweet.text for tweet in my_tweets_manager.myapiUserTimeline(id=id,count=TIMELINE_COUNT)
                ]))
            except:
                result_texts.append('faild')
                pass
        
        topics = pd.DataFrame({
            'id'     : result_ids
            , 'name' : result_names
            , 'text' : result_texts
        })

        return topics


    '''----------------------------------------
    calcLdaVector: トピックスを既存のLDA分類機で分析し類似度を付与する
        [ パラメータ ]
            ・topics(DataFrame{id,name,text}): 分析対象となるトピックス
                id: トピックID
                name: トピック名
                text: 分析対象となる文章
        [ 返り値 ]
        ・topics(DataFrame{id,name,text,similarity}): 分析対象となるトピックス
            id: トピックID
            name: トピック名
            text: 分析対象となる文章
            similarity: 先頭データとの類似度
    ----------------------------------------'''
    def calcLdaVector(self, topics):
        (vecses, similarities) = self.calcVecs(topics)
        topics['vecs'] = vecses
        topics['similarity'] = similarities


    '''----------------------------------------
    コンストラクタ
        [ パラメータ ]
            ・user_mode(String): ユーザ取得モード
                follower: フォロワー
                friend: フォロー
            ・relearn_mode(String): 再学習モード
                True: 再学習する
                False: 前回の学習結果を使用する
        [ 返り値 ]
        なし
    ----------------------------------------'''
    def __init__(self, user_mode=None, relearn_mode=None):
        super().__init__()
        # ユーザ取得モード
        if user_mode == 'follow':
            self.user_mode = True
        else:
            self.user_mode = False
        # 再学習モード
        if relearn_mode == 'True':
            self.relearn_mode = True
        else:
            self.relearn_mode = False
