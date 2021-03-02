from pygame._sdl2 import get_num_audio_devices, get_audio_device_name
from pygame import mixer


class Player:
    def __init__(self, device='CABLE Input (VB-Audio Virtual Cable)'):
        self.device = device
        self.volume = 100

    def set_volume(self, val):
        self.volume = val+1

    def play(self, file):
        mixer.init(devicename=self.device)
        mixer.music.set_volume(self.volume)
        mixer.music.load(file)
        mixer.music.play()

    @staticmethod
    def stop():
        mixer.quit()

    @staticmethod
    def get_devices():
        mixer.init()
        r = [get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]
        mixer.quit()
        return r
