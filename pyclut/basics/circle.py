from gi.repository import Clutter, Cogl, GObject
from pyclut.basics import Shape

class Circle(Shape):
	"""Circle Shape.
	You can set the radius property to change the rounded radius
	of corners (default is 10).
	"""
	__gtype_name__ = 'Circle'
	__gproperties__ = {
	  'radius' : (GObject.TYPE_INT, 'Radius', 'circle radius',
                0, 1, 0, GObject.PARAM_READWRITE),
	  'angle-start' : (GObject.TYPE_INT, 'Angle start', 'angle start',
                0, 360, 0, GObject.PARAM_READWRITE),
	  'angle-end' : (GObject.TYPE_INT, 'Angle end', 'angle end',
                0, 360, 0, GObject.PARAM_READWRITE),
	}
	def __init__ (self):
		Shape.__init__(self)
		self._radius = 10
		self._angle_start = 0
		self._angle_end = 360

	def do_set_property (self, pspec, value):
		try:
			setattr(self, "_%s" % pspec.name.replace("-", "_"), value)
		except AttributeError:
			raise TypeError('Unknown property ' + pspec.name)

	def do_get_property (self, pspec):
		try:
			return getattr(self, "_%s" % pspec.name.replace("-", "_"))
		except AttributeError:
			raise TypeError('Unknown property ' + pspec.name)

	def do_draw_shape(self, width, height):
		Cogl.path_arc(
			center_x=0,
			center_y=0,
			radius_x=self._radius,
			radius_y=self._radius,
			angle_1=self._angle_start,
			angle_2=self._angle_end
		)
		Cogl.path_fill()
		Cogl.path_close()
		self.queue_relayout()


GObject.type_register(Circle)

class CircleChrono(Circle):
	__gtype_name__ = 'CircleChrono'
	__gsignals__ = {
		'completed' : ( \
		  GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, () \
		),
	}
	def __init__(self, duration=5000):
		Circle.__init__(self)
		self._angle_end = 0
		self._duration = duration

	def start(self, loop=False):
		animation = self.animate(Clutter.AnimationMode.LINEAR, self._duration, "angle_end", 360)
		animation.set_loop(True)
		animation.connect('completed', self._on_done, loop)
		print dir(animation)

	def reset(self):
		self._angle_end = 0

	def _on_done(self, event, loop):
		self.emit("completed")


#         ClutterFixed	 dw, dh;
#         ClutterCircle	 *circle = CLUTTER_CIRCLE(self);
#         ClutterCirclePrivate	 *priv;
#         ClutterGeometry	 geom;
#         ClutterColor	 tmp_col;
#         ClutterFixed	 precision = 2;
#         circle = CLUTTER_CIRCLE(self);
#         priv = circle->priv;
#         Clutter_actor_get_allocation_geometry (self, &geom);
#         tmp_col.red = priv->color.red;
#         tmp_col.green = priv->color.green;
#         tmp_col.blue = priv->color.blue;
#         tmp_col.alpha = Clutter_actor_get_paint_opacity (self)
#                 * priv->color.alpha
#                 / 255;
#         Cogl_color (&tmp_col);
#         if ( priv->radius == 0 )
#                 Clutter_circle_set_radius(circle, geom.width);
#         dw = CLUTTER_INT_TO_FIXED(geom.width) >> 1;
#         dh = CLUTTER_INT_TO_FIXED(geom.height) >> 1;
#         Cogl_path_move_to(dw, dh);
#         cc_Cogl_path_arc(dw, dh,
#                 CLUTTER_INT_TO_FIXED(priv->radius),
#                 CLUTTER_INT_TO_FIXED(priv->radius),
#                 CLUTTER_ANGLE_FROM_DEG(priv->angle_start + 270),
#                 CLUTTER_ANGLE_FROM_DEG(priv->angle_stop + 270),
#                 precision, 1
#         );
#         if ( priv->width != 0 )
#         {
#                 cc_Cogl_path_arc(dw, dh,
#                         CLUTTER_INT_TO_FIXED(priv->radius + priv->width),
#                         CLUTTER_INT_TO_FIXED(priv->radius + priv->width),
#                         CLUTTER_ANGLE_FROM_DEG(priv->angle_stop + 270),
#                         CLUTTER_ANGLE_FROM_DEG(priv->angle_start + 270),
#                         precision, 0
#                 );
#         }
#         Cogl_path_close();
#         /* fill path
#          */
#         Cogl_path_fill();
#         /* and stroke border
#          */
#     glEnable(GL_LINE_SMOOTH);
#     glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE);
#     glLineWidth(1.5);
#         Cogl_path_stroke();
#         glDisable(GL_LINE_SMOOTH);

