from gi.repository import Clutter, Cogl, GObject
from pyclut.animation import ScaleAndFadeAnimation, OpacityAnimation
from pyclut.basics.rectangle import RoundRectangle

class ImageButton(Clutter.Group):
	"""ImageButton: button defined with two images, one image for
	release state, and one image for pressed state.
	A short fade effect is used to switch from one to the other.
	"""
	__gtype_name__ = 'ImageButton'
	__gsignals__ = {
		'pressed' : ( GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,) ),
		'released' : ( GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,) ),
	}

	def __init__(self, released_background, pressed_background, value=None):
		Clutter.Group.__init__(self)
		self._value = value
		self._pressed_background = pressed_background
		self._pressed_background.set_opacity(0)
		self._released_background = released_background
		self._released_background.set_opacity(255)
		self._show = OpacityAnimation(255, 10, Clutter.AnimationMode.LINEAR)
		self._hide = OpacityAnimation(0, 10, Clutter.AnimationMode.LINEAR)
		self.add_actor(self._pressed_background)
		self.add_actor(self._released_background)
		self._released_background.connect("button-press-event", self._on_pressed)
		self._released_background.connect("button-release-event", self._on_released)
		self._released_background.set_reactive(True)

	def _show_pressed(self):
		self._show.apply(self._pressed_background)
		self._hide.apply(self._released_background)
		self._show.start()
		self._hide.start()

	def _show_released(self):
		self._show.apply(self._released_background)
		self._hide.apply(self._pressed_background)
		self._show.start()
		self._hide.start()

	def _on_pressed(self, background, event):
		if event.button == 1:
			self._show_pressed()
			self.emit("pressed", self._value)

	def _on_released(self, background, event):
		if event.button == 1:
			self._show_released()
			self.emit("released", self._value)


class TextButton(ImageButton):
	"""TextButton: As ImageButton but with a text on it.
	"""
	__gtype_name__ = 'TextButton'
	def __init__(self, text, released_background, pressed_background, value=None):
		ImageButton.__init__(self, released_background, pressed_background, value)
		self.text = Clutter.Text(text)
		self.add_actor(self.text)

class PulseButton(Clutter.Group):
	"""PulseButton : button scaling to 1.5 its size during
	a short time to create the effect of pulsing.
	Emit the 'pressed' signal.
	"""
	__gtype_name__ = 'PulseButton'
	__gsignals__ = {
		'pressed' : ( GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_PYOBJECT,) ),
	}

	def __init__(self, background=None, text=None, value=None):
		"""Constructor.
		PulseButton(background, text, value) -> return an instance of PulseButton
		background -> Clutter object to set as background (ex : Texture or Rectangle)
		The background object is the reactive part of the button, when you click on it,
		the signal 'pressed' is emitted.
		text -> string represnting the text to set on the button
		value -> object given in the emitted signal
		"""
		Clutter.Group.__init__(self)
		self._value = value
		self.text = None
		self._background = background or RoundRectangle()
		self._background.set_anchor_point_from_gravity(Clutter.Gravity.CENTER)
		self._press = ScaleAndFadeAnimation(1.5, 0, 50, Clutter.AnimationMode.LINEAR)
		self._press.connect("completed", self._restore)
		self.add_actor(self._background)
		if text:
			self.text = Clutter.Text.new_with_text("courrier new 24px", text)
			self.text.set_anchor_point_from_gravity(Clutter.Gravity.CENTER)
			self.add_actor(self.text)
		self._background.connect("button-press-event", self._on_pressed)
		self._background.set_reactive(True)

	def set_position(self, x, y):
		Clutter.Group.set_position(self, x+self._background.get_width()/2, y+self._background.get_height()/2)

	def _restore(self, *args):
		self.set_scale(1.0, 1.0)
		self.set_opacity(255)

	def _on_pressed(self, background, event):
		if event.button == 1:
			self._press.apply(self)
			self._press.start()
			self.emit("pressed", self._value)


