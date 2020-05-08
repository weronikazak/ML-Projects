import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class KCamera(Image):
	def __init__(self, capture, fps, **kwargs):
		super(KCamera, self).__init__(**kwargs)
		self.capture = capture
		Clock.schedule_interval(self.update, 1.0 / fps)

	def update(self, dt):
		ret, frame = self.capture.read()

		if ret:
			buf1 = cv2.flip(frame, 0)
			buf = buf1.tostring()
			image_texture = Texture.create(
				size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
			image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
			self.texture = image_texture


class CamApp(App):
	def build(self):
		self.capture = cv2.VideoCapture(0)
		self.my_camera = KCamera(capture=self.capture, fps=30)
		return self.my_camera


	def on_stop(self):
		self.capture.release()


if __name__ == "__main__":
	CamApp().run()