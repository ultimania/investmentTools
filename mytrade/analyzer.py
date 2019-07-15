from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

from .models import T_STK_PRC_TR

def learnSvm(bland_cd):
    modified_data = []
    successive_data = []
    answers = []

    stock_data = pd.DataFrame(list(T_STK_PRC_TR.objects.filter(bland_cd=bland_cd).values_list(
            'opening_price'
            ,'high_orice'
            ,'low_price'
            ,'current_price'
            ,'sales_volume'
    )))
    stock_data.columns = [
            'open'
            ,'high'
            ,'low'
            ,'end'
            ,'volume'
    ]
    count_s = len(stock_data)

    for i in range(1, count_s):
        prev_value = float(stock_data.loc[i-1, ['end']])
        modified_data.append(
            float(stock_data.loc[i, ['end']] - prev_value) / float(prev_value * 20)
        )
    count_m = len(modified_data)

    continuity = 4  # 連続日数
    for i in range(continuity, count_m):
        successive_data.append([
            modified_data[i - continuity]
            ,modified_data[i - continuity + 1]
            ,modified_data[i - continuity + 2]
            ,modified_data[i - continuity + 3]
        ])
        if modified_data[i] > 0:
            answers.append(1)
        else:
            answers.append(0)

    # データの分割    
    x_train, x_test, y_train, y_test = train_test_split(
        successive_data
        ,answers
        ,train_size = 0.99
        ,test_size = 0.01
        ,random_state = 1
    )

    # SVMによる学習
    clf = svm.LinearSVC()
    clf.fit(x_train, y_train)

    # 学習後の評価
    y_train_pred = clf.predict(x_train)
    train_score = round(accuracy_score(y_train, y_train_pred)*100, 2)

    # 未知データの分類
    y_test_pred = clf.predict(x_test)
    pred_result = '上昇' if y_test_pred[0] == 1 else '下降'

    # 分類結果を返す
    return [pred_result, train_score]