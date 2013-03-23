# -*- Mode: python; coding: utf-8; tab-width: 4; indent-tabs-mode: nil; -*-
#
# Copyright (C) 2012 - fossfreedom
# Copyright (C) 2012 - Agustin Carrasco
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of thie GNU General Public License as published by
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

from gi.repository import Clutter
from gi.repository import GtkClutter
from gi.repository import GdkPixbuf
from gi.repository import Gtk

from pyclut.menus.coverflow import Coverflow

class PixbufTexture(Clutter.Texture):
    """
    Represents a texture that loads its data from a pixbuf.
    """
    __gtype_name__ = 'PixbufTexture'
 
    def __init__(self, width, height, pixbuf):
        """
        @type width: int
        @param width: The width to be used for the texture.
        @type height: int
        @param height: The height to be used for the texture.
        @type pixbuf: gdk.pixbuf
        @param pixbuf: A pixbuf from an other widget.
        """
        super(PixbufTexture, self).__init__()
        self.set_width(width)
        self.set_height(height)
        # do we have an alpha value?
        if pixbuf.props.has_alpha:
            bpp = 4
        else:
            bpp = 3
 
        self.set_from_rgb_data(
            pixbuf.get_pixels(),
            pixbuf.props.has_alpha,
            pixbuf.props.width,
            pixbuf.props.height,
            pixbuf.props.rowstride,
            bpp, 0)

class CoverartCoverflow(Gtk.Box):
    __gtype_name__ = "CoverartCoverflow"

    def __init__(self, *args, **kwargs):
        super(CoverartCoverflow, self).__init__(*args, **kwargs)

        self.set_orientation(Gtk.Orientation.VERTICAL)
        # coverflow
        embd = GtkClutter.Embed()
        embd.set_size_request(400,400)
        self.stage = embd.get_stage()
        col = Clutter.Color()
        col.from_string("#000")
        self.stage.set_color(col)
        self.pack_start(embd, True, True, 0)

        self.bttn = Gtk.Button("left")
        self.pack_start(self.bttn, False, True, 0)
        self.bttn2 = Gtk.Button("right")
        self.pack_start(self.bttn2, False, True, 0)

        self.show_all()

    def update_covers(self, covers_view):

        coverflow = Coverflow(size=(1024, 400), item_size=(128,128), angle=70,
            inter_item_space=50, selection_depth=150)
        self.stage.add_actor(coverflow)

        #item_images = ['a.png',
        #    'b.png',
        #    'c.png',
        #    'd.png',
        #    'e.png',
        #    'f.png',
        #    'g.png',
        #    'h.png']
        model = covers_view.get_model()
        
        for row in model:        
            coverflow.add_actor(PixbufTexture(64,64,model[row][1]))
                
        coverflow.set_position(0, 150)
        self.current = 1
        #self.stage.connect('key-press-event', self.on_input, coverflow, item_images)
        self.bttn.connect('clicked', self.button_left, coverflow)
        self.bttn2.connect('clicked', self.button_right, coverflow)

    def button_left(self,button, coverflow):
        coverflow.previous()

    def button_right(self,button, coverflow):
        coverflow.next()
    
    def on_input(stage, event, coverflow, item_images):
        if get_keyval(event) == Clutter.KEY_Left:
            coverflow.previous()
        elif get_keyval(event) == Clutter.KEY_Right:
            coverflow.next()
        elif get_keyval(event) == Clutter.a or get_keyval(event) == Clutter.A:
            coverflow.add_actor(Clutter.Texture.new_from_file(item_images[self.current]))
            self.current = (self.current + 1) % len(item_images)
        elif get_keyval(event) == Clutter.s or get_keyval(event) == Clutter.S:
            coverflow.show()
        elif get_keyval(event) == Clutter.h or get_keyval(event) == Clutter.H:
            coverflow.hide()
        #elif get_keyval(event) == Clutter.q or get_keyval(event) == Clutter.Q:
        #    Clutter.main_quit()
