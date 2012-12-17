# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
# Copyright (C) 2012 - fossfreedom
# Copyright (C) 2012 - Agustin Carrasco
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA.

from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import GObject
from gi.repository import Gio
from gi.repository import RB

from coverart_browser_prefs import GSetting
from coverart_utils import ConfiguredSpriteSheet
import rb

ui_string = \
"""<interface>
<object class="GtkMenu" id="popupbutton_menu">
    <property name="visible">True</property>
    <property name="can_focus">False</property>
  </object>
</interface>"""


# generic class from which implementation inherit from
class PopupButton(Gtk.Button):
    # the following vars are to be defined in the inherited classes
    #__gtype_name__ = gobject typename
    #default_image = default image to be displayed

    def __init__(self, **kargs):
        '''
        Initializes the button.
        '''
        super(PopupButton, self).__init__(
            **kargs)

        self._builder = Gtk.Builder()
        self._builder.add_from_string(ui_string)

        self._popup_menu = self._builder.get_object('popupbutton_menu')

        # initialise some variables
        self._first_menu_item = None
        self._current_val = None
        self.is_initialised = False
        self._initial_label = None

    def initialise(self, shell, callback):
        '''
        initialise - derived objects call this first
        shell = rhythmbox shell
        callback = function to call when a menuitem is selected
        '''
        if self.is_initialised:
            return

        self.is_initialised = True

        self.shell = shell
        self.callback = callback
        self.set_popup_value(self.get_initial_label())

        self.resize_button_image()

    def clear_popupmenu(self):
        '''
        reinitialises/clears the current popup menu and associated actions
        '''
        for menu_item in self._popup_menu:
            self._popup_menu.remove(menu_item)

            self._popup_menu.show_all()
            self.shell.props.ui_manager.ensure_update()

        self._first_menu_item = None

    def add_menuitem(self, label, func, val):
        '''
        add a new menu item to the popup
        '''
        if not self._first_menu_item:
            new_menu_item = Gtk.RadioMenuItem(label=label)
            self._first_menu_item = new_menu_item
        else:
            new_menu_item = Gtk.RadioMenuItem.new_with_label_from_widget(
                group=self._first_menu_item, label=label)

        if label == self._current_val:
            new_menu_item.set_active(True)

        new_menu_item.connect('toggled', func, val)
        new_menu_item.show()

        self._popup_menu.append(new_menu_item)

    def show_popup(self):
        '''
        show the current popup menu
        '''
        self._popup_menu.popup(None, None, None, None, 0,
            Gtk.get_current_event_time())

    def set_popup_value(self, val):
        '''
        set the tooltip according to the popup menu chosen
        '''
        if not val:
            val = self.get_initial_label()

        self.set_tooltip_text(val)
        self._current_val = val

    def do_clicked(self):
        '''
        when button is clicked, update the popup with the sorting options
        before displaying the popup
        '''
        self.show_popup()

    def set_initial_label(self, val):
        '''
        all popup's should have a default initial value
        '''
        self._initial_label = val

    def get_initial_label(self):
        '''
        get the first initial value stored in a popup
        '''
        return self._initial_label

    def resize_button_image(self, pixbuf=None):
        '''
        if the button contains an image rather than stock icon
        this function will ensure the image is resized correctly to
        fit the button style
        '''

        what, width, height = Gtk.icon_size_lookup(Gtk.IconSize.BUTTON)
        image = self.get_image()

        try:
            if pixbuf:
                pixbuf = pixbuf.scale_simple(width, height,
                    GdkPixbuf.InterpType.BILINEAR)
            else:
                pixbuf = self.default_image.get_pixbuf().scale_simple(width, height,
                        GdkPixbuf.InterpType.BILINEAR)

            image.set_from_pixbuf(pixbuf)
        except:
            pass

    def do_delete_thyself(self):
        self.clear_popupmenu()
        del self._popupmenu
        del self._actiongroup
        del self._builder


class PlaylistPopupButton(PopupButton):
    __gtype_name__ = 'PlaylistPopupButton'
    _library_name = _("Music Library")
    _queue_name = _("Play Queue")

    def __init__(self, **kargs):
        '''
        Initializes the button.
        '''
        super(PlaylistPopupButton, self).__init__(
            **kargs)

        #self.default_image = Gtk.Image.new_from_file('img/icon_playlist.png')
        self.set_initial_label(self._library_name)

        #weird introspection - do_clicked is overridden but
        #PopupButton version is called not the Playlist version
        #connect the clicked event to this version
        self.connect('clicked', self.do_clicked)

    def initialise(self, plugin, shell, callback):
        '''
        extend the default initialise function
        because we need to also resize the picture
        associated with the playlist button
        '''
        if self.is_initialised:
            return

        self._spritesheet = ConfiguredSpriteSheet(plugin, 'playlist')
        self.default_image = Gtk.Image.new_from_pixbuf(self._spritesheet['music'])
        
        super(PlaylistPopupButton, self).initialise(shell, callback)

    def do_clicked(self, button):
        '''
        we need to create the playlist first before showing
        the popup
        N.B. see comment above
        '''
        playlist_manager = self.shell.props.playlist_manager
        playlists_entries = playlist_manager.get_playlists()
        self.clear_popupmenu()
        self.add_menuitem(self.get_initial_label(),
            self._change_playlist_source, None)
        self.add_menuitem(self._queue_name,
            self._change_playlist_source, self.shell.props.queue_source)

        if playlists_entries:
            for playlist in playlists_entries:
                if playlist.props.is_local:
                    self.add_menuitem(playlist.props.name,
                        self._change_playlist_source, playlist)

        self.show_popup()

    def _change_playlist_source(self, menu, playlist):
        '''
        when a popup menu item is chosen change the button tooltip
        before invoking the source callback function
        '''
        if menu.get_active():
            if not playlist:
                model = None
                self.set_popup_value(self.get_initial_label())
                self.resize_button_image(self._spritesheet['music'])
            elif self._queue_name in playlist.props.name:
                model = playlist.get_query_model()
                self.set_popup_value(self._queue_name)
                self.resize_button_image(self._spritesheet['queue'])
            else:
                model = playlist.get_query_model()
                self.set_popup_value(playlist.props.name)
                if isinstance(playlist, RB.StaticPlaylistSource):
                    self.resize_button_image(self._spritesheet['playlist'])
                else:
                    self.resize_button_image(self._spritesheet['smart'])
                
            self.callback(model)


class GenrePopupButton(PopupButton):
    __gtype_name__ = 'GenrePopupButton'

    def __init__(self, **kargs):
        '''
        Initializes the button.
        '''
        super(GenrePopupButton, self).__init__(
            **kargs)

    def initialise(self, plugin, shell, callback):
        '''
        extend the default initialise function
        because we need to also resize the picture
        associated with the genre button
        '''
        if self.is_initialised:
            return

        self._spritesheet = ConfiguredSpriteSheet(plugin, 'genre')
        self.default_image = Gtk.Image.new_from_file(rb.find_plugin_file(plugin,'img/genre.png'))
        
        self.set_initial_label('All')
        super(GenrePopupButton, self).initialise(shell, callback)

        # seems like view [0] is the genre property view
        model = self.shell.props.library_source.get_property_views()[0].\
            get_model()

        # connect signals to update genres
        model.connect('row-inserted', self._update_popup)
        model.connect('row-deleted', self._update_popup)
        model.connect('row-changed', self._update_popup)

        # generate initial popup
        self._update_popup(model)

    def _update_popup(self, model, *args):
        still_exists = False
        current = self._current_val

        # clear and recreate popup
        self.clear_popupmenu()

        for row in model:
            genre = row[0]
            self.add_menuitem(genre, self._genre_changed, genre)

            still_exists = still_exists or genre == current

        if not still_exists:
            self._genre_changed(None, 'All')

    def _genre_changed(self, menu, genre):
        '''
        called when genre popup menu item chosen
        return None if the first entry in popup returned
        '''
        if not menu or menu.get_active():
            self.set_popup_value(genre)

            test_genre = genre.lower()
            
            self.resize_button_image(self._spritesheet[test_genre])
                
            if genre == self.get_initial_label():
                self.callback(None)
            else:
                self.callback(genre)


class SortPopupButton(PopupButton):
    __gtype_name__ = 'SortPopupButton'

    sorts = {'name': _('Sort by album name'),
        'album_artist': _('Sort by album artist'),
        'year': _('Sort by year'),
        'rating': _('Sort by rating')}

    sort_by = GObject.property(type=str)

    def __init__(self, **kargs):
        '''
        Initializes the button.
        '''
        super(SortPopupButton, self).__init__(
            **kargs)

        #self.default_image = Gtk.Image.new_from_file('img/sort.png')
        self.set_initial_label(self.sorts['name'])

    def initialise(self, plugin, shell, callback):
        '''
        extend the default initialise function
        because we need to also resize the picture
        associated with the sort button as well as find the
        saved sort order
        '''
        if self.is_initialised:
            return

        self._spritesheet = ConfiguredSpriteSheet(plugin, 'sort')
        #self.default_image = Gtk.Image.new_from_pixbuf(self._spritesheet['name'])

        super(SortPopupButton, self).initialise(shell, callback)

        # create the pop up menu
        for key, text in sorted(self.sorts.iteritems()):
            self.add_menuitem(text, self._sort_changed, key)

        gs = GSetting()
        source_settings = gs.get_setting(gs.Path.PLUGIN)
        source_settings.bind(gs.PluginKey.SORT_BY,
            self, 'sort_by', Gio.SettingsBindFlags.DEFAULT)

        self._sort_changed(None, self.sort_by)

    def _sort_changed(self, menu, sort):
        '''
        called when sort popup menu item chosen
        '''
        if not menu or menu.get_active():
            self.set_popup_value(self.sorts[sort])
            self.sort_by = sort

            self.resize_button_image(self._spritesheet[sort])
            
            self.callback(sort)


class ImageToggleButton(Gtk.Button):
    '''
    generic class from which implementation inherit from
    '''
    # the following vars are to be defined in the inherited classes
    #__gtype_name__ = gobject typename

    def __init__(self, **kargs):
        '''
        Initializes the button.
        '''
        super(ImageToggleButton, self).__init__(
            **kargs)

        # initialise some variables
        self.image_display = False
        self.is_initialised = False

    def initialise(self, callback, image1, image2):
        '''
        initialise - derived objects call this first
        callback = function to call when button is clicked
        image1 = by default (image_display is True), first image displayed
        image2 = (image display is False), second image displayed
        '''
        if self.is_initialised:
            return

        self.is_initialised = True

        self.callback = callback
        self._image1 = image1
        self._image2 = image2
        self._image1_pixbuf = self._resize_button_image(self._image1)
        self._image2_pixbuf = self._resize_button_image(self._image2)

        self._update_button_image()

    def on_clicked(self):
        self.image_display = not self.image_display
        self._update_button_image()
        self.callback(self.image_display)

    def _update_button_image(self):
        image = self.get_image()

        if image:
            if self.image_display:
                image.set_from_pixbuf(self._image1_pixbuf)
            else:
                image.set_from_pixbuf(self._image2_pixbuf)

    def _resize_button_image(self, image):
        '''
        this function will ensure the image is resized correctly to
        fit the button style
        '''

        what, width, height = Gtk.icon_size_lookup(Gtk.IconSize.BUTTON)

        pixbuf = None
        try:
            pixbuf = image.get_pixbuf().scale_simple(width, height,
                    GdkPixbuf.InterpType.BILINEAR)
        except:
            pass

        return pixbuf

    def do_delete_thyself(self):
        del self._image1_pixbuf
        del self._image2_pixbuf


class SortOrderButton(ImageToggleButton):
    __gtype_name__ = 'SortOrderButton'

    def __init__(self, **kargs):
        '''
        Initializes the button.
        '''
        super(SortOrderButton, self).__init__(
            **kargs)

        self.gs = GSetting()

    def initialise(self, plugin, callback, sort_order):
        '''
        set up the images we will use for this widget
        '''

        self.image_display = sort_order
        self.set_tooltip(self.image_display)

        if not self.is_initialised:
            image1 = Gtk.Image.new_from_file(rb.find_plugin_file(plugin,
            'img/arrow_up.png'))
            image2 = Gtk.Image.new_from_file(rb.find_plugin_file(plugin,
            'img/arrow_down.png'))

            super(SortOrderButton, self).initialise(callback,
               image1, image2)

    def do_clicked(self):

        val = not self.image_display
        self.gs.set_value(self.gs.Path.PLUGIN,
                    self.gs.PluginKey.SORT_ORDER, val)
        self.set_tooltip(val)
        self.on_clicked()

    def set_tooltip(self, val):
        if not val:
            self.set_tooltip_text(_('Sort in descending order'))
        else:
            self.set_tooltip_text(_('Sort in ascending order'))