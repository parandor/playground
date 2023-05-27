import simpleaudio as sa

class SoundPlayer:
    def __init__(self):
        self.beep_flag = False

    def load_beep(self):
        # Load the WAV file using simpleaudio
        wave_obj = sa.WaveObject.from_wave_file("sound/beep.wav")

        # Play the sound
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def beep(self):
        if not self.beep_flag:
            # Play the beep sound only once on the first trough detection
            self.load_beep()
            self.beep_flag = True

    def beep_off(self):
        self.beep_flag = False
        