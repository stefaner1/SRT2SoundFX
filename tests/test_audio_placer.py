import unittest
from src.audio_placer import place_audio

class TestAudioPlacer(unittest.TestCase):

    def setUp(self):
        self.sound_effects = [
            {
                'id': '1',
                'start': '00:00:01,000',
                'end': '00:00:02,000',
                'sound_effect': 'sound_effect_1.mp3'
            },
            {
                'id': '2',
                'start': '00:00:03,000',
                'end': '00:00:04,000',
                'sound_effect': 'sound_effect_2.mp3'
            }
        ]

    def test_place_audio(self):
        result = place_audio(self.sound_effects)
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()