import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

class Camera():
    def __init__(self):
        self.picam2 = Picamera2()
        video_config = self.picam2.create_video_configuration()
        self.picam2.configure(video_config)
        self.encoder = H264Encoder(10000000)

    def start(self):
        self.picam2.start_recording(self.encoder, f'launch-{time.time()}.h264')

    def stop(self):
        self.picam2.stop_recording()