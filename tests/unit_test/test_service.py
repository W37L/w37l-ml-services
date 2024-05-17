import unittest
from unittest.mock import patch, MagicMock

from src.mlservice.service.service_impl import MachineLearningService
from src.mlservice.adapters.repository import IMachineLearningRepository


class TestMachineLearningService(unittest.TestCase):

    @patch('joblib.load')
    @patch('src.mlservice.service.utils.data_processing.preprocess_text')
    def test_check_profanity(self, mock_preprocess_text, mock_joblib_load):
        mock_preprocess_text.return_value = 'processed text'
        
        mock_model = MagicMock()
        mock_model.predict.return_value = [1]
        mock_joblib_load.side_effect = [mock_model, MagicMock()]

        ml_repository = MagicMock(spec=IMachineLearningRepository)
        service = MachineLearningService(ml_repository=ml_repository)

        response = service.check_profanity('some text')
        self.assertTrue(response.success)
        self.assertEqual(response.message, 'Profanity detected')

        mock_model.predict.return_value = [0]
        response = service.check_profanity('some text')
        self.assertFalse(response.success)
        self.assertEqual(response.message, 'No profanity detected')

    @patch('joblib.load')
    @patch('src.mlservice.service.utils.data_processing.preprocess_text')
    def test_get_hashtag(self, mock_preprocess_text, mock_joblib_load):
        mock_preprocess_text.return_value = 'processed text'
        
        mock_vectorizer = MagicMock()
        mock_vectorizer.fit_transform.return_value = 'matrix'
        mock_vectorizer.get_feature_names_out.return_value = ['word1', 'word2', 'word3']
        
        mock_lda = MagicMock()
        mock_joblib_load.side_effect = [mock_vectorizer, mock_lda]

        ml_repository = MagicMock(spec=IMachineLearningRepository)
        service = MachineLearningService(ml_repository=ml_repository)

        with patch('src.mlservice.service.machine_learning_service.get_hashtag', return_value='#hashtag'):
            response = service.get_hashtag('some text')
        
        self.assertTrue(response.success)
        self.assertEqual(response.message, '#hashtag')

    @patch('joblib.load')
    @patch('src.mlservice.service.utils.data_processing.preprocess_text')
    def test_get_trending_topics(self, mock_preprocess_text, mock_joblib_load):
        mock_preprocess_text.side_effect = lambda text: f'processed {text}'
        
        mock_vectorizer = MagicMock()
        mock_vectorizer.fit_transform.return_value = 'matrix'
        mock_vectorizer.get_feature_names_out.return_value = ['word1', 'word2', 'word3']
        
        mock_lda = MagicMock()
        mock_joblib_load.side_effect = [mock_vectorizer, mock_lda]

        ml_repository = MagicMock(spec=IMachineLearningRepository)
        ml_repository.get_last_posts.return_value = [MagicMock(content='post1'), MagicMock(content='post2')]
        service = MachineLearningService(ml_repository=ml_repository)

        with patch('src.mlservice.service.machine_learning_service.get_topics', return_value='topics'):
            response = service.get_trending_topics()
        
        self.assertTrue(response.success)
        self.assertEqual(response.message, 'topics')

if __name__ == '__main__':
    unittest.main()