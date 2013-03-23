from gi.repository import Clutter
from pyclut.effects.transitions import Transition
from pyclut.animation import RotateAnimation, OpacityAnimation

class RotateAndFadeAnimation(RotateAnimation, OpacityAnimation):
	def __init__(self, angle, axis, direction, opacity, duration, style, center, timeline=None, alpha=None):
		RotateAnimation.__init__(self, angle, axis, direction, duration, style, center, timeline=timeline, alpha=alpha)
		OpacityAnimation.__init__(self, opacity, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = RotateAnimation.do_prepare_animation(self)
		behaviours.extend(OpacityAnimation.do_prepare_animation(self))
		return behaviours

class RotateTransition(Transition):
	def __init__(self, actor_in, actor_out, direction=Clutter.RotateDirection.CW, axis=Clutter.RotateAxis.Y_AXIS, final_position=None, center=None, duration=500, style=Clutter.AnimationMode.LINEAR):
		Transition.__init__(self, actor_out, actor_in, actor_out, final_position=final_position or actor_in.get_position(), duration=duration, style=style, backface_culling=True)
		self._axis = axis
		self._direction = direction
		self._duration = duration
		self._style = style
		self._center = center

	def __prepare_in_position(self):
		self._actor_in.set_position(*self._final_position)
		self._actor_in.set_rotation(self._axis, 180.0, 0.0, 0.0, 0.0)
		self._actor_in.set_opacity(0)

	def __prepare_out_position(self):
		self._actor_out.set_rotation(self._axis, 0.0, 0.0, 0.0, 0.0)
		self._actor_out.set_opacity(255)

	def preset_position(self):
		actor_out_width, actor_out_height = self._actor_out.get_size()
		self._final_position = self._final_position or (self._zone_center[0]-actor_out_width/2,self._zone_center[1]-actor_out_height/2)
		self.__prepare_in_position()
		self.__prepare_out_position()

	def create_animations(self):
		anim_in = RotateAndFadeAnimation(0, self._axis, self._direction, 255, self._duration, self._style, self._center)
		anim_out = RotateAndFadeAnimation(-180, self._axis, self._direction, 0, self._duration, self._style, self._center)
		return anim_in, anim_out

class FlapTransition(RotateTransition):
	def __init__(self, actor_in, actor_out, duration=500):
		RotateTransition.__init__(self, actor_in, actor_out, direction=Clutter.RotateDirection.CW, axis=Clutter.RotateAxis.X_AXIS, final_position=actor_in.get_position(), center=(0, 0, 0), duration=duration, style=Clutter.AnimationMode.EASE_OUT_BOUNCE)


