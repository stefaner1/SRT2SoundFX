import unittest
from src.chatgpt_interface import send_to_chatgpt

class TestChatGPTInterface(unittest.TestCase):
    def setUp(self):
        self.elements = [{'id': 1, 'text': 'Hello, world!'}]

    def test_send_to_chatgpt(self):
        result = send_to_chatgpt(self.elements)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(self.elements))
        for item in result:
            self.assertIn('id', item)
            self.assertIn('prompt', item)

if __name__ == '__main__':
    unittest.main()