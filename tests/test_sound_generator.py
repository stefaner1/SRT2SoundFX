import unittest
from src.sound_generator import generate_sounds

class TestSoundGenerator(unittest.TestCase):
    def setUp(self):
        self.srt_elements = [
            {'id': 1, 'start': '00:00:01,000', 'end': '00:00:02,000', 'prompt': 'sound of rain'},
            {'id': 2, 'start': '00:00:03,000', 'end': '00:00:04,000', 'prompt': 'sound of thunder'},
        ]

    def test_generate_sounds(self):
        sounds = generate_sounds(self.srt_elements)
        self.assertEqual(len(sounds), len(self.srt_elements))
        for sound in sounds:
            self.assertIn('id', sound)
            self.assertIn('start', sound)
            self.assertIn('end', sound)
            self.assertIn('audio', sound)

if __name__ == '__main__':
    unittest.main()