import joblib
import re
from bs4 import BeautifulSoup

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from dataclasses import dataclass

from src.models.model import User
from src.models.model import Post
from src.adapters.repository import IMachineLearningRepository


@dataclass
class MachineLearningService:
    ml_repository: IMachineLearningRepository

    def check_profanity(self, content: str) -> bool:
        model = joblib.load('src/service/models/linear_svc_model.joblib')
        vectorizer = joblib.load('src/service/models/vectorizer.joblib')
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

    stop_words = stopwords.words('english')
    review_without_stop_words = ' '.join([word for word in text.split() if word not in stop_words]) 
    stemmer = SnowballStemmer("english") 
    review_stemmed = ' '.join([stemmer.stem(word) for word in
    review_without_stop_words.split()])
    return review_stemmed
