import pandas as pd
import sqlite3
import numpy as np
import pickle


# from config.settings import DATA_DIRS


def keywordissuemap_KIM(mon):
    freqMonth = int(mon)

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute(f'''
           SELECT 
               tf{freqMonth}.keyword,
               tf{freqMonth - 1}.num,
               tf{freqMonth}.num,
               df{freqMonth}.num,
               df{freqMonth - 1}.num
           FROM tf_freq_{freqMonth} tf{freqMonth}
           LEFT OUTER JOIN tf_freq_{freqMonth - 1} tf{freqMonth - 1}
           ON tf{freqMonth - 1}.keyword = tf{freqMonth}.keyword
           LEFT OUTER JOIN df_freq_{freqMonth - 1} df{freqMonth - 1}
           ON df{freqMonth - 1}.keyword = tf{freqMonth}.keyword
           LEFT OUTER JOIN df_freq_{freqMonth} df{freqMonth}
           ON df{freqMonth}.keyword = tf{freqMonth}.keyword
           ''')
    numKeywords = pd.DataFrame(c.fetchall(), columns=['keyword', 'tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum'])
    numKeywords[['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']] = numKeywords[
        ['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']].fillna(0)
    numKeywords[['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']] = numKeywords[
        ['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']].astype(int)

    KIM_result = []

    numKeywords1 = numKeywords.values.tolist()
    numKeywords = numKeywords1[:100]
    # print(numKeywords)
    for i in numKeywords:
        # print(i)
        keyWord = i[0]
        pre_tfNum = i[1]
        now_tfNum = i[2]
        pre_dfNum = i[3]
        now_dfNum = i[4]
        df_mean = round((pre_dfNum + now_dfNum) / 2, 2)
        tf_mean = round((pre_tfNum + now_tfNum) / 2, 2)
        df_changeRate = round((now_dfNum - pre_dfNum) / (pre_dfNum + 1) * 100, 2)
        tf_changeRate = round((now_tfNum - pre_tfNum) / (pre_dfNum + 1) * 100, 2)
        KIM_result.append({'x': df_mean, 'y': df_changeRate, 'name': keyWord, 'country': keyWord})

    conn.close()

    return KIM_result


def keywordissuemap_KEM(mon):
    freqMonth = int(mon)

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute(f'''
           SELECT 
               tf{freqMonth}.keyword,
               tf{freqMonth - 1}.num,
               tf{freqMonth}.num,
               df{freqMonth}.num,
               df{freqMonth - 1}.num
           FROM tf_freq_{freqMonth} tf{freqMonth}
           LEFT OUTER JOIN tf_freq_{freqMonth - 1} tf{freqMonth - 1}
           ON tf{freqMonth - 1}.keyword = tf{freqMonth}.keyword
           LEFT OUTER JOIN df_freq_{freqMonth - 1} df{freqMonth - 1}
           ON df{freqMonth - 1}.keyword = tf{freqMonth}.keyword
           LEFT OUTER JOIN df_freq_{freqMonth} df{freqMonth}
           ON df{freqMonth}.keyword = tf{freqMonth}.keyword
           ''')
    numKeywords = pd.DataFrame(c.fetchall(), columns=['keyword', 'tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum'])
    numKeywords[['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']] = numKeywords[
        ['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']].fillna(0)
    numKeywords[['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']] = numKeywords[
        ['tf_preNum', 'tf_nowNum', 'df_preNum', 'df_nowNum']].astype(int)

    KEM_result = []

    numKeywords1 = numKeywords.values.tolist()
    numKeywords = numKeywords1[:100]
    # print(numKeywords)
    for i in numKeywords:
        # print(i)
        keyWord = i[0]
        pre_tfNum = i[1]
        now_tfNum = i[2]
        pre_dfNum = i[3]
        now_dfNum = i[4]
        df_mean = round((pre_dfNum + now_dfNum) / 2, 2)
        tf_mean = round((pre_tfNum + now_tfNum) / 2, 2)
        df_changeRate = round((now_dfNum - pre_dfNum) / (pre_dfNum + 1) * 100, 2)
        tf_changeRate = round((now_tfNum - pre_tfNum) / (pre_dfNum + 1) * 100, 2)
        KEM_result.append({'x': tf_mean, 'y': tf_changeRate, 'name': keyWord, 'country': keyWord})

    conn.close()

    return KEM_result


with open("sim_word.pkl", "rb") as r:  # 피클파일경로 입력
    read_data = pickle.load(r)


def similarity_word(rela):
    search_word = rela
    w2v_model_result = read_data.wv.most_similar(search_word, topn=20)

    sim_words = []
    for i in w2v_model_result:
        sim_word = i[0].replace(',', '')
        # print(sim_words)
        sim_words.append([search_word, sim_word])

    return sim_words


# search_keyword 빈도수

import sqlite3
import re
from collections import Counter
from datetime import date
import pandas as pd
from gensim.models import Word2Vec
import pickle
import datetime


now = datetime.datetime.now()
nowDate = now.strftime('%Y%m%d')
yesterday = now - datetime.timedelta(1)
yesterDate = yesterday.strftime('%Y%m%d')

def searchKeywords(rela):
    keyword = rela

    dt_index = pd.date_range(end=yesterDate, periods=12, freq='M')
    dt_list = dt_index.strftime("%Y%m").tolist()

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    tf_word_nums = []
    df_word_nums = []
    categories = []
    for i in dt_list:
        categories.append(i[2:4] + '년 ' + i[4:6] + '월')
        c.execute(f"SELECT num FROM tf_freq_{i} WHERE keyword LIKE '{keyword}'")
        tf_word = c.fetchall()
        for freq in tf_word:
            freq = re.sub("[-=+#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》,]", "", str(freq))
            tf_word_nums.append(int(freq))

        c.execute(f"SELECT num FROM df_freq_{i} WHERE keyword LIKE '{keyword}'")
        df_word = c.fetchall()
        for freq in df_word:
            freq = re.sub("[-=+#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》,]", "", str(freq))
            df_word_nums.append(int(freq))

    # name = name
    # data = data

    #     print(categories, tf_word_nums, df_word_nums)

    conn.close()
    return categories, tf_word_nums, df_word_nums


if __name__ == "__main__":
    keywordissuemap_KIM(202010);
    print(keywordissuemap_KIM(202010));

    similarity_word('달고나');
    print(similarity_word("달고나"));

    print(searchKeywords("손학규"))
