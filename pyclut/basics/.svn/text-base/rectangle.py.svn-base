import sys
from gi.repository import Cogl, GObject
from pyclut.basics import Shape

class RoundRectangle(Shape):
	"""Rectangle Shape with rounded corner.
	You can set the radius property to change the rounded radius
	of corners (default is 10).
	"""
	__gtype_name__ = 'RoundRectangle'
	__gproperties__ = {
		'color' : (
			str, 'color', 'Color', None, GObject.PARAM_READWRITE
		),
		'radius': (
			GObject.TYPE_INT, 'Radius', 'Radius of the round angles',
			0, 360, 0, GObject.PARAM_READWRITE
		),
		'border_color': (
			str, 'border color', 'Border color', None, GObject.PARAM_READWRITE
		),
		'border_width' : (
			GObject.TYPE_FLOAT, 'border width', 'Border width',
			0.0, 360, 0.0, GObject.PARAM_READWRITE
		),
	}
	def __init__ (self):
		Shape.__init__(self)
		self._radius = 10

	def set_radius(self, radius):
		"""Change the radius of corners.
		radius must be an integer.
		"""
		self._radius = radius

	def do_set_property (self, pspec, value):
		if pspec.name == 'radius':
			self.set_radius(value)
		else:
			raise TypeError('Unknown property ' + pspec.name)

	def do_get_property (self, pspec):
		if pspec.name == 'radius':
			return self._radius
		else:
			raise TypeError('Unknown property ' + pspec.name)

	def do_draw_shape(self, width, height):
		Cogl.path_round_rectangle (0, 0, width, height, self._radius, 5)

		Cogl.path_close()


GObject.type_register(RoundRectangle)



