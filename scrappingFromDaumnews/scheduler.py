import csv
import datetime
import numpy as np
import pandas as pd
import re
import requests
import schedule
import sqlite3
import pickle
import time
from bs4 import BeautifulSoup
from collections import Counter
from konlpy.tag import Okt
from urllib.parse import quote, quote_plus
from gensim.models import Word2Vec

now = datetime.datetime.now()
nowDate = now.strftime('%Y%m%d')
yesterday = now - datetime.timedelta(1)
yesterDate = yesterday.strftime('%Y%m%d')


def preprocessing_articles(data):
    content = str(data).split('\n')
    content = list(filter(lambda s: len(s) > 3, content))
    content_prep = content[:-1]
    content_prep = list(filter(lambda s: len(s) > 30 and \
                                         '▶' not in s and \
                                         '©' not in s and \
                                         '▲' not in s and \
                                         '사진=' not in s and \
                                         '사진제공=' not in s and \
                                         '@' not in s and \
                                         not re.findall("기자 *$", s) and \
                                         not re.findall("제공 *$", s) and \
                                         not re.findall("이하", s) and \
                                         not re.findall("무단전재", s) and \
                                         not re.findall("기자 *= *", s), content_prep))

    content_prep = list(map(lambda s: re.sub("\[.*\]", "", s), content_prep))  # [스포츠서울]
    content_prep = list(map(lambda s: re.sub("\(.*\=.*\)", "", s), content_prep))  # (서울=뉴시스)
    content_prep = list(map(lambda s: re.sub("\【.*\=.*\】", "", s), content_prep))  # 【파이낸셜뉴스 포천=강근주 기자】
    content_prep = list(map(lambda s: re.sub('[^가-힣]', ' ', s), content_prep))  # 한글 제외 영문, 한자, 숫자, 특수문자 모두 제거

    return content_prep


def scrap():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"}

    max_page = 10000  # 뉴스 페이지 탭 수 지정

    page_url = f"https://news.daum.net/breakingnews/?page=10000&regDate={yesterDate}"
    page = requests.get(page_url, headers=headers)
    page_soup = BeautifulSoup(page.text, "lxml")
    last_page = page_soup.find("em", attrs="num_page").get_text()
    lastPage_num = re.sub(r'[^0-9]', '', last_page)
    # print(lastPage_num)

    results = []
    for j in range(1, int(lastPage_num) + 1):
        main_url = f"https://news.daum.net/breakingnews/?page={j}&regDate={yesterDate}"  # url 입력
        res = requests.get(main_url, headers=headers)

        if res.status_code == 200:
            print(yesterDate, int(lastPage_num), '중', j, 'page', round(j / int(lastPage_num) * 100, 2), '%', main_url,
                  'status:', res.status_code)
            soup = BeautifulSoup(res.text, "lxml")  # soup으로 저장
            main = soup.find("ul", attrs={"class": "list_news2 list_allnews"})
            news = main.find_all("strong", attrs={"class": "tit_thumb"})
            cnt = 0

            for new in news:
                urls = new.select_one("a")["href"]  # 페이지에 나와있는 뉴스 URL 변수 입력
                # print(urls)
                result = requests.get(urls, headers=headers)  # request 로 다시 개별 뉴스 접속

                if result.status_code == 200:
                    news_soup = BeautifulSoup(result.text, "lxml")
                    # 뉴스 제목, 발행시간, 기사본문 저장
                    news_name = news_soup.find("h3", attrs={"tit_view"}).get_text().strip()
                    pubdate = news_soup.find("span", attrs={"num_date"}).get_text().strip()
                    text = news_soup.find("div", attrs={"news_view"}).get_text().strip()
                    data_prep = preprocessing_articles(text)
                    news_content = "".join(data_prep).strip()
                    result_a = [news_name, pubdate, news_content, urls]
                    results.append(result_a)
                    cnt += 1

                else:
                    print(yesterDate, 'page : ', j, '번째 기사', 'error_code :', result.status_code, urls)
                    pass

        else:
            print(yesterDate, 'page : ', j, 'error_code :', res.status_code, main_url)
            pass

    conn = sqlite3.connect('../db.sqlite3')
    c = conn.cursor()
    df = pd.DataFrame(results, columns=['news_name', 'pubdate', 'news_content', 'url'])
    data_prep = df.replace('', np.nan)
    data_prep_drop = data_prep.dropna(axis=0)
    data_prep_drop_dup = data_prep_drop.drop_duplicates(['news_content'], keep='first', inplace=False,
                                                        ignore_index=True)
    data_prep_drop_dup.to_sql('news_dummy', conn, if_exists='append', index=False)
    conn.commit()

    print('스크래핑 및 news_dummy TB 저장')

    c.execute('''
        SELECT 
           pubdate,
           news_content,
           news_id
        FROM news_dummy
        WHERE pubdate
        LIKE '2021. 10.%'
        ''')
    all_news = c.fetchall()

    okt = Okt()
    for i in all_news:
        pub_time = i[0][-5:]
        pub_date = i[0][:-5].strip()
        pub_date = re.sub("[. ]", "", pub_date)
        content = i[1]
        news_id = i[2]
        words = okt.nouns(content)
        news_words = []
        for word in words:
            if len(word) > 1:
                news_words.append(word)
        c.execute("INSERT INTO news_words (pub_date, pub_time, news_words, news_id) VALUES(?,?,?,?)",
                  (pub_date, pub_time, str(news_words), news_id))
    conn.commit()

    dt_index = pd.date_range(end=yesterDate, periods=30, freq='D')
    dt_list = dt_index.strftime("%Y%m%d").tolist()
    dt_date = dt_list[-1]

    li_result = []
    for i in dt_list:
        c.execute(f"SELECT news_words FROM news_words WHERE pub_date LIKE '{i}'")
        result = c.fetchall()

        for words in result:
            words = re.sub("[-=+#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]", "", str(words))
            words = words.split(', ')
            li_result.append(words)

    model = Word2Vec(sentences=li_result, vector_size=100, window=5, min_count=5, workers=4, sg=0)

    save_data = model
    with open("sim_word.pkl", "wb") as w:
        pickle.dump(save_data, w)

    print('피클 저장 완료')

    c.execute(f'DROP TABLE IF EXISTS `tf_freq_{yesterDate[:-2]}`;')
    c.execute(f'''
            CREATE TABLE `tf_freq_{yesterDate[:-2]}` (
                `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `keyword` TEXT NOT NULL,
                `num` TEXT NOT NULL
            );
    ''')
    c.execute(f'DROP TABLE IF EXISTS `df_freq_{yesterDate[:-2]}`;')
    c.execute(f'''
            CREATE TABLE `df_freq_{yesterDate[:-2]}` (
                `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                `keyword` TEXT NOT NULL,
                `num` TEXT NOT NULL
            );
    ''')
    print('tf, df 나누기 시작')
    c.execute(f'''
            SELECT             
               news_words
            FROM news_words
            WHERE pub_date
            LIKE '{yesterDate[:-2]}%'
            ''')
    news_words = c.fetchall()
    # print(i, len(news_words))
    tf_words = []
    df_words = []
    for words in news_words:
        words = re.sub("[-=+#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]", "", str(words))
        df_list = list(set(words.split(', ')))
        tf_list = words.split(', ')
        # print(tf_list, df_list)
        for tf_word in tf_list:
            tf_word = tf_word.replace(',', '')
            tf_word = tf_word.strip()
            tf_words.append(tf_word)
            # print(tf_words)
        for df_word in df_list:
            df_word = df_word.replace(',', '')
            df_word = df_word.strip()
            df_words.append(df_word)
            # print(df_words)

    stopwords = ['지난', '이번', '통해', '위해', '이번', '대한', '상황', '진행', '대해', \
                 '이후', '최근', '지역', '관련', '시간', '라며', '현재', '예정', '모두', \
                 '이상', '한편', '때문', '경우', '공개', '가운데', '모습', '가장', '자신', \
                 '기준', '앞서', '우리', '대비', '기간', '사실', '모든', '또한', '역시', '포함', \
                 '동안', '일부', '진자', '상태', '정도', '당시', '역시', '억원', '만큼', '마련', \
                 '더욱', '면서', '비롯', '다만', '가지', '중인', '만원', '개월', '각각', '사이', \
                 '여러', '먼저', '두기', '여기', '매우', '대부분', '달라', '동시', '보이', '바로', \
                 '거나', '그동안', '누구', '반면', '인근', '각종', '로부터', '통한', '제대로', \
                 '대신', '달리', '별로', '수가', '조금', '서로', '대규모', '가량', '서도', '분기', \
                 '순간', '세대', '상대로', '여러분', '이기', '그대로', '다수', '마치', '해도', \
                 '라면', '오히려', '전일', '별도', '곳곳', '대해', '에서', '이고', '라고', '다고', '라기', \
                 '라며', '면서', '라면서', '로써', '로서', '으로', '에서', '어야', '부터', '한다', '이다', '였다', '였었다']

    tf_key = [w1 for w1 in tf_words if not w1 in stopwords]
    df_key = [w1 for w1 in df_words if not w1 in stopwords]

    count_tf = Counter(tf_key)
    count_df = Counter(df_key)
    for key, val in count_tf.items():
        c.execute(f"INSERT INTO `tf_freq_{yesterDate[:-2]}` (keyword, num) VALUES(?,?)", (key, val))
    for key, val in count_df.items():
        c.execute(f"INSERT INTO `df_freq_{yesterDate[:-2]}` (keyword, num) VALUES(?,?)", (key, val))

    conn.commit()
    conn.close()
    print(f'df_freq_{yesterDate[:-2]}와 tf_freq_{yesterDate[:-2]} 저장완료')


schedule.every().day.at("00:05").do(scrap)

while True:
    schedule.run_pending()
    time.sleep(1)