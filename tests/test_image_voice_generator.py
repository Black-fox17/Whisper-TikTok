import unittest
from unittest import mock

from src.image_generator import generate_image
from src.voice_generator import generate_voice


class TestImageVoiceGenerator(unittest.TestCase):

    @mock.patch('requests.post')
    def test_generate_images(self, mock_post):
        mock_response = mock.Mock()
        mock_response.text = 'mocked response'
        mock_post.return_value = mock_response

        result = generate_image('prompt', 'negative_prompt', 1, 1, 100, 100, 1, 'key')
        self.assertEqual(result, 'mocked response')

    @mock.patch('requests.post')
    def test_create_voice(self, mock_post):
        mock_response = mock.Mock()
        mock_response.text = 'mocked voice'
        mock_post.return_value = mock_response

        result = generate_voice('prompt', 'voice_id', 'key')
        self.assertEqual(result, 'mocked voice')


if __name__ == '__main__':
    unittest.main()
