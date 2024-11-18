import unittest
import asyncio
from src.srt2soundfx.chatgpt_interface import send_to_chatgpt
from dotenv import load_dotenv



class TestChatGPTInterface(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.elements = [
            {"id": 1, "text": "The door creaked open slowly."},
            {"id": 2, "text": "She walked into the room silently."},
            {"id": 3, "text": "The wind howled outside the window."},
            {"id": 4, "text": "He poured the water into the glass."},
            {'id': 5, 'text': 'Hello, world!'}]

    def test_send_to_chatgpt(self):
        result = asyncio.run(send_to_chatgpt(self.elements))
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIn('id', item)
            self.assertIn('prompt', item)

if __name__ == '__main__':
    unittest.main()