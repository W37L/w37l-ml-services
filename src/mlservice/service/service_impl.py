import joblib
from dataclasses import dataclass

from src.mlservice.model.model import *
from src.mlservice.service.utils.data_processing import *
from src.mlservice.adapters.repository import IMachineLearningRepository

@dataclass
class MachineLearningService:
    ml_repository: IMachineLearningRepository

    def check_profanity(self, text: str) -> Response:
        """
        Checks a given text for profanity using a pre-trained machine learning model.

        Args:
            text (str): The text to be checked for profanity.

        Returns:
            Response: A Response object indicating success status and message.
                - success: True if profanity is detected, False otherwise.
                - message: "Profanity detected" if profanity is found, "No profanity detected" otherwise.

        Raises:
            FileNotFoundError: If the profanity detection model or vectorizer files are not found.
        """


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
        """
        Suggests a hashtag for a given text using a pre-trained topic modeling model.

        Args:
            text (str): The text for which a hashtag suggestion is needed.

        Returns:
            Response: A Response object indicating success status and message.
                - success: True if a hashtag suggestion is generated, False otherwise.
                - message: The suggested hashtag string.

        Raises:
            Exception: If any unexpected error occurs during hashtag suggestion processing.
        """

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
        """
        Extracts trending topics from the most recent posts using a topic modeling model.

        This method leverages the `ml_repository` to retrieve recent posts and then uses
        a pre-trained topic modeling model to identify potential trending topics within the posts' content.

        Returns:
            Response: A Response object indicating success status and message.
                - success: True if trending topics are extracted, False otherwise.
                - message: A string containing the extracted trending topics (format depends on implementation).

        Raises:
            Exception: If any unexpected error occurs during trending topic extraction.
        """
        
        try:
            list_posts_text = [post.content for post in self.ml_repository.get_last_posts()]
            vectorizer = joblib.load('src/mlservice/service/utils/count_vectorizer.joblib')
            text_preprocessed = [preprocess_text(text) for text in list_posts_text]
            matrix = vectorizer.fit_transform(text_preprocessed)
            tf_feature_names = vectorizer.get_feature_names_out()
            lda = joblib.load('src/mlservice/service/utils/lda_trend_model.joblib').fit(matrix)
            topics = get_topics(lda, tf_feature_names, 3)
            return Response(success=True, message=topics)
        except Exception as e:
            return Response(success=False, message=str(e))

    def get_recommendation_user(self, user: str) -> Response:

        # Implement user recommendation logic here
        # ... (implementation details)

        return []  # Placeholder for recommendation logic

    def get_recommendation_post(self, user: str) -> Response:


        # Implement post recommendation logic here
        # ... (implementation details)

        return []  # Placeholder for recommendation logic