

## 모듈 탑제
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

# url = 크롤링할 제품 페이지 (다른 제품 선택시 url만 변경)
url = "https://www.coupang.com/np/categories/403250"


## User-Agent 없으면 크롤링 못함
## Accept-Language 없으면 무한로딩..
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
}

# 제품 목록 만들기
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
cp_url = "https://www.coupang.com"
product_list = []
price_list = []
review_count_list = []
star_rating_list = []
url_list = []
rep_count_list = []
for li in range(1):  # 크롤링할 페이지 수
    div = soup.findAll("div", {"class": "name"})
    lis = soup.find("ul", {"id": "productList"}).findAll("li")

    for li in lis: # lis 뒤에 [:]로 리스트에서 임의로 추출(리뷰 개수)
        product = li.find("div", {"class": "name"})
        price = li.find("em", {"class": "sale"}).find("strong", {"class": "price-value"})
        rep = li.find("span", {"class": "rating-total-count"})
        star = li.find("em", {"class": "rating"})
        a_link = li.find("a", href=True)['href']
        ulink = cp_url + a_link

        # 별점이 없는 제품 생략
        if star is None:
            continue

        product = product.text.strip()
        price = price.text.strip("()") + "원"
        rep = rep.text.strip("()") + "개"
        star = star.text.strip() + "점"

        product_list.append(product)
        price_list.append(price)
        rep_count_list.append(rep)
        star_rating_list.append(star)
        url_list.append(ulink)


# 리뷰 크롤링
review_date_list = []
review_list = []
author_list = []
rating_list = []
## 빈 리스트 생성

## 제품 url_list를 반복
    ### NAME이 review인 element를 찾아서 클릭하고 Bs로 크롤링(클릭을 안하면 요소가 숨겨져있음)
for i, url in enumerate(url_list):
    browser = webdriver.Chrome('C:\chromedriver.exe')
    browser.get(url)
    time.sleep(5)
    browser.find_element(By.NAME, 'review').click()
    time.sleep(1)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    
    ## 리뷰 배너에서 1인당 리뷰 클래스를 찾기
    review_elements = soup.find_all('article', class_='sdp-review__article__list js_reviewArticleReviewList')


    ## review_count에 추출한 review_elements의 수 담기, 리스트에 추가
    review_count = len(review_elements)
    review_count_list.append(review_count)

    ## 리뷰내에서 작성일자, 작성자명, 별점, 리뷰 추출
    for element in review_elements:
        review_date = element.find('div', class_='sdp-review__article__list__info__product-info__reg-date').text.strip()


        author = element.find('span', class_='sdp-review__article__list__info__user__name js_reviewUserProfileImage').text.strip()
    
        
        rating_element = element.find('div', class_='sdp-review__article__list__info__product-info__star-orange js_reviewArticleRatingValue')
        rating = rating_element.get('data-rating')

        ## 리뷰가 다른 요소에 있는 경우도 있어서 if문으로 예외처리
        review_text = element.find('div', class_='sdp-review__article__list__review__content js_reviewArticleContent')
        if review_text == None:
            review_text = element.find('div', class_='sdp-review__article__list__info__product-info__name').text.strip()
        else:
            review_text = review_text.text.strip()
        ## 줄바꿈 제거
        review_text = re.sub("\n", '', review_text)

        ## 별점이 없으면 공백처
        if rating_element:
            rating = rating_element.get('data-rating')
        else:
            rating = ''

        review_date_list.append(review_date)
        author_list.append(author)
        review_list.append(review_text)
        rating_list.append(rating + "점")

    browser.quit()


# 데이터프레임
data = {
    "제품": [],
    "가격": [],
    "리뷰수": [],
    "총별점": [],
    "작성일자": [],
    "작성자명": [],
    "리뷰": [],
    "작성자 별점": []
}

### 모든 제품의 리뷰수가 동일하지 않아서 행열 오류발생. 추출한 리뷰수에 따라 행열 생
for i, product in enumerate(product_list):
    review_count = review_count_list[i]
    data["제품"].extend([product] * review_count)
    data["가격"].extend([price_list[i]] * review_count)
    data["리뷰수"].extend([rep_count_list[i]] * review_count)
    data["총별점"].extend([star_rating_list[i]] * review_count)
    data["작성일자"].extend(review_date_list[:review_count])
    data["작성자명"].extend(author_list[:review_count])
    data["리뷰"].extend(review_list[:review_count])
    data["작성자 별점"].extend(rating_list[:review_count])
    review_date_list = review_date_list[review_count:]
    author_list = author_list[review_count:]
    review_list = review_list[review_count:]
    rating_list = rating_list[review_count:]

df = pd.DataFrame(data)

# CSV 파일로 저장
df.to_csv("coupang_reviews.csv", encoding="utf-8", index=False)
