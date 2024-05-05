import joblib
from dataclasses import dataclass

from src.mlservice.model.model import *
from src.mlservice.service.utils.data_processing import *
from src.mlservice.adapters.repository import IMachineLearningRepository

@dataclass
class MachineLearningService:
    ml_repository: IMachineLearningRepository

    def check_profanity(self, text: str) -> Response:

        try:
            model = joblib.load('src/mlservice/service/utils/linear_svc_model.joblib')
            vectorizer = joblib.load('src/mlservice/service/utils/count_vectorizer.joblib')
            proccesed = preprocess_text(text)
            feature = vectorizer.transform([proccesed])
            prediction = model.predict(feature)[0]
            message = "Profanity detected" if prediction == 1 else "No profanity detected"
            response = Response(success=True if prediction == 1 else False, message=message)
            return response
        except FileNotFoundError:
            return Response(success=False, message="Profanity detection model or vectorizer not found.")
        
    def get_hashtag(self, text: str) -> Response:
        try:
            text = preprocess_text(text)
            vectorizer = joblib.load('src/mlservice/service/utils/count_vectorizer.joblib')
            matrix = vectorizer.fit_transform([text])
            tf_feature_names = vectorizer.get_feature_names_out()
            lda = joblib.load('src/mlservice/service/utils/lda_model.joblib')
            lda.fit(matrix)
            hashtag = get_hashtag(lda, tf_feature_names, 3)
            return Response(success=True, message=hashtag)
        except Exception as e:
            return Response(success=False, message=str(e))


    def get_trending_topics(self) -> Response:
        try:
            list_posts = self.ml_repository.get_last_posts()
            vectorizer = joblib.load('src/mlservice/service/utils/count_vectorizer.joblib')
            text_preprocessed = [preprocess_text(text) for text in list_posts]
            matrix = vectorizer.fit_transform(text_preprocessed)
            tf_feature_names = vectorizer.get_feature_names_out()
            lda = joblib.load('src/mlservice/service/utils/lda_trend_model.joblib').fit(matrix)
            topics = get_topics(lda, tf_feature_names, 3)
            return Response(success=True, message=topics)
        except Exception as e:
            return Response(success=False, message=str(e))

    def get_recommendation_user(self, user: User) -> list[str]:

        # Implement user recommendation logic here
        # ... (implementation details)

        return []  # Placeholder for recommendation logic

    def get_recommendation_post(self, user: User) -> list[str]:


        # Implement post recommendation logic here
        # ... (implementation details)

        return []  # Placeholder for recommendation logic