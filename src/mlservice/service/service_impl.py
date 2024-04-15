import joblib
import re
from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer
from dataclasses import dataclass

from src.mlservice.models.model import User
from src.mlservice.models.model import Post
from src.mlservice.adapters.repository import IMachineLearningRepository


@dataclass
class MachineLearningService:
    ml_repository: IMachineLearningRepository

    def check_profanity(self, content: str) -> bool:
        model = joblib.load('src/mlservice/service/utils/linear_svc_model.joblib')
        vectorizer = joblib.load('src/mlservice/service/utils/vectorizer.joblib')
        proccesed = preprocess_text(content)
        feature = vectorizer.transform([proccesed])
        prediction = model.predict(feature)[0]
        return prediction == 1
    
    def get_trending_topics(self) -> list[str]:
        list_posts = self.ml_repository.get_last_posts()
        return list_posts
    
    def get_recomendation_user(self, user: User) -> list[str]:
        ...
    
    def get_recomendation_post(self, user: User) -> list[str]:
        ...


def preprocess_text(text):
    text = BeautifulSoup(text, 'html.parser').get_text() 
    text = re.sub(r'http\S+', '', text) 
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    review_without_stop_words = ' '.join([word for word in text.split() if word not in stop_words]) 
    stemmer = SnowballStemmer("english") 
    review_stemmed = ' '.join([stemmer.stem(word) for word in
    review_without_stop_words.split()])
    return review_stemmed

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                   'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they',
                     'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those',
                       'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                         'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
                           'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
                             'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
                               'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
                                 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                                   'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd',
                                     'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven',
                                       'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']
