import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpl_finance
import pandas as pd

from .models import T_BLAND_MS
from .models import T_STK_PRC_TR

chart_image_path = 'static/main_chart.png'


def getParams(model_name, model_data):
    if(model_name == 'T_STK_PRC_TR'):
        # 画面側パラメータ定義
        params = {
            'bland_info': model_data['T_BLAND_MS'].values()[0],
            'stock_info': model_data[model_name].values()[0],
            'chart_image_path': chart_image_path
        }
    return params

# Generate chart image


def generateChart(model_name, model_data, sample_mode):
    queryset = model_data[model_name]

    # チャートデータ編集
    df_origin = pd.DataFrame(list(queryset.values_list(
        'created_at', 'opening_price', 'high_orice', 'low_price', 'current_price', 'sales_volume'
    )))
    d_ohlcv = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }
    df_origin.set_index(0, inplace=True)
    df_origin.columns = d_ohlcv.keys()
    avline_key = list(d_ohlcv.keys())[3]

    # チャート判定
    if(sample_mode == 'week'):
        df = df_origin.resample('W-MON', closed='left',
                                label='left').agg(d_ohlcv).copy()
    elif(sample_mode == 'month'):
        df = df_origin.resample('MS', closed='left',
                                label='left').agg(d_ohlcv).copy()
    elif(sample_mode == 'year'):
        df = df_origin.resample('YS', closed='left',
                                label='left').agg(d_ohlcv).copy()
    else:
        df = df_origin.copy()
    df.index = mdates.date2num(df.index)
    arrays = df.reset_index().values

    # チャート作成
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(
        12, 4), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    mpl_finance.candlestick_ohlc(
        ax[0], arrays, width=4, alpha=0.75, colorup='r', colordown='b')
    ax[0].plot(df.index, df[avline_key].rolling(4).mean())
    ax[0].plot(df.index, df[avline_key].rolling(13).mean())
    ax[0].plot(df.index, df[avline_key].rolling(26).mean())
    ax[1].bar(df.index, df['volume'], width=4, color='navy')
    ax[0].grid
    ax[1].grid

    locator = mdates.AutoDateLocator()
    ax[0].xaxis.set_major_locator(locator)
    ax[0].xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

    plt.savefig(chart_image_path)

# get Model Data


def getModelData(bland_cd=''):
    model_data = {}
    if bland_cd == '':
        model_data['T_BLAND_MS'] = T_BLAND_MS.objects.all()
    else:
        model_data['T_BLAND_MS'] = T_BLAND_MS.objects.filter(bland_cd=bland_cd)
        model_data['T_STK_PRC_TR'] = T_STK_PRC_TR.objects.filter(bland_cd=bland_cd)

    return model_data
