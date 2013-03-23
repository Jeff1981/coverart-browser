from gi.repository import Clutter
from pyclut.animation import DepthAnimation
from pyclut.effects.transitions.slide import SlideTransition
from pyclut.effects.transitions import Direction


class PageFullError(Exception):
	pass

class ThumbnailPage(Clutter.Group):
	__gtype_name__ = 'ThumbnailPage'
	def __init__(self, size=(512, 512), max_row=2, max_column=2, selection_depth=75, item_size=(128, 128), inter_item_space=10):
		Clutter.Group.__init__(self)
		self._max_item = max_row * max_column
		self._max_row = max_row
		self._max_column = max_column
		self._selection_depth = selection_depth
		self._selected = -1
		self._item_size = item_size
		self._width = size[0]
		self._height = size[1]
		self._inter_item_space = inter_item_space
		self._children=[]

	def add_actor(self, *children):
		if self.is_full():
			raise PageFullError()
		[child.set_size(*self._item_size) for child in children]
		self._children+=children
		Clutter.Group.add_actor(self, *children)
		self.__update()

	def __update(self):
		i=0
		delta_y = (self._item_size[1] + self._inter_item_space)
		delta_x = (self._item_size[0] + self._inter_item_space)
		y = self._height - (self._max_row * delta_y)
		try:
			for r in range(self._max_row):
				x = self._width - (self._max_column * delta_x)
				for c in range(self._max_column):
					self._children[i].set_position(x, y)
					i+=1
					x+=delta_x
				y+=delta_y
		except IndexError:
			pass
		self.select(self._selected)

	def _select_item(self, selected):
		try:
			self._selected = selected
			if selected >=0:
				anim = DepthAnimation(self._selection_depth, duration=200, style=Clutter.AnimationMode.LINEAR)
				anim.apply(self._children[selected])
				anim.start()
		except IndexError:
			self._selected = 0

	def _unselect_items(self, selected):
		anims=[]
		for i,item in enumerate(self._children):
			if i != selected:
				anim = DepthAnimation(0, duration=200, style=Clutter.AnimationMode.LINEAR)
				anim.apply(item)
				anims.append(anim)
		[anim.start() for anim in anims]

	def select(self, index_):
		self._select_item(index_)
		self._unselect_items(index_)

	def next(self):
		self.select((self._selected + 1)%len(self._children))

	def previous(self):
		self.select((self._selected - 1)%len(self._children))

	def is_empty(self):
		return (len(self._children) == 0)

	def is_full(self):
		return (len(self._children) >= self._max_item)

	def get_selected(self):
		return self._selected

class ThumbnailMenu(Clutter.Group):
	__gtype_name__ = 'ThumbnailMenu'
	def __init__(self, x=0, y=0, item_size=(128, 128), row=2, column=2, selection_depth=200, inter_item_space=10, *children):
		Clutter.Group.__init__(self)
		self._x = x
		self._y = y
		self._selected = 0
		width = (item_size[0] + inter_item_space) * column
		height = (item_size[1] + inter_item_space) * row
		self._args = (width, height), row, column, selection_depth, item_size, inter_item_space
		self._item_by_page = row * column
		self._current_page = ThumbnailPage(*self._args)
		self._current_page.show()
		self._current_page_index = 0
		self._pages = [self._current_page, ]
		Clutter.Group.add_actor(self, self._current_page)
		self._nb_children=0
		if children:
			self.add_actor(*children)

	def add_actor(self, *children):
		last_page = self._pages[-1]
		for child in children:
			try:
				last_page.add_actor(child)
			except PageFullError:
				last_page = ThumbnailPage(*self._args)
				last_page.hide()
				self._pages.append(last_page)
				Clutter.Group.add_actor(self, last_page)
				last_page.add_actor(child)

	def next(self):
		self._current_page.next()

	def previous(self):
		self._current_page.previous()

	def next_page(self):
		self._current_page_index = (self._current_page_index + 1) % len(self._pages)
		next_page = self._pages[self._current_page_index]
		self._current_page.select(-1)
		transition = SlideTransition(
			next_page,
			self._current_page,
			self,
			in_direction=Direction.LEFT,
			out_direction=Direction.LEFT,
			final_position=(self._x, self._y),
		)
		self._current_page = next_page
		transition.start()

	def previous_page(self):
		self._current_page_index = (self._current_page_index - 1) % len(self._pages)
		previous_page = self._pages[self._current_page_index]
		self._current_page.select(-1)
		transition = SlideTransition(
			previous_page,
			self._current_page,
			self,
			in_direction=Direction.RIGHT,
			out_direction=Direction.RIGHT,
			final_position=(self._x, self._y),
		)
		self._current_page = previous_page
		transition.start()



