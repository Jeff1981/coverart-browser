from gi.repository import Clutter, Cogl, GObject
import random

from datetime import datetime
from pyclut.basics.rectangle import RoundRectangle
from pyclut.effects.transitions.rotate import FlapTransition

class Flap(Clutter.Group):
	__gtype_name__ = 'Flap'
	def __init__(self, value, size, font, background_color="White", text_color="Black"):
		Clutter.Group.__init__(self)
		if background_color:
			self.background = RoundRectangle()
			self.background.set_size(*size)
			color = Clutter.Color()
			color.from_string(background_color)
			self.background.set_color(color)
			self.add_actor(self.background)
		self.text = Clutter.Text.new_with_text(font, "%02d" % value)
		txt_color = Clutter.Color()
		txt_color.from_string(text_color)
		self.text.set_color(txt_color)
		self.text.set_position(
			(size[0]/2)-(self.text.get_width()/2),
			(size[1]/2)-(self.text.get_height()/2)
		)
		self.add_actor(self.text)

class HalfFlap(Flap):
	__gtype_name__ = 'HalfFlap'
	def __init__(self, value, size, font, top_part=True, background_color="White", text_color="Black"):
		Flap.__init__(self, value, size, font, background_color, text_color)
		self.background.set_clip(0, 0, size[0], size[1]/2)
		if top_part:
			self.text.set_clip(0, 0, size[0], size[1]/2)
		else:
			self.text.set_clip(0, size[1]/2, size[0], size[1]/2)


class FlapClock(Clutter.Group):
	__gtype_name__ = 'FlapClock'

	def __init__(self, font="Arial 48px", flap_size=(70, 60)):
		Clutter.Group.__init__(self)
		self._font = font
		self._flap_size = flap_size
		self._number_values = 3*[0,]
		self._inter_space = 10
		self._flaps = []
		self._update_numbers()
		self._create_flaps()
		GObject.timeout_add_seconds(1, self.on_tick)

	def _create_flap(self, rank, value):
		flap = Flap(value, self._flap_size, self._font)
		flap.set_position(rank*(self._flap_size[0]+self._inter_space), 0)
		return flap

	def _create_flaps(self):
		for rank, num in enumerate(self._number_values):
			flap = self._create_flap(rank, num)
			self._flaps.append(flap)
			self.add_actor(flap)

	def _update_numbers(self):
		now = datetime.now()
		old_numbers = self._number_values
		#self._number_values = [now.hour/10, now.hour%10, now.minute/10, now.minute%10, now.second/10, now.second%10]
		self._number_values = [now.hour, now.minute, now.second]
		return [new != old for new, old in zip(self._number_values, old_numbers)]

	def _update_number(self, rank, new_value):
		new_flap = self._create_flap(rank, new_value)
		self.add_actor(new_flap)
		old_flap = self._flaps[rank]
		self._flaps[rank] = new_flap
		transition = FlapTransition(
			actor_in=new_flap,
			actor_out=old_flap,
			duration=random.randint(200, 500),
		)
		transition.connect("completed", self._on_transition_done, rank, old_flap)
		return transition, rank, old_flap

	def _on_transition_done(self, event, rank, old_flap):
		self.remove_actor(old_flap)

	def do_refresh_clock(self, as_changed):
		transitions = []
		for rank, (value, animate) in enumerate(zip(self._number_values, as_changed)):
			if animate:
				transitions.append(self._update_number(rank, value))
		[transition.start() for transition, rank, _ in transitions]

	def on_tick(self):
		self.do_refresh_clock(self._update_numbers())
		return True

class DoubleFlap(Clutter.Group):
	__gtype_name__ = 'DoubleFlap'
	def __init__(self, value, size, font, background_color="White", text_color="Black"):
		Clutter.Group.__init__(self)
		self.top = HalfFlap(value, size, font, background_color, text_color)
		self.bottom = HalfFlap(value, size, font, False, background_color, text_color)
		self.bottom.set_rotation(Clutter.RotateAxis.Y_AXIS, 180, self.bottom.get_width()/2, 0, 0)
		self.add_actor(self.top)
		self.add_actor(self.bottom)


class FlipClock(FlapClock):
	__gtype_name__ = 'FlipClock'

	def __init__(self, font="Arial 48px", flap_size=(70, 60)):
		Clutter.Group.__init__(self)
		self._font = font
		self._flap_size = flap_size
		self._number_values = 3*[0,]
		self._inter_space = 10
		self._flaps = []
		self._update_numbers()
		self._create_flaps()
		GObject.timeout_add_seconds(1, self.on_tick)

	def _create_flap(self, rank, value):
		flap = DoubleFlap(value, self._flap_size, self._font)
		flap.set_position(rank*(self._flap_size[0]+self._inter_space), 0)
		return flap

	def _update_number(self, rank, new_value):
		new_flap = self.__create_flap(rank, new_value)
		self.add_actor(new_flap)
		old_flap = self._flaps[rank]
		self._flaps[rank] = new_flap
		transition = FlapTransition(
			actor_in=new_flap,
			actor_out=old_flap,
			duration=random.randint(200, 500),
		)
		transition.connect("completed", self._on_transition_done, rank, old_flap)
		return transition, rank, old_flap


