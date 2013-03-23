from gi.repository import Clutter
from pyclut.utils import get_keyval
import glob
import os.path
import sys

class PyClutTest(object):
	def __init__(self, resolution=(1024, 768), background_color=None, image_directory="./images"):
		Clutter.init(sys.argv)
		self._stage = Clutter.Stage()
		self._stage.set_size(*resolution)
		self._stage.connect('destroy', self.quit)
		color = Clutter.Color()
		color.from_string(background_color or "Black")
		self._stage.set_color(color)
		self._stage.set_title(self.__class__.__name__)
		self._stage.show()
		self.item_images = glob.glob(os.path.join(image_directory, "*.png"))
		self.current_image = 0
		self._stage_center = (self._stage.get_size()[0]/2, self._stage.get_size()[1]/2)
		self._stage.connect('key-press-event', self.on_input)

	def impl_on_input(self, *args):
		pass

	def quit(self, *args):
		Clutter.main_quit()

	def on_input(self, stage, event):
		if get_keyval(event) == Clutter.q:
			Clutter.main_quit()
		else:
			self.impl_on_input(stage, event)

	def get_image(self):
		self.current_image = (self.current_image + 1) % len(self.item_images)
		return self.item_images[self.current_image-1]



