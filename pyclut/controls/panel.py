from gi.repository import Clutter


class Panel(Clutter.Group):
	__gtype_name__ = 'Panel'

	def __init__(self, size, background, *children):
		Clutter.Group.__init__(self)
		if type(background) is str:
			self._background = Clutter.Rectangle()
			self._background.set_color(Clutter.Color.from_string(background))
		else:
			self._background = background
		self._background.set_size(*size)
		self.add_actor(self._background)
		if children:
			self.add_actor(*children)

	def show(self):
		print "show panel"
		Clutter.Group.show(self)
		for i in range(self.get_n_children()):
			self.get_nth_child(i).show()
		
	def hide(self):
		print "hide panel"
		Clutter.Group.hide(self)
		for i in range(self.get_n_children()):
			self.get_nth_child(i).hide()
		
	def get_background(self):
		return self._background


