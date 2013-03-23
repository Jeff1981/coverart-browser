from gi.repository import Cogl, GObject
from pyclut.basics import Shape

class Triangle (Shape):
    __gtype_name__ = 'Triangle'
    def do_draw_shape(self, width, height):
        Cogl.path_move_to(width / 2, 0)
        Cogl.path_line_to(width, height)
        Cogl.path_line_to(0, height)
        Cogl.path_line_to(width / 2, 0)
        Cogl.path_close()

GObject.type_register(Triangle)


