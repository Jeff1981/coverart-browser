from gi.repository import Clutter, Cogl, GObject

class TextureReflection (Clutter.Clone):
	__gtype_name__ = 'TextureReflection'

	def __init__ (self, parent):
		Clutter.Clone.__init__(self, parent)
		self._reflection_height = -1

	def set_reflection_height (self, height):
		self._reflection_height = height
		self.queue_redraw()

	def get_reflection_height (self):
		return self._reflection_height

	def do_paint (self):
		parent = self.get_source()
		if (parent is None):
			return
		print parent
		print parent.get_cogl_texture()
		# get the Cogl handle for the parent texture
#		Cogl_tex = parent.get_cogl_texture()
#		if not Cogl_tex:
#			return

#		(width, height) = self.get_size()
#
#		# clamp the reflection height if needed
#		r_height = self._reflection_height
#		if (r_height < 0 or r_height > height):
#			r_height = height
#
#		rty = float(r_height / height)
#
#		opacity = self.get_paint_opacity()
#
#		# the vertices are a 6-tuple composed of:
#		#  x, y, z: coordinates inside Clutter modelview
#		#  tx, ty: texture coordinates
#		#  color: a Clutter.Color for the vertex
#		#
#		# to paint the reflection of the parent texture we paint
#		# the texture using four vertices in clockwise order, with
#		# the upper left and the upper right at full opacity and
#		# the lower right and lower left and 0 opacity; OpenGL will
#		# do the gradient for us
#		color1 = Cogl.color_premultiply((1, 1, 1, opacity/255.))
#		color2 = Cogl.color_premultiply((1, 1, 1, 0))
#		vertices = ( \
#			(    0,        0, 0, 0.0, 1.0,   color1), \
#			(width,        0, 0, 1.0, 1.0,   color1), \
#			(width, r_height, 0, 1.0, 1.0-rty, color2), \
#			(    0, r_height, 0, 0.0, 1.0-rty, color2), \
#		)
#
#		Cogl.push_matrix()
#
#		Cogl.set_source_texture(Cogl_tex)
#		Cogl.polygon(vertices=vertices, use_color=True)
#
#		Cogl.pop_matrix()

class ReflectedItem(Clutter.Group):
	__gtype_name__ = 'ReflectedItem'

	def __init__(self, object):
		Clutter.Actor.__init__(self)
		self._object = object
		self.add_actor(self._object)
		self._create_reflection()

	def _create_reflection(self):
		self._reflect = TextureReflection(self._object)
		self.add_actor(self._reflect)
		self._reflect.set_position(0, self._object.get_height()+10)


class RotatingItem(ReflectedItem):
	__gtype_name__ = 'RotatingItem'
	def __init__(self, object):
		ReflectedItem.__init__(self, object)
		self.timeline = Clutter.Timeline(duration=3000)
		self.timeline.set_loop(True)
		self.alpha = Clutter.Alpha(self.timeline, Clutter.AnimationMode.LINEAR)
		self.behaviour = Clutter.BehaviourRotate(Clutter.AlignAxis.Y_AXIS, 0.0, 360.0, self.alpha, Clutter.RotateDirection.CW)
		self.behaviour.set_center(int(object.get_width()/2), 0, 0)
		self.behaviour.apply(self)
		self.timeline.start()



