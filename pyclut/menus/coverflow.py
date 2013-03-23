from gi.repository import Clutter
from pyclut.animation import MoveAnimation, RotateAnimation, ScaleAnimation, DepthAnimation
from pyclut.utils import clamp_angle


class CoverflowItemAnimation(MoveAnimation, RotateAnimation, ScaleAnimation, DepthAnimation):
	def __init__(self, destination, angle, axis, direction, scale, depth, duration, style, timeline=None, alpha=None):
		MoveAnimation.__init__(self, destination, duration, style, timeline=timeline, alpha=alpha)
		RotateAnimation.__init__(self, angle, axis, direction, duration, style, timeline=self._timeline, alpha=self._alpha)
		ScaleAnimation.__init__(self, scale, scale, duration, style, timeline=self._timeline, alpha=self._alpha)
		DepthAnimation.__init__(self, depth, duration, style, timeline=self._timeline, alpha=self._alpha)

	def do_prepare_animation(self):
		behaviours = MoveAnimation.do_prepare_animation(self)
		if clamp_angle(self._actor.get_rotation(self._axis)[0]) != clamp_angle(self._angle):
			behaviours.extend(RotateAnimation.do_prepare_animation(self))
		behaviours.extend(ScaleAnimation.do_prepare_animation(self))
		behaviours.extend(DepthAnimation.do_prepare_animation(self))
		return behaviours

class Coverflow(Clutter.Group):
	"""Coverflow menu is a list of items on a line rotated if not selected."""
	__gtype_name__ = 'Coverflow'
	def __init__(self, x=0, y=0, size=(512, 128), item_size=(128, 128), angle=70, inter_item_space=50, selection_depth=200, *children):
		"""Constructor
		Coverflow(x, y, size, item_size, angle, inter_item_space, selection_depth, *children) -> Coverflow instance
		x, y : coverflow position (default is x=0, y=0)
		size : witdh and height of the carrousel (default is (512, 512))
		item_size : width and height of a menu item (default is (128, 128))
		angle : rotation angle of unselected items (default is 70)
		inter_item_space : space between two items (default is 50)
		selection_depth : selected item is bring to front (default is 200)
		children : optional list of item to add to the menu.
		"""
		Clutter.Group.__init__(self)
		self._x = x
		self._y = y
		self._width = size[0]
		self._height = size[1]
		self._item_size = item_size
		self._selected = 0
		self._inter_item_space = inter_item_space
		self._angle = angle
		self._selection_depth = selection_depth
		self._children = []
		self.set_reactive(True)
		if children:
			self.add_actor(*children)

	def show(self):
		self.set_scale(0, 0)
		Clutter.Group.show(self)
		anim = ScaleAnimation(scale_x=1.0, scale_y=1.0, duration=1000, style=Clutter.AnimationMode.EASE_OUT_BACK)
		anim.apply(self)
		anim.start()

	def hide(self):
		anim = ScaleAnimation(scale_x=0.0, scale_y=0.0, duration=1000, style=Clutter.AnimationMode.EASE_IN_BACK)
		anim.apply(self)
		anim.start()

	def add_actor(self, *children):
		"""Add a list of items to the coverflow menu.
		coverflow.add_actor(item1, item2, item3) -> return None
		"""
		print children
		[child.set_size(*self._item_size) for child in children]
		self.do_add_actor(*children)
		[super(Coverflow, self).add_actor(child) for child in children]

	def do_add_actor(self, *children):
		for child in children:
			self._children.append(child)
		self.__update_items_position()

	def remove(self, *children):
		Clutter.Group.remove(self, *children)
		self.do_remove(*children)

	def do_remove(self, *children):
		for child in children:
			if child in self._children:
				self._children.remove(child)
		self.__update_items_position()

	def __apply_animation(self, item, destination, angle, direction, depth):
		anim = CoverflowItemAnimation(
			destination=(destination, self._y),
			angle=angle,
			axis=Clutter.RotateAxis.Y_AXIS,
			direction=direction,
			scale=1.0,
			depth=depth,
			duration=200,
			style=Clutter.AnimationMode.EASE_IN_OUT_SINE
		)
		anim.apply(item)
		return anim

	def __update_items_position(self, selected_rotation=Clutter.RotateDirection.CW):
		center_x = self._x + self._width/2
		anims=[]
		for index, item in enumerate(self._children[:self._selected]):
			anims.append(self.__apply_animation(
				item=item,
				destination=(center_x - (self._item_size[0]/2) - (self._inter_item_space*((self._selected-index)+1))),
				angle=self._angle,
				direction=Clutter.RotateDirection.CW,
				depth=0.0))

		anims.append(self.__apply_animation(
			item=self._children[self._selected],
			destination=(center_x - self._item_size[0]/2),
			angle=0,
			direction=selected_rotation,
			depth=self._selection_depth))

		if self._selected < (len(self._children)-1):
			for index, item in enumerate(self._children[self._selected+1:]):
				anims.append(self.__apply_animation(
					item=item,
					destination=(center_x + (self._item_size[0]/2) + (self._inter_item_space*(index+1))),
					angle=360-self._angle,
					direction=Clutter.RotateDirection.CCW,
					depth=0.0))
		anims[-1].connect("completed", self._on_anim_completed)
		[anim.start() for anim in anims]

	def _on_anim_completed(self, event):
		self.set_reactive(True)

	def next(self):
		"""Select the next item.
		coverflow.next() -> return None
		"""
		if self.get_reactive():
			self.set_reactive(False)
			self._selected = min(self._selected + 1,len(self._children)-1)# % len(self._children)
			self.__update_items_position(Clutter.RotateDirection.CW)

	def previous(self):
		"""Select the previous item.
		coverflow.next() -> return None
		"""
		if self.get_reactive():
			self.set_reactive(False)
			self._selected = max(self._selected - 1, 0)# % len(self._children)
			self.__update_items_position(Clutter.RotateDirection.CCW)

	def get_selected(self):
		"""Return the rank of the selected item.
		coverflow.get_selected() -> return integer
		"""
		return self._selected


