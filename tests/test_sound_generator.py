import unittest
from src.srt2soundfx.sound_generator import generate_sounds
import os

class TestSoundGenerator(unittest.TestCase):
    def setUp(self):
        self.srt_elements = [
            {'id': 1, 'start': '00:00:01,000', 'end': '00:00:02,000', 'prompt': 'sound of rain', 'duration': 1},
            {'id': 2, 'start': '00:00:03,000', 'end': '00:00:04,000', 'prompt': 'sound of thunder', 'duration': 1},
        ]

    def test_generate_sounds(self):
        save_dir= os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "tests")
        sounds = generate_sounds(self.srt_elements, save_dir, "test")
        self.assertEqual(len(sounds), len(self.srt_elements))
        for sound in sounds:
            self.assertIn('id', sound)
            self.assertIn('start', sound)
            self.assertIn('end', sound)
            self.assertIn('audio_path', sound)

if __name__ == '__main__':
    unittest.main()