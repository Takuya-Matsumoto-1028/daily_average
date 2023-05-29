import streamlit as st
import numpy as np
import datetime
import pandas as pd

st.title('移動平均算出')

days = st.slider('何日平均を表示しますか',  min_value=0, max_value=365, step=1, value=365)

st.write('汎用集計表：T6001 / csv(utf-8) 算出する期間の倍以上を取得して下さい')
uploaded_file1 = st.file_uploader('ファイルをアップロード', type='csv')

# st.header('読み込みデータ表示')
if uploaded_file1 is not None:
    # アップロードファイルをメイン画面にデータ表示
    df = pd.read_csv(uploaded_file1)
    df = df.replace(',', '', regex=True)
    df = df[:-1]
    df['税抜売上金額'] = df['税抜売上金額'].astype(int)
    df['部門コード'] = df['部門コード'].astype(int)
    df['受注方法コード'] = df['受注方法コード'].astype(int)
    df['売上日付'] = pd.to_datetime(df['売上日付'], format='%Y年%m月%d日')

    # 移動平均計算（売上）
    df_sum = df.pivot_table(index='売上日付', columns='受注方法コード', values='税抜売上金額', aggfunc='sum', margins=True)
    df_sum = df_sum[:-1]
    df_sum = df_sum.rename(columns={'All': '売上金額(千円)'})
    df_sum = df_sum.reset_index()
    df_sum_ = df_sum.set_index('売上日付')
    df_sum_ = df_sum_['売上金額(千円)']
    df_sum_ = ((df_sum_.rolling(days).mean()).round(2)) / 1000
    df_sum_ = df_sum_[(days-1):]

    # st.line_chart(df_sum_)

    # 移動平均計算（客数）
    df_count = df.pivot_table(index='売上日付', columns='受注方法コード', values='税抜売上金額', aggfunc='count', margins=True)
    df_count = df_count[:-1]
    df_count = df_count.rename(columns={'All': '客数(人)'})
    df_count = df_count.reset_index()
    df_count_ = df_count.set_index('売上日付')
    df_count_ = df_count_['客数(人)']
    df_count_ = (df_count_.rolling(days).mean()).round(2)
    df_count_ = df_count_[(days-1):]

    # st.line_chart(df_count_)

    # 移動平均計算（客単価）
    df_average = df.pivot_table(index='売上日付', columns='受注方法コード', values='税抜売上金額', aggfunc='mean', margins=True)
    df_average = df_average[:-1]
    df_average = df_average.rename(columns={'All': '客単価(円)'})
    df_average = df_average.reset_index()
    df_average_ = df_average.set_index('売上日付')
    df_average_ = df_average_['客単価(円)']
    df_average_ = (df_average_.rolling(days).mean()).round(2)
    df_average_ = df_average_[(days-1):]

    # st.line_chart(df_average_)

    st.write(days, '日移動平均グラフ')
    df_concat = pd.concat([df_sum_, df_count_], axis=1)
    st.line_chart(df_concat)

    df1 = df_sum[df_sum['売上日付'] == datetime.datetime((datetime.date.today().year - 1), datetime.date.today().month, datetime.date.today().day)]
    df1 = df1[['売上金額(千円)']]
    df2 = df_count[df_count['売上日付'] == datetime.datetime((datetime.date.today().year - 1), datetime.date.today().month, datetime.date.today().day)]
    df2 = df2[['客数(人)']]
    df3 = df_average[df_average['売上日付'] == datetime.datetime((datetime.date.today().year - 1), datetime.date.today().month, datetime.date.today().day)]
    df3 = df3[['客単価(円)']]

    st.write('去年同日の売上金額は', df1.iloc[0,0], '円です。')
    st.write('去年同日の売上件数は', df2.iloc[0,0], '円です。')
    st.write('去年同日の平均客単価は', df3.iloc[0,0], '円です。')