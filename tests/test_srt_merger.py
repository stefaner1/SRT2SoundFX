import unittest
from src.srt_merger import merge_prompts

class TestSrtMerger(unittest.TestCase):

    def setUp(self):
        self.prompts = [
            {'id': 1, 'prompt': 'sound of rain'},
            {'id': 2, 'prompt': 'sound of thunder'},
            {'id': 3, 'prompt': 'sound of wind'}
        ]
        self.srt_elements = [
            {'id': 1, 'start': '00:00:01,000', 'end': '00:00:02,000', 'text': 'It was a rainy day.'},
            {'id': 2, 'start': '00:00:03,000', 'end': '00:00:04,000', 'text': 'Suddenly, a thunder roared.'},
            {'id': 3, 'start': '00:00:05,000', 'end': '00:00:06,000', 'text': 'The wind was howling.'}
        ]

    def test_merge_prompts(self):
        result = merge_prompts(self.prompts, self.srt_elements)
        expected = [
            {'id': 1, 'start': '00:00:01,000', 'end': '00:00:02,000', 'prompt': 'sound of rain'},
            {'id': 2, 'start': '00:00:03,000', 'end': '00:00:04,000', 'prompt': 'sound of thunder'},
            {'id': 3, 'start': '00:00:05,000', 'end': '00:00:06,000', 'prompt': 'sound of wind'}
        ]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()