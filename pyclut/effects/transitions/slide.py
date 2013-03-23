from gi.repository import Clutter
from pyclut.effects.transitions import Transition, Direction
from pyclut.animation import MoveAnimation

class SlideTransition(Transition):
	def __init__(self, actor_in, actor_out, zone_object, in_direction=Direction.LEFT, out_direction=Direction.LEFT, final_position=None, duration=500, style=Clutter.AnimationMode.LINEAR):
		Transition.__init__(self, zone_object, actor_in, actor_out, final_position, duration=duration, style=style)
		self._in_direction = in_direction
		self._out_direction = out_direction
		self._duration = duration
		self._style = style

	def __prepare_in_position(self):
		actor_in_width, actor_in_height = self._actor_in.get_size()
		positions = {
			Direction.LEFT : (
				self._zone_size[0]+actor_in_width+10,
				self._final_position[1]
			),
			Direction.RIGHT : (
				-actor_in_width-10,
				self._final_position[1]
			),
			Direction.TOP : (
				self._final_position[0],
				-actor_in_height-10
			),
			Direction.BOTTOM : (
				self._final_position[0],
				self._zone_size[1]+actor_in_height+10
			),
		}
		self._actor_in.set_position(*positions[self._in_direction])
		#self._actor_in.set_opacity(0)

	def __prepare_out_position(self):
		actor_out_width, actor_out_height = self._actor_out.get_size()
		positions = {
			Direction.LEFT : (
				-actor_out_width-10,
				self._final_position[1]
			),
			Direction.RIGHT : (
				self._zone_size[0]+actor_out_width+10,
				self._final_position[1]
			),
			Direction.TOP : (
				self._final_position[0],
				self._zone_size[1]+actor_out_height+10
			),
			Direction.BOTTOM : (
				self._final_position[0],
				-actor_out_height-10
			),
		}
		self._out_final_position = positions[self._out_direction]

	def preset_position(self):
		actor_out_width, actor_out_height = self._actor_out.get_size()
		self._final_position = self._final_position or (self._zone_center[0]-actor_out_width/2,self._zone_center[1]-actor_out_height/2)
		self.__prepare_in_position()
		self.__prepare_out_position()

	def create_animations(self):
		self._actor_in.show()
		anim_in = MoveAnimation(self._final_position, self._duration, self._style)
		anim_out = MoveAnimation(self._out_final_position, self._duration, self._style)
		return anim_in, anim_out

