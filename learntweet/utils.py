import MeCab
import os

'''----------------------------------------
strings2list: 文字列をリストに変換する
    [ パラメータ ]
    ・list_strings(string): リスト文字列
    [ 返り値 ]
    ・list_result(string[]): 変換後のリストオブジェクト
----------------------------------------'''
def strings2list(list_strings):
    list_result = []
    # 両端をトリム
    list_strings = list_strings.strip("[""]")
    # 区切り文字で分割する
    tmp_result = list_strings.replace("),",") ,").split(" , ")
    # 各要素をリスト化して二次元配列化する
    for tmp_value in tmp_result:
        list_result.append(tmp_value.strip("("")").split(", "))
    return list_result


def _split_to_words(text, to_stem=False):
    """
    入力: 'すべて自分のほうへ'
    出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
    """
    tagger = MeCab.Tagger('mecabrc')  # 別のTaggerを使ってもいい
    mecab_result = tagger.parse(text)
    info_of_words = mecab_result.split('\n')
    words = []
    for info in info_of_words:
        # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
        if info == 'EOS' or info == '':
            break
            # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
        info_elems = info.split(',')
        # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
        if info_elems[6] == '*':
            # info_elems[0] => 'ヴァンロッサム\t名詞'
            words.append(info_elems[0][:-3])
            continue
        if to_stem:
            # 語幹に変換
            words.append(info_elems[6])
            continue
        # 語をそのまま
        words.append(info_elems[0][:-3])
    return words

def stems(text):
    stems = _split_to_words(text=text, to_stem=True)
    return stems