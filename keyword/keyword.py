from konlpy.tag import Okt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import konlpy
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
#nltk.download('punkt')

stop_words_list = stopwords.words('korean')
#stop_words_list.append('삼성', '삼성전자', '김치', '플러스', '방문', '설치', '글램', '화이트', '리뷰', '김치냉장고', '사용', '시작', '교체', '유가')
df = pd.read_csv('C:/Users/xlawk/coupang_reviews.csv', encoding = 'utf-8')

clean_data1 = []
for main in df['리뷰'].to_list(): ### to_list = Series를 list로 만들기.
                                        ### == df 내의 comments열만.
    clean_main = re.sub('[^\w\d\s]', '', main)
    clean_data1.append(clean_main)

komoran = konlpy.tag.Komoran()
pos_data = []

clean_data = []

for text in clean_data1:
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
                            "]+", flags = re.UNICODE)
    text = emoji_pattern.sub(r'', text) ### 이모지 제거.
    text = re.sub('[|A-Za-z|]+', '', text) ### 알파벳 모두 제거.
    text = re.sub('[|0-9|]+', '', text) ### 숫자 제거.
    text = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", text)
    clean_data.append(text)

for clean_main in clean_data: ## komoran 품사 분류
    try:
        pos_main = komoran.pos(clean_main)
    except:
        continue
    pos_data.append(pos_main)

filter_data = []
for pos_main in pos_data:
    filter_main=[]
    for word, pos in pos_main:
        if pos == "NNP":  ## 고유명사
            filter_main.append(word)
        elif pos == 'NNG':  ## 일반 명사
            filter_main.append(word)

    filter_data.append(filter_main)

filter_data_1 = []
wordl = []
for sublist in filter_data:
    for word in sublist:
        if len(word) >1 and word not in stop_words_list:
            wordl.append(word)
    filter_data_1.append(wordl)
    wordl = []

docu = []
for final_main in filter_data_1:
    docu.append(" ".join(final_main))

df['Aword'] = pd.Series(filter_data_1)
df['clean_com'] = pd.Series(docu)
df.info()
address ='C:/Users/xlawk/'
df.to_csv(path_or_buf = address+'keywd.csv')

## 벡터화
vectorizer = TfidfVectorizer()
docu_tfidf = vectorizer.fit_transform(np.array(docu))
docu_tfidf_matrix = pd.DataFrame(np.array(docu_tfidf.todense()), columns = vectorizer.get_feature_names_out(), index= df['제품'])
docu_tfidf_matrix.to_csv(path_or_buf = address+'vector_review.csv')

