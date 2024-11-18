import unittest
from src.srt2soundfx.audio_placer import AudioPlacer

class TestAudioPlacer(unittest.TestCase):

    def setUp(self):
        self.sound_effects = [
            {
                'id': '1',
                'start': 1,
                'end': 5,
                'audio_path': '/app/tests/resources/1.mp3'
            },
            {
                'id': '2',
                'start': 6,
                'end': 8,
                'audio_path': '/app/tests/resources/2.mp3'
            }
        ]
        self.audiobook_file="/app/tests/resources/audiobook.mp3"
        self.temp_dir="/app/tests/resources/"

    def test_place_audio(self):
        audio_placer=AudioPlacer()
        result = audio_placer.add_sounds_to_audio(self.audiobook_file, self.sound_effects, self.temp_dir)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()