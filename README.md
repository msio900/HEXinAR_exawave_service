# 📰텍스트 마이닝을 이용한 트렌드 예측 서비스

> 멀티캠퍼스의 '빅데이터 기반 지능형 서비스 개발' 프로그램의 `HEXinAR` 팀의 `EXA_wave` 서비스 프로젝트 입니다.



#### 📑Contents

1. [Team Member](#idx1)
2. [Overview](#idx2)
3. [project scheduling](#idx3)



------

## Team Member<a id="idx1"></a> 

* Subject : 뉴스 분석을 통한 미래 키워드 예측
* Team : HEXinAR
* PM : 김민성
* Member : 주창석, 김수원, 권회동, 남승주, 김하영



## Overview<a id="idx2"></a>

* DAUM 일자별 news 기사의 날짜, 제목, 내용, url을 Scraping하고 DB news_dummy TB 저장

  

* OKT를 활용하여 명사 단위로 Token화하여 DB news_words TB 저장



* Word2Vec을 활용하여 단어의 연관도를 Pickle로 저장


## Project Scheduling<a id="idx3"></a>

* 프로젝트 계획

  - 주제선정  
  ![image](https://user-images.githubusercontent.com/85272350/136386032-597bf1f1-1285-49a9-8081-007b145243d6.png)

  - WIREFRAME
  ![image](https://user-images.githubusercontent.com/85272350/136385832-1c6b57de-f5f6-4a42-ba17-00af57232c87.png)
  
  - ERD  
  ![image](https://user-images.githubusercontent.com/85272350/136387764-bbe6f020-6448-42d0-bdec-a7aceeef6954.png)

  - 화면정의서  
  ![image](https://user-images.githubusercontent.com/85272350/136386252-5a1863cd-65cf-40b6-9983-d26b8f3e83cb.png)

  - WBS 작성  
  ![image](https://user-images.githubusercontent.com/85272350/136387475-5649a691-cbcc-4f04-b96b-c97d22a5df46.png)

* 스크래핑
  - DAUM 일자별 NEWS (2020. 08. 01 ~ 2021. 10. 06)
  - Schedule : 스크래핑 자동화
  
* DB 저장
  - news_dummy TB : news_id, pubdate, news_name(기사 제목), news_content(기사 내용), url
  - news_words TB : news_id, pub_date, news_words(전처리된 단어), url
  - news_df_YYYYMM TB : 특정 단어가 언급된 기사 빈도 수
  - news_tf_YYYYMM TB : 모든 기사에 언급된 특정 단어 전체의 빈도 수
  
* 서비스 구현


