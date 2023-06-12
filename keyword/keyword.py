from konlpy.tag import Okt
from nltk.corpus import stopwords
import konlpy


clean_data1 = []
for main in df['comments'].to_list(): ### to_list = Series를 list로 만들기.
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
    text = re.sub("[^가-힣ㄱ-ㅎㅏ-|\\s]", "", text)
    clean_data.append(text)
