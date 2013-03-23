from gi.repository import Clutter, GObject
from pyclut.controls.button import PulseButton
from pyclut.basics.rectangle import RoundRectangle

class Key(object):
	def __init__(self, value=None, text=None):
		self.value = value
		self.text = text

	def __str__(self):
		if self.text:
			return self.text
		return ""

	def __call__(self, *args, **kwargs):
		if self.value:
			return self.value
		return self.text

class LayoutSwitcher(Key):
	def __init__ (self, switch_to_layout, value=None, text=None):
		Key.__init__(self, value, text)
		self.switch_to_layout = switch_to_layout

class KeyFactory(object):
	def getKey(self, key):
		if isinstance(key, str):
			return Key(text=key)
		elif isinstance(key, Key):
			return key
		elif isinstance(key, list) or isinstance(key, tuple):
			return Key(text=key[0], value=key[1])

class KeyboardLayout:
	def __init__ (self, name, key_map=None):
		self.name = name
		self._key_map = []
		self.__key_factory = KeyFactory()
		if key_map:
			self.set_key_map(key_map)

	def set_key_map(self, key_map):
		self._key_map = [[self.__key_factory.getKey(key) for key in line] for line in key_map]

	def get_key_map(self):
		return self._key_map

class PulseButtonFactory(object):
	def __init__(self, background=None, color=None):
		self._background = background
		self._color = color

	def get_button(self, text=None, value=None):
		if self._background:
			background=Clutter.Texture.new_from_file(self._background)
		else:
			background=Clutter.RoundRectangle()
			background.set_color(self._color or "White")
		return PulseButton(background, text=text, value=value)

class KeyRowLayout(Clutter.Group):
	__gtype_name__ = 'KeyRowLayout'
	__gsignals__ = {
		'key-pressed' : ( GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,) ),
	}
	def __init__(self, keys, button_factory=None, button_size=(75,75), inter_button_space=0):
		Clutter.Group.__init__(self)
		x, y = 0, 0
		for key in keys:
			button=button_factory.get_button(text=str(key), value=key)
			button.set_size(*button_size)
			button.connect("pressed", self._on_pressed)
			self.add_actor(button)
			button.set_position(x, y)
			x += button_size[0] + inter_button_space

	def _on_pressed(self, event, key):
		self.emit("key-pressed", key)

class SimpleKeyboard(Clutter.Group):
	__gtype_name__ = 'SimpleKeyboard'
	__gsignals__ = {
		'key-pressed' : ( GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,) ),
	}

	def __init__(self, layout=None, background=None, button_factory=None,
		button_size=(75,75), inter_button_space=0):
		Clutter.Group.__init__(self)
		self._layout = layout
		self._button_size = button_size
		self._inter_button_space = inter_button_space
		self._background = background or RoundRectangle()
		self._button_factory = button_factory or PulseButtonFactory()
		self.add_actor(self._background)
		self.__create_buttons()

	def __get_keyboard_size(self):
		height = self._inter_button_space + len(self._layout.get_key_map()) * (self._button_size[1]+self._inter_button_space)
		width = 0
		for line in self._layout.get_key_map():
			width = max(width, self._inter_button_space + len(line)*(self._button_size[0]+self._inter_button_space))
		return width, height

	def __create_buttons(self):
		width, height = self.__get_keyboard_size()
		self._background.set_size(width, height)
		y=self._inter_button_space
		for line in self._layout.get_key_map():
			row = KeyRowLayout(line, self._button_factory, self._button_size, self._inter_button_space)
			row.connect("key-pressed", self._on_button)
			self.add_actor(row)
			row.set_position(self._inter_button_space+(width-row.get_width())/2, y)
			y += self._button_size[1]+self._inter_button_space

	def _on_button(self, event, key):
		self.emit("key-pressed", key())


