#! /usr/bin/python

#imports
from gi.repository import Gtk, Gdk, GLib, Pango, PangoCairo
from gi.repository.GdkPixbuf import Pixbuf
import cairo, math, struct, string, re

class dics(object):
	#temps
	circle = {}
	curve = {}
	img = {}
	line = {}
	square = {}
	text = {}
	#ui
	ui = {
		'win1': ['WMBox', 'pack_start', False, False, 0, 'FileOpen', 'fileopen.png', 'button-press-event', 'open_file_diag', None, 'Open File'],
		'win2': ['WMBox', 'pack_start', False, False, 0, 'FileNew', 'filenew.png', 'button-press-event', 'on_new_file_event', None, 'New File'],
		'win3': ['WMBox', 'pack_end', False, False, 0, 'Mini', 'mini.png', 'button-press-event', 'iconify_hack', None, 'Minimize'],
		'win4': ['WMBox', 'pack_end', False, False, 0, 'Max', 'max.png', 'button-press-event', 'fullscreen_hack', None, 'Maximize'],
		'win5': ['WMBox', 'pack_end', False, False, 0, 'Quit', 'quit.png', 'button-press-event', 'Gtk.main_quit', None, 'Quit'],
		'gen1': ['IconBox', 'pack_end', True, True, 60, 'self.T', 'tools.png', 'button-press-event', 'tool_ui', None, 'Draw Tools'],
		'gen2': ['IconBox', 'pack_end', True, True, 60, 'self.BGUI', 'bg.png', 'button-press-event', 'Slide_ui', None, 'Slide Tools'],
		'tool1': ['IconBox', 'pack_end', True, True, 0, 'self.Line', 'line.png', 'button-press-event', 'draw_init', 'line', 'Draw a Line'],
		'tool2': ['IconBox', 'pack_end', True, True, 0, 'self.Circle', 'circle.png', 'button-press-event', 'draw_init', 'circle', 'Draw a Circle'],
		'tool3': ['IconBox', 'pack_end', True, True, 0, 'self.Square', 'square.png', 'button-press-event', 'draw_init', 'square', 'Draw a Square'],
		'tool4': ['IconBox', 'pack_end', True, True, 0, 'self.Text', 'text.png', 'button-press-event', 'draw_init', 'text', 'Insert Text'],
		'tool5': ['IconBox', 'pack_end', True, True, 0, 'self.Img', 'img.png', 'button-press-event', 'draw_init', 'img', 'Insert an Image'],
		'tool6': ['IconBox', 'pack_end', True, True, 0, 'self.ToolRet', 'back.png', 'button-press-event', 'gen_ui', None, 'Back'],
		'bg1': ['IconBox', 'pack_end', True, True, 0, 'self.changebg', 'changebg.png', 'button-press-event', 'change_bg_diag', None, 'Load Backgroud Image'],
		'bg2': ['IconBox', 'pack_end', True, True, 0, 'self.BGRet', 'back.png', 'button-press-event', 'gen_ui', None, 'Back']
	}

	tool_cfg_ui = {
		'cfg1': ['CBox', 'pack_start', False, False, 0, 'self.LC', 'lcround.png', 'button-press-event', 'lc_change', None, 'Change the line cap'],
		'cfg2': ['CBox', 'pack_start', False, False, 0, 'self.Fill', 'square.png', 'button-press-event', 'fill_set', None, 'Fill']
	}

#input stuff for text editing in cairo
class text_input(object):
	special_chars = {
		'BackSpace': None,
		'Delete': None,
		'space': ' ',
		'Return': None,
		'Tab': None,
		'exclam': '!',
		'quotedbl': '\"',
		'numbersign': '#',
		'dollar': '$',
		'percent': '%',
		'ampersand': '&',
		'apostrophe': '\'',
		'parenleft': '(',
		'parenright': ')',
		'plus': '+',
		'asterisk': '*',
		'comma': ',',
		'minus': '-',
		'period': '.',
		'slash': '/',
		'colon': ':',
		'semicolon': ';',
		'less': '<',
		'equal': '=',
		'greater': '>',
		'question': '?',
		'Left': None,
		'Right': None,
		'Up': None,
		'Down': None,
		'at': '@',
		'bracketleft': '[',
		'backslash': '\\',
		'bracketright': ']',
		'asciicircum': '^',
		'underscore': '_',
		'grave': '`',
		'quoteleft': '"',
		'braceleft': '{',
		'braceright': '}',
		'yen': '¥',
		'asciitilde': '~',
		'bar': '|'
	}
	temp_text = Gtk.EntryBuffer()

class temp_lists(object):
	circle = []
	coords = []
	curve = []
	end_coords = []
	img = []
	line = []
	root_coords = []
	square = []
	temp = []
	text = []
	extra = []

class dset(object):
	ProjName = ('lala - test')
	BG = ('')
	Cl = [0, 0, 0, 1]
	font = 'Purisa'
	fill = False
	LCap = cairo.LINE_CAP_ROUND
	img = ('')

class LalaWin(Gtk.Window):

	def __init__(self):

		super(LalaWin, self).__init__()

		self.init_ui()

	def init_ui(self):
		self.Full = False

		Gtk.Window.__init__(self, title=dset.ProjName)
		self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.95, .95, .95, .95))

		self.set_position(Gtk.WindowPosition.CENTER)

		#remove window decorations and add main box
		self.set_decorated(False)
		MainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

		self.WMBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		MainBox.pack_start(self.WMBox, False, False, 0)

		for n, c in reversed(sorted(dics.ui.items())):
			if n.startswith('win'):
				self.make_btn(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10])

		#move/title bar
		MoveBar = Gtk.EventBox()
		MoveBar.connect('button-press-event', self.on_move_event)
		ProjTitle = Gtk.Label(label=dset.ProjName, halign=Gtk.Align.CENTER)
		MoveBar.add(ProjTitle)
		self.WMBox.pack_start(MoveBar, True, True, 0)

		self.Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

		self.IconBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.Box.pack_start(self.IconBox, False, False, 60)
		self.gen_ui(None, None)

		#border
		BorderBox = Gtk.Box()
		BorderUI = Gtk.Image()
		BorderUI.set_from_file('border.png')
		BorderBox.pack_start(BorderUI, True, True, 0)

		#slide interface (cairo surface)
		self.DrawBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.darea = Gtk.DrawingArea()
		self.darea.connect('draw', self.on_draw_slide)
		self.darea.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
		self.DrawBox.pack_start(self.darea, True, True, 0)

		self.CBox = Gtk.Box()

		self.Box.pack_end(self.DrawBox, True, True, 0)
		self.Box.pack_end(BorderBox, False, False, 0)

		MainBox.pack_start(self.Box, True, True, 0)

		self.add(MainBox)

		self.resize(1200, 800)

		self.connect('delete-event', Gtk.main_quit)
		self.show_all()

#move bar on click
	def on_move_event(self, widget, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and Gdk.EventType.MOTION_NOTIFY and event.button == 1:
			coords = Gdk.Event.get_root_coords(event)
			tstamp = Gdk.Event.get_time(event)
			self.begin_move_drag(event.button, coords[1], coords[2], tstamp)

#dirty fix for Iconify
	def iconify_hack(self, *args, **kwargs):
		self.iconify()

#dirty fix for fullscreen
	def fullscreen_hack(self, *args, **kwargs):
		if not self.Full:
			self.fullscreen()
			self.Full = True
		else:
			self.unfullscreen()
			self.Full = False

#for generic (startup) icons
	def gen_ui(self, widget, event):
		if event != None:
			self.clean_ui()
			if hasattr(self, 'drwchk'):
				if self.drwchk == True:
					self.dc(True)

		for n, c in reversed(sorted(dics.ui.items())):
			if n.startswith('gen'):
				self.make_btn(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10])

		self.show_all()

#tool ui (paint mode)
	def tool_ui(self, widget, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:

			if hasattr(self, 'drawsig'):
				if self.drwchk == True:
					self.dc()
					self.drwchk = False

			self.clean_ui()
			self.drwchk = False

			for n, c in reversed(sorted(dics.ui.items())):
				if n.startswith('tool'):
					self.make_btn(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10])

			self.show_all()

#BG ui (for manipulating/changing Slide BG)
	def Slide_ui(self, widget, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
			self.clean_ui()
			self.draw_customize_box('img')

			for n, c in reversed(sorted(dics.ui.items())):
				if n.startswith('bg'):
					self.make_btn(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10])

			self.show_all()

#cleans ui
	def clean_ui(self):
		for n, c in reversed(sorted(dics.ui.items())):
			btn_name = c[5]
			if btn_name.startswith('self.'):
				btn_name = btn_name[5:]
				if hasattr(self, btn_name + 'IBox'):
					a = getattr(self, btn_name + 'IBox')
					a.destroy()

		if hasattr(self, 'CBox'):
			self.CBox.destroy()

#create's button from image
	def make_btn(self, pck_box, pck_type, pck_1, pck_2, pck_3, btn_name, icn_name, event, con1, con2, tooltip):
		dic = {}

		pck_box = getattr(self, pck_box)
		if btn_name.startswith('self.'):
			btn_name = btn_name[5:]
			setattr(self, btn_name + 'IBox', Gtk.EventBox())
			setattr(self, btn_name + 'Icon', Gtk.Image())
			box = getattr(self, btn_name + 'IBox')
			icon = getattr(self, btn_name + 'Icon')
		else:
			box = dic[btn_name + 'IBox'] = Gtk.EventBox()
			icon = dic[btn_name + 'Icon'] = Gtk.Image()

		icon.set_from_file(icn_name)
		box.set_tooltip_text(tooltip)
		box.add(icon)

		if con1 == 'Gtk.main_quit':
			con1 = Gtk.main_quit
		else:
			con1 = getattr(self, con1)
		if con2 != None:
			box.connect(event, con1, con2)
		else:
			box.connect(event, con1)

		if pck_type == 'pack_end':
			p = pck_box.pack_end
		elif pck_type == 'pack_start':
			p = pck_box.pack_start

		p(box, pck_1, pck_2, pck_3)

#handles the customization box (below slide) (needs to be cleaner)
	def draw_customize_box(self, draw_type):
		self.CBox = Gtk.Box()

		if not hasattr(self, 'LwAdj'):
			self.LwAdj = 20
		if not hasattr(self, 'img_alpha'):
			self.img_alpha = 100

		self.ClSelBtn = Gtk.EventBox()
		self.ClSelBtn.set_tooltip_text('change the color')
		self.ClSelLabel = Gtk.Label('           ')
		self.ClSelBtn.add(self.ClSelLabel)
		self.ClSelBtn.connect('button-press-event', self.on_color_chooser, draw_type)

		self.SetLw = Gtk.Entry()
		self.SetLw.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(.95, .95, .95))
		self.SetLw.set_has_frame(False)
		self.SetLw.set_width_chars(3)

		if draw_type == 'text':
			self.LwAdj = 20
		self.SetLw.set_text(str(self.LwAdj))

		#GTK HAXX FTW!
		def focus_loss(spinner):
			spinner.set_state(Gtk.StateType.INSENSITIVE)
			spinner.set_state(Gtk.StateType.NORMAL)

		self.SetLw.connect('changed', self.spin_chk, self.SetLw)
		self.SetLw.connect('activate', focus_loss)

		self.CBox.pack_start(self.ClSelBtn, False, False, 20)

		for n, c in reversed(sorted(dics.tool_cfg_ui.items())):
			self.make_btn(c[0], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10])

		self.CBox.pack_start(self.SetLw, False, False, 20)

		if draw_type == 'line':
			self.FillIBox.destroy()

		if draw_type == 'img':
			self.ClSelBtn.destroy()
			self.SetLw.destroy()
			self.LCIBox.destroy()
			self.FillIBox.destroy()

			self.img_slider_container = Gtk.Box()
			self.img_slider = Gtk.Entry()
			self.img_slider.set_has_frame(False)
			self.img_slider.set_width_chars(3)
			self.img_slider.set_text(str(self.img_alpha))
			self.img_slider.connect('changed', self.spin_chk, self.img_slider)

			self.img_slider_container.pack_start(self.img_slider, False, False, 0)
			self.CBox.pack_start(self.img_slider_container, False, False, 20)

		elif hasattr(self, 'img_slider'):
			self.img_slider.destroy()

		if draw_type == 'text':
			self.FillIBox.destroy()
			self.LCIBox.destroy()
			if hasattr(self, 'ClSel'):
				color = self.ClSel.get_current_color()
			else:
				color = Gdk.Color(dset.Cl[0], dset.Cl[1], dset.Cl[2])
			color = color.to_string()
			self.ClSelLabel.set_markup("<span font_desc=\"Sans Bold 20.0\" color=\"" + color + "\">  A  </span>")

			font_map = PangoCairo.font_map_get_default()
			fonts = [f.get_name() for f in font_map.list_families()]

			self.font_set = Gtk.ComboBoxText()
			self.font_set.set_entry_text_column(0)
			self.font_set.connect('changed', self.font_change)
			for font in fonts:
				self.font_set.append_text(font)
			self.font_set.set_active(0)
			self.font_set.set_focus_on_click(False)
			self.CBox.pack_start(self.font_set, False, False, 20)

		else:
			self.ClSelBtn.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(dset.Cl[0], dset.Cl[1], dset.Cl[2], dset.Cl[3]))
			self.ClSelBtn.override_background_color(Gtk.StateFlags.ACTIVE, Gdk.RGBA(dset.Cl[0], dset.Cl[1], dset.Cl[2], dset.Cl[3]))
			self.ClSelBtn.override_background_color(Gtk.StateFlags.SELECTED, Gdk.RGBA(dset.Cl[0], dset.Cl[1], dset.Cl[2], dset.Cl[3]))

		self.DrawBox.pack_end(self.CBox, False, False, 20)

		self.show_all()

	def spin_chk(self, event, slider):
		test_buffer = slider.get_buffer()
		text = test_buffer.get_text()
		chk = re.match('\d', test_buffer.get_text()[::-1])

		if not chk:
			if len(text) != 0:
				test_buffer.delete_text(len(text)-1, 2)
			else:
				test_buffer.delete_text(len(text), 1)

		if len(text) > 2 and text != '100':
			test_buffer.delete_text(len(text)-1, 1)

		self.update_img_alpha(slider)

	def lc_change(self, widget, event):
		if dset.LCap == cairo.LINE_CAP_ROUND:
			dset.LCap = cairo.LINE_CAP_BUTT
			self.LCIcon.set_from_file('lcbutt.png')
		else:
			dset.LCap = cairo.LINE_CAP_ROUND
			self.LCIcon.set_from_file('lcround.png')

	def update_img_alpha(self, slider):
		if slider.get_text() != '':
			adj = int(slider.get_text())
		else:
			adj = 0
		if slider == self.SetLw:
			self.LwAdj = adj
		elif slider == self.img_slider:
			self.img_alpha = adj
		self.queue_draw()

	def fill_set(self, widget, event):
		if dset.fill == True:
			dset.fill = False
			self.FillIcon.set_from_file('square.png')
		else:
			dset.fill = True
			self.FillIcon.set_from_file('fill.png')

	def font_change(self, combo):
		dset.font = combo.get_active_text()

#draw
	def draw_init(self, widget, event, draw_type):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
			self.textchk, self.arcchk, self.curvechk, self.mouse_down = [False, False, False, False]

			if self.drwchk == True:
				self.dc(False)

			self.draw_customize_box(draw_type)


			if draw_type == 'img':
				self.filter_type = 1
				load_err = 1
				load_type = 2
				self.diag_menu(load_err, load_type)

			drawcon = {
			1: ['drawsig', 'draw', self.draw, draw_type],
			2: ['drawbutsig', 'button-press-event', self.on_draw, draw_type],
			3: ['drawmotsig', 'motion-notify-event', self.on_draw, draw_type],
			4: ['drawrelsig', 'button-release-event', self.on_draw, draw_type]
			}

			self.drawkeysig = self.connect('key-press-event', self.on_draw, draw_type)

			for a, b in drawcon.items():
				setattr(self, b[0], self.darea.connect(b[1], b[2], b[3]))

			self.drwchk = True
			self.show_all()

	#removes connections to old input when switching draw modes
	def dc(self, chk):
		x = [self.drawbutsig, self.drawmotsig, self.drawrelsig, self.drawsig]
		for a in x:
			self.darea.disconnect(a)
		if hasattr(self, 'drawkeysig'):
			self.disconnect(self.drawkeysig)
		if chk == True:
			self.drawsig = self.darea.connect('draw', self.draw, None)
		self.CBox.destroy()
		self.drwchk, dset.LCap, dset.fill= [False, cairo.LINE_CAP_ROUND, False]

	#handles all incoming signals for draw modes
	def on_draw(self, widget, event, draw_type):
		if draw_type == 'line' and event.state & Gdk.ModifierType.SHIFT_MASK:
			draw_type = 'curve'
			self.curvechk = True

		d = getattr(dics, draw_type)

		#grab mode
		if event.state & Gdk.ModifierType.CONTROL_MASK:
			if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
				self.grabchk = True

				for a, b in sorted(d.items()):
					l = b[0]
					origin, endpoint = l[0], l[1]
					origin = [origin[0] + self.aw, origin[1] + self.ah]
					endpoint = [endpoint[0] + self.aw, endpoint[1] + self.ah]
					x, y = event.x - origin[0], event.y - origin[1]
					x2, y2 = endpoint[0] - event.x, endpoint[1] - event.y

					if origin[0] < endpoint[0]:
						chkx = endpoint[0] >= event.x >= origin[0]
					else:
						chkx = origin[0] >= event.x >= endpoint[0]
					if origin[1] < endpoint[1]:
						chky = endpoint[1] >= event.y >= origin[1]
					else:
						chky = origin[1] >= event.y >= endpoint[1]

					if chkx and chky:
						temp_lists.extra = [self.LwAdj, dset.Cl, dset.fill, dset.img]
						temp_lists.grab = [origin, endpoint, x, y, x2, y2, a, b[1], b[2], b[3], b[4]]
						self.mouse_down = True


			elif self.mouse_down and event.type == Gdk.EventType.MOTION_NOTIFY and event.type != Gdk.EventType.BUTTON_RELEASE:
				i, j, x, y, x2, y2, name, Lw, Cl, fill, img = temp_lists.grab
				self.LwAdj, dset.Cl, dset.fill, dset.img = Lw, Cl, fill, img

				temp_lists.coords = [event.x - x, event.y - y]
				temp_lists.root_coords = [(event.x - x), (event.y - y)]
				temp_lists.temp = [temp_lists.coords[:]]


				temp_lists.end_coords = [event.x + x2, event.y + y2]
				temp_lists.temp.append(temp_lists.end_coords[:])
				setattr(temp_lists, draw_type, temp_lists.temp)

			elif self.mouse_down and event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1:
				self.mouse_down = False
				d.pop(temp_lists.grab[6])
				l = [temp_lists.root_coords[:], temp_lists.end_coords[:]]
				self.dic_entry(draw_type, d, temp_lists.grab[6], l, temp_lists.grab[7], temp_lists.grab[8], temp_lists.grab[9], temp_lists.grab[10])
				self.LwAdj, dset.Cl, dset.fill, dset.img = temp_lists.extra

		#normal mode
		else:

			if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
				self.mouse_down = True
				temp_lists.coords = [event.x, event.y]
				temp_lists.root_coords = [event.x - self.aw, event.y - self.ah]
				temp_lists.temp = [temp_lists.coords[:]]
				setattr(temp_lists, draw_type, temp_lists.temp)

			elif self.mouse_down and event.type == Gdk.EventType.MOTION_NOTIFY and event.type != Gdk.EventType.BUTTON_RELEASE:
				temp_lists.end_coords = [event.x, event.y]
				temp_lists.temp.append(temp_lists.end_coords[:])
				setattr(temp_lists, draw_type, temp_lists.temp)


			elif event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1:
				self.mouse_down = False
				temp_lists.end_coords = [event.x - self.aw, event.y - self.ah]
				l = [temp_lists.root_coords[:], temp_lists.end_coords[:]]
				if draw_type == 'text':
					cl = dset.Cl
					fill = dset.font
					extra = ''
				elif draw_type == 'img':
					cl = self.img_alpha
					fill = None
					extra = dset.img
				else:
					cl = dset.Cl
					fill = dset.fill
					extra = dset.LCap
				self.dic_entry(draw_type, d, draw_type + str(len(d)+1), l, cl, self.LwAdj, fill, extra)
				self.curvechk = False


			elif event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3 and len(d) >= 1:
				d.pop(draw_type + str(len(d)))
				self.textchk = False

				setattr(temp_lists, draw_type, [])
				temp_lists.temp = []

			if event.type == Gdk.EventType.KEY_PRESS and self.textchk == True and draw_type == 'text':
				a = Gdk.keyval_name(event.keyval)
				b = text_input.temp_text.get_text()

				if len(a) == 1:
					text_input.temp_text.set_text(b + a, len(b) + 1)

				for name, char in text_input.special_chars.items():
					if a == 'BackSpace' or a == 'Delete':
						if len(b) > 0:
							text_input.temp_text.delete_text(len(b) - 1, 2)
						else:
							text_input.temp_text.delete_text(len(b), 1)

					elif a == 'Return':
						for a, b in dics.text.items():
							if a == 'text' + str(len(dics.text)) and a != 'text0':
								l = b[0]

						if text_input.temp_text.get_text() != '':
							self.dic_entry(draw_type, d, draw_type + str(len(d)+1), l, dset.Cl, self.LwAdj, dset.font, text_input.temp_text.get_text())
						else:
							dics.text.pop('text' + str(len(dics.text)))

						self.textchk = False
						text_input.temp_text.delete_text(0, -1)

					elif a == name:
						text_input.temp_text.delete_text(len(b), 1)
						text_input.temp_text.set_text(b + char, len(b) + 1)

		self.queue_draw()

	def dic_entry(self, draw_type, d, n, l, Cl, Lw, fill, extra):
		d[n] = l[:], Cl, Lw, fill, extra

		if draw_type == 'text':
			self.textchk = True

		else:
			self.textchk = False

	#does the actual drawing
	def draw(self, widget, cr, draw_type):
		if self.curvechk == True:
			draw_type = 'curve'

		cr.save()
		cr.translate(self.aw, self.ah)

		for dic in dir(dics):
			if not '_' in dic:
				x = getattr(dics, dic)
				if len(x.items()) != 0:
					cr.save()
					for a, b in sorted(x.items()):
						l = b[0]
						cl = b[1]
						lw = b[2]
						fill = b[3]
						extra = b[4]

						drw = {
						'line': self.draw_line,
						'curve': self.draw_curve,
						'circle': self.draw_circle,
						'square': self.draw_square,
						'text': self.draw_text,
						'img': self.draw_img
						}

						for a, b in drw.items():
							if a == dic:
								if a == 'circle':
									b(l, cr, cl, lw, fill, cairo.LINE_CAP_BUTT)
								else:
									b(l, cr, cl, lw, fill, extra)

					cr.restore()
		cr.restore()

		if len(temp_lists.temp) >= 2:
			cr.save()

			drawi = {
			'line': [self.draw_line, temp_lists.line, dset.LCap],
			'curve': [self.draw_curve, temp_lists.curve, dset.LCap],
			'circle': [self.draw_circle, temp_lists.circle, cairo.LINE_CAP_BUTT],
			'square': [self.draw_square, temp_lists.square, dset.LCap],
			'img': [self.draw_img, temp_lists.img, dset.img]
			}

			for a, b in drawi.items():
				if a == draw_type:
					draw = b[0]
					l = b[1]
					cap = b[2]
					if draw_type == 'img':
						draw(l, cr, self.img_alpha, None, None, cap)
					else:
						draw(l, cr, dset.Cl, self.LwAdj, dset.fill, cap)
					self.draw_BB(l, cr)
					if len(temp_lists.text) != 0:
						temp_lists.text = []
					if len(l) != 0:
						while len(l) > 1:
							l.pop()
			cr.restore()

		#clips the saved painted objects to the slide surface
		cr.rectangle(110, 110, 751, 563)
		cr.clip()

		if self.textchk == True:
			self.on_draw_text(cr)

		del temp_lists.coords[:]

	def draw_BB(self, l, cr):
		cr.set_source_rgba(0, 0, 0, .6)
		cr.set_line_cap(cairo.LINE_CAP_ROUND)
		cr.set_line_width(1)
		cr.set_dash([14.0, 6.0])
		for i in l:
			for j in l:
				w2 = j[0] - i[0]
				h2 = j[1] - i[1]
				cr.rectangle(i[0], i[1], w2, h2)
				cr.stroke()

	def draw_circle(self, l, cr, cl, lw, fill, cap):
		cr.set_source_rgba(cl[0], cl[1], cl[2], cl[3])
		cr.set_line_cap(cairo.LINE_CAP_BUTT)
		cr.set_line_width(lw)
		for i in l:
			for j in l:
				xdif = j[0] - i[0]
				ydif = j[1] - i[1]
				xc = xdif/2 + i[0]
				yc = ydif/2 + i[1]
				r = (xdif+ydif)/4
				cr.save()

				if xdif != ydif and xdif != 0 and ydif != 0 and r != 0:
					xr = float(((xdif*2)/4)/r)
					yr = float(((ydif*2)/4)/r)

					cr.translate(i[0]+(r*xr), i[1]+(r*yr))
					cr.scale(xr, yr)
					cr.translate(-i[0]-(r*xr), -i[1]-(r*yr))

				cr.arc(xc, yc, r, 0, 2*math.pi)
				cr.restore()
				if fill == True:
					cr.fill()
				cr.stroke()

	def draw_curve(self, l, cr, cl, lw, fill, cap):
		cr.set_source_rgba(cl[0], cl[1], cl[2], cl[3])
		cr.set_line_cap(cap)
		cr.set_dash([10, 0])
		cr.set_line_width(lw)
		for i in l:
			for j in l:
				cr.move_to(i[0], i[1])
				q = (j[0]-i[0])/4
				if i[1] > j[1] and i[0] > j[0]:
					pnt2 = (q*3)+i[0], i[1]
					pnt3 = j[0], q+i[1]
				elif i[1] > j[1] and i[0] < j[0]:
					pnt2 = (q*3)+i[0], i[1]
					pnt3 = j[0], q+j[1]
				elif i[1] < j[1] and i[0] < j[0]:
					pnt2 = (q*3)+i[0], i[1]
					pnt3 = j[0], q+i[1]
				else:
					pnt2 = (q*3)+i[0], i[1]
					pnt3 = j[0], q+j[1]	
			cr.curve_to(pnt2[0], pnt2[1], pnt3[0], pnt3[1], j[0], j[1])
			cr.stroke()

	def draw_img(self, l, cr, alpha, empty, none, img):
		if type(img) != str:
			cr.save()
			imh = img.get_height()
			imw = img.get_width()
			if len(l) == 2:
				i, j = l
				x1, y1 = i
				x2, y2 = j

				if x2-x1 != 0 and y2-y1 != 0:
					wr = float(x2-x1)/float(imw)
					hr = float(y2-y1)/float(imh)
					cr.translate(x1+wr, y1+hr)
					if wr != 0 and hr != 0:
						cr.scale(wr, hr)
						Gdk.cairo_set_source_pixbuf(cr, img, 0, 0)
						cr.paint_with_alpha(int(alpha)*.01)
			cr.restore()

	def draw_insert(self, l, cr, cl):
		cr.set_source_rgba(cl[0], cl[1], cl[2], cl[3])
		cr.set_line_cap(cairo.LINE_CAP_BUTT)
		cr.set_line_width(1)
		i = l[0]
		cr.move_to(i[0], i[1] + .75*self.LwAdj)
		cr.line_to(i[0], i[1] + self.LwAdj + .06*self.LwAdj)
		cr.move_to(i[0], i[1] + self.LwAdj + .06*self.LwAdj)
		cr.line_to(i[0] + .25*self.LwAdj, i[1] + self.LwAdj + .06*self.LwAdj)
		cr.stroke()

	def draw_line(self, l, cr, cl, lw, fill, cap):
		cr.set_source_rgba(cl[0], cl[1], cl[2], cl[3])
		cr.set_line_cap(cap)
		cr.set_dash([10, 0])
		cr.set_line_width(lw)
		for i in l:
			for j in l:
				cr.move_to(i[0], i[1])
				cr.line_to(j[0], j[1])
				cr.stroke()

	def draw_square(self, l, cr, cl, lw, fill, lj):
		cr.set_source_rgba(cl[0], cl[1], cl[2], cl[3])
		cr.set_line_cap(cairo.LINE_CAP_BUTT)
		cr.set_dash([10, 0])
		cr.set_line_width(lw)
		for i in l:
			for j in l:
				w2 = j[0] - i[0]
				h2 = j[1] - i[1]
				cr.rectangle(i[0], i[1], w2, h2)
				if fill == True:
					cr.fill()
				cr.set_line_join(lj)
				cr.stroke()

	def draw_text(self, l, cr, cl, lw, font, text):
		cr.set_source_rgba(cl[0], cl[1], cl[2], cl[3])
		cr.set_line_cap(cairo.LINE_CAP_BUTT)
		cr.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
		cr.set_font_size(lw)
		x = l[0]
		cr.move_to(x[0], x[1]+lw)
		cr.show_text(text)

	def on_draw_text(self, cr):
		for a, b in dics.text.items():
			if a == 'text' + str(len(dics.text)) and a != 'text0':
				l = b[0]

		self.draw_insert(l, cr, dset.Cl)
		self.draw_text(l, cr, dset.Cl, self.LwAdj, dset.font, text_input.temp_text.get_text())

#handles slide bg
	def SlideBG_change(self, event):
		if dset.BG != '':
			self.bg = Pixbuf.new_from_file(dset.BG)
		self.queue_draw()

	def on_draw_slide(self, widget, cr):
		cr.save()
		w, h = self.get_size()
		self.aw = w/2 - 600
		self.ah = h/2 - 400
		cr.translate(w/2, h/2)
		x = [0, 1, 2, 3]
		for r in x:
			cr.set_source_rgba(0, 0, 0, .04 + (r/20))
			cr.rectangle(-494 + r, -294 + r, 759 - 2*r, 571 - 2*r)
			cr.fill()

		cr.set_source_rgb(1, 1, 1)
		cr.rectangle(-490, -290, 751, 563)
		cr.fill()


		if len(dset.BG) >= 1:
			cr.save()
			cr.translate(-490, -290)

			imh = self.bg.get_height()
			imw = self.bg.get_width()
			wr = float(751)/float(imw)
			hr = float(563)/float(imh)
			cr.scale(wr, hr)

			Gdk.cairo_set_source_pixbuf(cr, self.bg, 0, 0)
			cr.paint_with_alpha(self.img_alpha*.01)
			cr.restore()

		cr.restore()

#warning dialogues
	def on_new_file_event(self, widget, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
			#popup
			dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, 'Are you sure you want to start over?')
			dialog.format_secondary_text('You will lose all progress since last saved!')
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				#REPLACE WITH ACTUAL RESTART!! (IE reset all changes back to original values)
				print ('new file clickeded')
			elif response == Gtk.ResponseType.CANCEL:
				print ('cancel clickeded')
			dialog.destroy()

	#load error popup
	def on_load_err(self, load_err):
		if load_err == 0:
			load_type = ('a lala')
		elif load_err == 1:
			load_type = ('a compatible image')

		dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, 'Not ' + load_type + ' file!')
		dialog.format_secondary_text('It looks like you selected a file Lala can\'t read! Please select ' + load_type +' file or cancel.')
		dialog.run()
		dialog.destroy()

#color chooser dialogue
	def on_color_chooser(self, widget, event, draw_type):
		dialog = color_chooser(self)
		response = dialog.run()

		if response == Gtk.ResponseType.OK:

			dset.Cl = self.ClSel.get_current_rgba()
			dset.Cl = list(dset.Cl)

			if draw_type == 'text':
				color = self.ClSel.get_current_color()
				color = color.to_string()
				self.ClSelLabel.set_markup("<span font_desc=\"Sans Bold 20.0\" color=\"" + color + "\">  A  </span>")

			else:
				self.ClSelBtn.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(dset.Cl[0], dset.Cl[1], dset.Cl[2], dset.Cl[3]))
				self.ClSelBtn.override_background_color(Gtk.StateFlags.ACTIVE, Gdk.RGBA(dset.Cl[0], dset.Cl[1], dset.Cl[2], dset.Cl[3]))
				self.ClSelBtn.override_background_color(Gtk.StateFlags.SELECTED, Gdk.RGBA(dset.Cl[0], dset.Cl[1], dset.Cl[2], dset.Cl[3]))

		elif response == Gtk.ResponseType.CANCEL:
			print('color change aborted')

		dialog.destroy()
		self.show_all()

#file chooser dialogue
	def diag_menu(self, load_err, load_type):
		dialog = Gtk.FileChooserDialog('Select File to Open', self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		self.add_filters(dialog)
			#!!NEEDS ACTUAL IMPORT!!
		chk = False
		chk2 = False
		if load_type == 0:
			while chk == False:
				response = dialog.run()
				filename = dialog.get_filename()

				if response == Gtk.ResponseType.OK and not '.lala' in filename:
					print ('failed to load:' + filename)
					self.on_load_err(load_err)

				elif response == Gtk.ResponseType.OK:
					print ('loading file: ' + filename)
					chk = True
				elif response == Gtk.ResponseType.CANCEL:
					chk = True

		elif load_type == 1:
			while chk == False:
				response = dialog.run()
				filename = dialog.get_filename()
				supported_image_types = ['.jpg', '.png']
				for l in supported_image_types:
					if response == Gtk.ResponseType.OK and not l in filename:
						chk2 = False
					else:
						chk2 = True
				if response == Gtk.ResponseType.OK and chk2 == True:
					print ('failed to load:' + filename)
					self.on_load_err(load_err)
				elif response == Gtk.ResponseType.OK:
					dset.BG = filename
					self.SlideBG_change(None)
					chk = True
				elif response == Gtk.ResponseType.CANCEL:
					chk = True


		elif load_type == 2:
			while chk == False:
				response = dialog.run()
				filename = dialog.get_filename()
				supported_image_types = ['.jpg', '.png']
				for l in supported_image_types:
					if response == Gtk.ResponseType.OK and not l in filename:
						chk2 = False
					else:
						chk2 = True
				if response == Gtk.ResponseType.OK and chk2 == True:
					print ('failed to load:' + filename)
					self.on_load_err(load_err)
				elif response == Gtk.ResponseType.OK:
					dset.img = Pixbuf.new_from_file(filename)
					self.SlideBG_change(None)
					chk = True
				elif response == Gtk.ResponseType.CANCEL:
					chk = True

		dialog.destroy()

	#open file
	def open_file_diag(self, widget, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
			self.filter_type = 0
			load_err = 0
			load_type = 0
			self.diag_menu(load_err, load_type)

	#change bg
	def change_bg_diag(self, widget, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
			self.filter_type = 1
			load_err = 1
			load_type = 1
			self.diag_menu(load_err, load_type)

	#filters
	def add_filters(self, dialog):
		if self.filter_type == 0:
			self.lala_filter(dialog)
			self.all_filter(dialog)

		elif self.filter_type == 1:
			self.img_filter(dialog)
			self.all_filter(dialog)

	def lala_filter(self, dialog):
		filter_lala = Gtk.FileFilter()
		filter_lala.set_name('Only lala files')
		filter_lala.add_pattern('*' + '.lala')
		dialog.add_filter(filter_lala)

	def img_filter(self, dialog):
		filter_lala = Gtk.FileFilter()
		filter_lala.set_name('Only image files (.png, .jpg, .gif)')
		filter_lala.add_pattern('*' + '.png')
		filter_lala.add_pattern('*' + '.jpg')
		filter_lala.add_pattern('*' + '.gif')
		dialog.add_filter(filter_lala)

	def all_filter(self, dialog):
		filter_all = Gtk.FileFilter()
		filter_all.set_name('Everything')
		filter_all.add_pattern('*')
		dialog.add_filter(filter_all)

#color chooser window
class color_chooser(Gtk.Dialog):

	def __init__(self, parent):
		Gtk.Dialog.__init__(self, 'Select Color', parent, 0, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
		self.set_decorated(False)
		self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.95, .95, .95, .95))

		LalaWin.ClSel = Gtk.ColorSelection()
		LalaWin.ClSel.set_has_opacity_control(True)
		LalaWin.ClSel.set_current_rgba(Gdk.RGBA(dset.Cl[0], dset.Cl[1], dset.Cl[2], dset.Cl[3]))

		Box = self.get_content_area()
		Box.add(LalaWin.ClSel)
		self.show_all()

def main():

	app = LalaWin()
	Gtk.main()

if __name__ == '__main__':
	main()