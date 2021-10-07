##키워드 이슈맵 함수 keywordissuemap(data)
## 202009 형식으로 데이터가 들어가야함.
## 표시 가능 범위는 : 2020.09~2021.08

import pandas as pd
import sqlite3
import numpy as np


def keywordMap(mon):
    freqMonth = int(mon)

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute(f'''
        SELECT 
            tf{freqMonth}.keyword,
            tf{freqMonth-1}.num,
            tf{freqMonth}.num,
            df{freqMonth}.num,
            df{freqMonth-1}.num
        FROM tf_freq_{freqMonth} tf{freqMonth}
        LEFT OUTER JOIN tf_freq_{freqMonth-1} tf{freqMonth-1}
        ON tf{freqMonth-1}.keyword = tf{freqMonth}.keyword
        LEFT OUTER JOIN df_freq_{freqMonth-1} df{freqMonth-1}
        ON df{freqMonth-1}.keyword = tf{freqMonth}.keyword
        LEFT OUTER JOIN df_freq_{freqMonth} df{freqMonth}
        ON df{freqMonth}.keyword = tf{freqMonth}.keyword
        ''')
    numKeywords = pd.DataFrame(c.fetchall(), columns= ['keyword', 'tf_preNum' ,'tf_nowNum','df_preNum', 'df_nowNum'])
    numKeywords[['tf_preNum' ,'tf_nowNum','df_preNum', 'df_nowNum']] = numKeywords[['tf_preNum' ,'tf_nowNum','df_preNum', 'df_nowNum']].fillna(0)
    numKeywords[['tf_preNum' ,'tf_nowNum','df_preNum', 'df_nowNum']] = numKeywords[['tf_preNum' ,'tf_nowNum','df_preNum', 'df_nowNum']].astype(int)


    KEM_result = []
    KIM_result = []

    KEM_df_mean = []
    KEM_df_changeRate =[]
    KIM_tf_mean = []
    KIM_tf_changeRate = []
    KEM = []
    KIM = []
    numKeywords = numKeywords.values.tolist()

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
        df_changeRate = round((now_dfNum - pre_dfNum) / (pre_dfNum+1) * 100,2)
        tf_changeRate = round((now_tfNum - pre_tfNum) / (pre_dfNum+1) * 100,2)
        KEM.append([keyWord, tf_mean, tf_changeRate])
        KIM.append([keyWord, df_mean, df_changeRate])
        KIM_result.append({'x': df_mean,'y': df_changeRate , 'name' : keyWord, 'country': keyWord})
        KEM_result.append({'x': tf_mean,'y': tf_changeRate , 'name' : keyWord, 'country': keyWord})


    KEM = np.array(KEM)
    KIM = np.array(KIM)

    tf_mean_median = np.median(KEM[:,1].astype(np.float32))
    tf_change_median = np.median(KEM[:,2].astype(np.float32))

    df_mean_median = np.median(KIM[:,1].astype(np.float32))
    df_change_median = np.median(KIM[:,2].astype(np.float32))

    # print('tf평균',tf_mean_mean,'df평균',df_mean_mean, 'tf중앙',tf_mean_median, 'tf중앙',df_mean_median)

    KEM_strongSig = []
    KEM_weakSig = []
    KEM_latentSig = []
    KEM_wellKnownSig = []

    KIM_strongSig = []
    KIM_weakSig = []
    KIM_latentSig = []
    KIM_wellKnownSig = []

    for KEM_word in KEM:
        if (KEM_word[1].astype(np.float32) >= tf_mean_median) & (KEM_word[2].astype(np.float32) >= tf_change_median) :
            KEM_strongSig.append(KEM_word)
        elif (KEM_word[1].astype(np.float32) < tf_mean_median) & (KEM_word[2].astype(np.float32) >= tf_change_median) :
            KEM_weakSig.append(KEM_word)
        elif (KEM_word[1].astype(np.float32) < tf_mean_median) & (KEM_word[2].astype(np.float32) < tf_change_median) :
            KEM_latentSig.append(KEM_word)
        else:
            KEM_wellKnownSig.append(KEM_word)

    KEM_strongSigDF = pd.DataFrame(KEM_strongSig, columns = ['keyword', 'tf_mean', 'tf_changeRate'])
    KEM_strongSigDF = KEM_strongSigDF.astype({'tf_mean':'float', 'tf_changeRate':'float'})
    KEM_strongSigDF.sort_values('tf_changeRate', ascending=False,  inplace=True)

    KEM_weakSigDF = pd.DataFrame(KEM_weakSig, columns = ['keyword', 'tf_mean', 'tf_changeRate'])
    KEM_weakSigDF = KEM_weakSigDF.astype({'tf_mean':'float', 'tf_changeRate':'float'})
    KEM_weakSigDF.sort_values('tf_changeRate', ascending=False,  inplace=True)

    KEM_latentSigDF = pd.DataFrame(KEM_latentSig, columns = ['keyword', 'tf_mean', 'tf_changeRate'])
    KEM_latentSigDF = KEM_latentSigDF.astype({'tf_mean':'float', 'tf_changeRate':'float'})
    KEM_latentSigDF.sort_values('tf_changeRate', ascending=False,  inplace=True)

    KEM_wellKnownSigDF = pd.DataFrame(KEM_wellKnownSig, columns = ['keyword', 'tf_mean', 'tf_changeRate'])
    KEM_wellKnownSigDF = KEM_wellKnownSigDF.astype({'tf_mean':'float', 'tf_changeRate':'float'})
    KEM_wellKnownSigDF.sort_values('tf_changeRate', ascending=False,  inplace=True)




    for KIM_word in KIM:
        if (KIM_word[1].astype(np.float32) >= df_mean_median) & (KIM_word[2].astype(np.float32) >= df_change_median) :
            KIM_strongSig.append(KIM_word)
        elif (KIM_word[1].astype(np.float32) < df_mean_median) & (KIM_word[2].astype(np.float32) >= df_change_median) :
            KIM_weakSig.append(KIM_word)
        elif (KIM_word[1].astype(np.float32) < df_mean_median) & (KIM_word[2].astype(np.float32) < df_change_median) :
            KIM_latentSig.append(KIM_word)
        else:
            KIM_wellKnownSig.append(KIM_word)

    KIM_strongSigDF = pd.DataFrame(KIM_strongSig, columns = ['keyword', 'df_mean', 'df_changeRate'])
    KIM_strongSigDF = KIM_strongSigDF.astype({'df_mean':'float', 'df_changeRate':'float'})
    KIM_strongSigDF.sort_values('df_changeRate', ascending=False,  inplace=True)

    KIM_weakSigDF = pd.DataFrame(KIM_weakSig, columns = ['keyword', 'df_mean', 'df_changeRate'])
    KIM_weakSigDF = KIM_weakSigDF.astype({'df_mean':'float', 'df_changeRate':'float'})
    KIM_weakSigDF.sort_values('df_changeRate', ascending=False,  inplace=True)

    KIM_latentSigDF = pd.DataFrame(KIM_latentSig, columns = ['keyword', 'df_mean', 'df_changeRate'])
    KIM_latentSigDF = KIM_latentSigDF.astype({'df_mean':'float', 'df_changeRate':'float'})
    KIM_latentSigDF.sort_values('df_changeRate', ascending=False,  inplace=True)

    KIM_wellKnownSigDF = pd.DataFrame(KIM_wellKnownSig, columns = ['keyword', 'df_mean', 'df_changeRate'])
    KIM_wellKnownSigDF = KIM_wellKnownSigDF.astype({'df_mean':'float', 'df_changeRate':'float'})
    KIM_wellKnownSigDF.sort_values('df_changeRate', ascending=False, inplace=True)

    KEM_strongSigTop10 = list(KEM_strongSigDF.keyword[:10])
    KEM_weakSigTop10=list(KEM_weakSigDF.keyword[:10])
    KEM_latentSigTop10=list(KEM_latentSigDF.keyword[:10])
    KEM_wellKnownSigTop10=list(KEM_wellKnownSigDF.keyword[:10])

    KIM_strongSigTop10=list(KIM_strongSigDF.keyword[:10])
    KIM_weakSigTop10=list(KIM_weakSigDF.keyword[:10])
    KIM_latentSigTop10=list(KIM_latentSigDF.keyword[:10])
    KIM_wellKnownSigTop10=list(KIM_wellKnownSigDF.keyword[:10])

    conn.close()

    return KEM_result[:10], KIM_result[:10], KEM_strongSigTop10, KEM_weakSigTop10, KEM_latentSigTop10, KEM_wellKnownSigTop10, KIM_strongSigTop10, KIM_weakSigTop10, KIM_latentSigTop10, KIM_wellKnownSigTop10


if __name__ == "__main__":
    print(keywordMap(202009)[2])