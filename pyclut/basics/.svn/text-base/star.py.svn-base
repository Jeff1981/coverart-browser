from gi.repository import Cogl, GObject
from pyclut.basics import Shape

class SixBranchStar (Shape):
	"""Simple star shape with six branches.
	"""
	__gtype_name__ = 'SixBranchStar'

	def do_draw_shape(self, width, height):
		Cogl.path_move_to(0, height/4)
		Cogl.path_line_to(width, height/4)
		Cogl.path_line_to(width/2, height)
		Cogl.path_line_to(0, height/4)

		Cogl.path_move_to(0, height*3/4)
		Cogl.path_line_to(width, height*3/4)
		Cogl.path_line_to(width/2, 0)
		Cogl.path_line_to(0, height*3/4)

		Cogl.path_close()


GObject.type_register(SixBranchStar)


