from gi.repository import Clutter
from pyclut.effects.transitions import Transition, Direction
from pyclut.animation import ScaleAndFadeAnimation

class ZoomTransition(Transition):
	def __init__(self, actor_in, actor_out, duration=500, style=Clutter.AnimationMode.LINEAR):
		Transition.__init__(self, actor_out, actor_in, actor_out, final_position=actor_out.get_position(), duration=duration, style=style)
		self._duration = duration
		self._style = style

	def __prepare_in_position(self):
		self._actor_in.set_position(*self._final_position)
		self._actor_in.set_scale(0.0, 0.0);
		self._actor_in.set_opacity(0)

	def __prepare_out_position(self):
		self._actor_out.set_opacity(255)

	def preset_position(self):
		actor_out_width, actor_out_height = self._actor_out.get_size()
		self._final_position = self._final_position or (self._zone_center[0]-actor_out_width/2,self._zone_center[1]-actor_out_height/2)
		self.__prepare_in_position()
		self.__prepare_out_position()

	def create_animations(self):
		self._actor_in.show()
		anim_in = ScaleAndFadeAnimation(1.0, 255, self._duration, self._style)
		anim_out = ScaleAndFadeAnimation(5.0, 0, self._duration, self._style)
		return anim_in, anim_out



