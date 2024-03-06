import io
import threading

class CameraOutput(object):
    def __init__(self, filename, format):
        self.output_file = io.open(filename, 'wb')
        self.format = format
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        if self.format == 'mjpeg' and buf.startswith(b'\xff\xd8'):
            # This is a new frame; signal HTTP clients that the frame is available.
            with self.condition:
                self.frame = buf
                self.condition.notify_all()
        self.output_file.write(buf)

    def flush(self):
        self.output_file.flush()