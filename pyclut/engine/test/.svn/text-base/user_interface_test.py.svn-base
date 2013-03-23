import unittest
import mox
import pyclut
from pyclut.engine.user_interface import UserInterface

class UserInterfaceTestCase(unittest.TestCase):
	"""UserInterface unit test cases"""
	def setUp(self):
		self.mox_factory = mox.Mox()
		self._mock_config = self.mox_factory.CreateMockAnything()

	def tearDown(self):
		self.mox_factory.VerifyAll()

	def test_ui_creation_01(self):
		"""UserInterface : creation, check default values"""
		default_resolution = (1024, 768)
		self.mox_factory.ReplayAll()
		ui = UserInterface()
		self.failUnlessEqual(default_resolution, ui.get_resolution())
		self.failUnlessEqual({}, ui.get_screens())
		self.failUnlessEqual(0, ui.get_nb_screen())

	def test_ui_creation_02(self):
		"""UserInterface : creation, check attributes given in constructor"""
		resolution = (800, 600)
		screen_names = ["first", "second", "third"]
		screens = {}
		for name in screen_names:
			screens[name] = self.mox_factory.CreateMockAnything()
		self.mox_factory.ReplayAll()
		ui = UserInterface(
			resolution = resolution,
			screens = screens,
		)
		self.failUnlessEqual(resolution, ui.get_resolution())
		self.failUnlessEqual(screens, ui.get_screens())
		self.failUnlessEqual(len(screen_names), ui.get_nb_screen())

	def __prepare_ui_with_config(self, resolution=(800, 600), screens=None):
		self._mock_config.get_resolution().AndReturn(resolution)
		self._mock_config.get_screens().AndReturn(screens)

		mox.Replay(self._mock_config)
		ui = UserInterface(
			config = self._mock_config,
		)
		mox.Reset(self._mock_config)
		return ui

	def test_ui_creation_03(self):
		"""UserInterface : creation, check with configuration"""
		resolution = (800, 600)
		screen_names = ["first", "second", "third"]
		screens = {}
		for name in screen_names:
			screens[name] = "something" #self.mox_factory.CreateMockAnything()
		ui = self.__prepare_ui_with_config(resolution, screens)
		self.failUnlessEqual(resolution, ui.get_resolution())
		self.failUnlessEqual(screens, ui.get_screens())
		self.failUnlessEqual(len(screen_names), ui.get_nb_screen())

	def test_screen_creation_01(self):
		"""UserInterface : create screen from config"""
		resolution = (800, 600)
		screen_names = ["first", "second"]
		screens = {}
		for name in screen_names:
			screens[name] = self.mox_factory.CreateMockAnything()
		ui = self.__prepare_ui_with_config(resolution, screens)

if __name__ == "__main__":
	unittest.main()


