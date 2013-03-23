from gi.repository import Clutter
from pyclut.controls.panel import Panel

class UIConfigurationProxy(object):
	def __init__(self, resolution, screens, config):
		self._config = config
		if config:
			self._resolution = resolution or self._config.get_resolution()
			self._screens = self._config.get_screens()
		else:
			self._resolution = resolution or (1024, 768)
			self._screens = {}
		self._screens.update(screens or {})

	def add_screen(self, name, screen):
		self._screens[name] = screen
		
	def get_screen(self, name):
		return self._screens[name]

	def get_resolution(self):
		return self._resolution

	def get_screens(self):
		return self._screens

	def get_nb_screen(self):
		return len(self._screens)

class UserInterface(object):
	def __init__(self, resolution=None, screens=None, config=None):
		self._config = UIConfigurationProxy(resolution, screens, config)
		self.current_screen = None
		self._stage = Clutter.Stage()
		self._stage.set_size(*self._config.get_resolution())
		self._stage.connect('destroy', Clutter.main_quit)

	def run(self):
		self._stage.show()
		Clutter.main()

	def create_screen(self, name, background, components):
		screen = Panel(self.get_resolution(), background, *components)
		screen.hide()
		self._config.add_screen(name, screen)
		
	def set_screen(self, name):
		if self.current_screen:
			self.current_screen.hide()
			self._stage.remove(self.current_screen)
		self.current_screen = self._config.get_screen(name)
		self._stage.add_actor(self.current_screen)
		self.current_screen.show()
		
		
	def switch_to_screen(self, screen_name, transition=None):
		pass

	def get_resolution(self):
		return self._config.get_resolution()

	def get_screens(self):
		return self._config.get_screens()

	def get_nb_screen(self):
		return self._config.get_nb_screen()


