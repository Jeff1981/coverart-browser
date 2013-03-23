from gi.repository import  Clutter, Cogl

class DoubleFaceTexture(Clutter.Group):
	__gtype_name__ = 'DoubleFaceTexture'

	def __init__(self, front, back):
		Clutter.Group.__init__(self)
		self._front = Clutter.Texture.new_from_file(front)
		self._back = Clutter.Texture.new_from_file(back)
		self._back.set_rotation(Clutter.RotateAxis.Y_AXIS, 180, self._back.get_width()/2, 0, 0)
		self.add_actor(self._back)
		self.add_actor(self._front)

	def do_paint(self):
		cull = Cogl.get_backface_culling_enabled()
		Cogl.set_backface_culling_enabled(True)
		Clutter.Group.do_paint(self)
		Cogl.set_backface_culling_enabled(cull)

