# ๐ฐํ์คํธ ๋ง์ด๋์ ์ด์ฉํ ํธ๋ ๋ ์์ธก ์๋น์ค

> ๋ฉํฐ์บ ํผ์ค์ '๋น๋ฐ์ดํฐ ๊ธฐ๋ฐ ์ง๋ฅํ ์๋น์ค ๊ฐ๋ฐ' ํ๋ก๊ทธ๋จ์ `HEXinAR` ํ์ `EXA_wave` ์๋น์ค ํ๋ก์ ํธ ์๋๋ค.



#### ๐Contents

1. [Team Member](#idx1)
2. [Overview](#idx2)
3. [project scheduling](#idx3)



------

## Team Member<a id="idx1"></a> 

* Subject : ๋ด์ค ๋ถ์์ ํตํ ๋ฏธ๋ ํค์๋ ์์ธก
* Team : HEXinAR
* PM : ๊น๋ฏผ์ฑ
* Member : ์ฃผ์ฐฝ์, ๊น์์, ๊ถํ๋, ๋จ์น์ฃผ, ๊นํ์



## Overview<a id="idx2"></a>

* DAUM ์ผ์๋ณ news ๊ธฐ์ฌ์ ๋ ์ง, ์ ๋ชฉ, ๋ด์ฉ, url์ Scrapingํ๊ณ  DB news_dummy TB ์ ์ฅ

  

* OKT๋ฅผ ํ์ฉํ์ฌ ๋ช์ฌ ๋จ์๋ก Tokenํํ์ฌ DB news_words TB ์ ์ฅ



* Word2Vec์ ํ์ฉํ์ฌ ๋จ์ด์ ์ฐ๊ด๋๋ฅผ Pickle๋ก ์ ์ฅ


## Project Scheduling<a id="idx3"></a>

* ํ๋ก์ ํธ ๊ณํ

  - ์ฃผ์ ์ ์   
  ![image](https://user-images.githubusercontent.com/85272350/136386032-597bf1f1-1285-49a9-8081-007b145243d6.png)

  - WIREFRAME
  ![image](https://user-images.githubusercontent.com/85272350/136385832-1c6b57de-f5f6-4a42-ba17-00af57232c87.png)
  
  - ERD  
  ![image](https://user-images.githubusercontent.com/85272350/136387764-bbe6f020-6448-42d0-bdec-a7aceeef6954.png)

  - ํ๋ฉด์ ์์  
  ![image](https://user-images.githubusercontent.com/85272350/136386252-5a1863cd-65cf-40b6-9983-d26b8f3e83cb.png)

  - WBS ์์ฑ  
  ![image](https://user-images.githubusercontent.com/85272350/136387475-5649a691-cbcc-4f04-b96b-c97d22a5df46.png)

* ์คํฌ๋ํ
  - DAUM ์ผ์๋ณ NEWS (2020. 08. 01 ~ 2021. 10. 06)
  - Schedule : ์คํฌ๋ํ ์๋ํ
  
* DB ์ ์ฅ
  - news_dummy TB : news_id, pubdate, news_name(๊ธฐ์ฌ ์ ๋ชฉ), news_content(๊ธฐ์ฌ ๋ด์ฉ), url
  - news_words TB : news_id, pub_date, news_words(์ ์ฒ๋ฆฌ๋ ๋จ์ด), url
  - news_df_YYYYMM TB : ํน์  ๋จ์ด๊ฐ ์ธ๊ธ๋ ๊ธฐ์ฌ ๋น๋ ์
  - news_tf_YYYYMM TB : ๋ชจ๋  ๊ธฐ์ฌ์ ์ธ๊ธ๋ ํน์  ๋จ์ด ์ ์ฒด์ ๋น๋ ์
  
* ์๋น์ค ๊ตฌํ


