import unittest
import clutter
from pyclut.controls.panel import Panel

class PanelTestCase(unittest.TestCase):
	"""Panel widget unit test cases"""
	def test_panel_creation_01(self):
		"""Panel : creation, with color"""
		size = (512, 256)
		panel = Panel(size=size, background="Black")
		background = panel.get_background()
		self.failUnlessEqual(size, background.get_size())
		self.failUnless(isinstance(background, clutter.Rectangle))

	def test_panel_creation_02(self):
		"""Panel : creation, with texture"""
		size = (512, 256)
		panel = Panel(size=size, background=clutter.Texture())
		background = panel.get_background()
		self.failUnlessEqual(size, background.get_size())
		self.failUnless(isinstance(background, clutter.Texture))

if __name__ == "__main__":
	unittest.main()



