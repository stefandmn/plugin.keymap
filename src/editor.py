# -*- coding: utf-8 -*-
import sys
import json
import Commons as commons
from threading import Timer
from thread import get_ident as _get_ident
from _abcoll import KeysView, ValuesView, ItemsView

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


_actions = [
	["Navigation", [
		"left"							, "Move Left",
		"right"							, "Move Right",
		"up"							, "Move Up",
		"down"							, "Move Down",
		"pageup"						, "Page Up",
		"pagedown"						, "Page Down",
		"select"						, "Select Item",
		"highlight"						, "Highlight Item",
		"parentfolder"					, "Parent Directory",
		"back"							, "Back",
		"previousmenu"					, "Previous Menu",
		"info"							, "Show Info",
		"contextmenu"					, "Context Menu",
		"firstpage"						, "First Page",
		"lastpage"						, "Last Page",
		"nextletter"					, "Next Letter",
		"prevletter"					, "Previous Letter",
	]],

	["Playback", [
		"play"							, "Play",
		"pause"							, "Pause",
		"playpause"						, "Play/Pause",
		"stop"							, "Stop",
		"skipnext"						, "Next",
		"skipprevious"					, "Previous",
		"fastforward"					, "Fast Forward",
		"rewind"						, "Rewind",
		"smallstepback"					, "Small Step Back",
		"stepforward"					, "Step Forward",
		"stepback"						, "Step Back",
		"bigstepforward"				, "Big Step Forward",
		"bigstepback"					, "Big Step Back",
		"chapterorbigstepforward"		, "Next Chapter or Big Step Forward",
		"chapterorbigstepBack"			, "Previous Chapter or Big Step Back",
		"osd"							, "Show OSD",
		"showtime"						, "Show current play time",
		"playlist"						, "Show Playlist",
		"fullscreen"					, "Toggle Fullscreen",
		"aspectratio"					, "Change Aspect Ratio",
		"showvideomenu"					, "Go to DVD Video Menu",
		"playercontrol(repeat)"			, "Toggle Repeat",
		"playercontrol(repeatone)"		, "Repeat One",
		"playercontrol(repeatall)"		, "Repeat All",
		"playercontrol(repeatoff)"		, "Repeat Off",
		"playercontrol(random)"			, "Toggle Random",
		"playercontrol(randomon)"		, "Random On",
		"playercontrol(randomoff)"		, "Random Off",
		"createbookmark"				, "Create Bookmark",
		"createepisodebookmark"			, "Create Episode Bookmark",
		"togglestereomode"				, "Toggle 3D/Stereoscopic mode",
		"switchplayer"					, "Switch Player",
	]],

	["Audio", [
		"mute"							, "Mute",
		"volumeup"						, "Volume Up",
		"volumedown"					, "Volume Down",
		"audionextlanguage"				, "Next Language",
		"audiodelay"					, "Delay",
		"audiodelayminus"				, "Delay Minus",
		"audiodelayplus"				, "Delay Plus",
		"audiotoggledigital"			, "Toggle Digital/Analog",
	]],

	["Pictures", [
		"nextpicture"					, "Next Picture",
		"previouspicture"				, "Previous Picture",
		"rotate"						, "Rotate Picture",
		"rotateccw"						, "Rotate Picture CCW",
		"zoomout"						, "Zoom Out",
		"zoomin"						, "Zoom In ",
		"zoomnormal"					, "Zoom level Normal",
		"zoomlevel1"					, "Zoom level 1",
		"zoomlevel2"					, "Zoom level 2",
		"zoomlevel3"					, "Zoom level 3",
		"zoomlevel4"					, "Zoom level 4",
		"zoomlevel5"					, "Zoom level 5",
		"zoomlevel6"					, "Zoom level 6",
		"zoomlevel7"					, "Zoom level 7",
		"zoomlevel8"					, "Zoom level 8",
		"zoomlevel9"					, "Zoom level 9",
	]],

	["Subtitle", [
		"showsubtitles"					, "Show Subtitles",
		"nextsubtitle"					, "Next Subtitle",
		"subtitledelay"					, "Delay",
		"subtitledelayminus"			, "Delay Minus",
		"subtitledelayplus"				, "Delay Plus",
		"subtitlealign"					, "Align",
	]],

	["Item Actions", [
		"queue"							, "Queue item",
		"delete"						, "Delete item",
		"copy"							, "Copy item",
		"move"							, "Move item",
		"moveitemup"					, "Move item up",
		"moveitemdown"					, "Move item down",
		"rename"						, "Rename item",
		"scanitem"						, "Scan item",
		"togglewatched"					, "Toggle watched status",
	]],

	["System", [
		"togglefullscreen"				, "Toggle Fullscreen",
		"minimize"						, "Minimize",
		"shutdown"						, "Shutdown",
		"reboot"						, "Reboot",
		"hibernate"						, "Hibernate",
		"suspend"						, "Suspend",
		"restartapp"					, "Restart XBMC",
		"system.logoff"					, "Log off",
		"quit"							, "Quit XBMC",
	]],

	["Virtual Keyboard", [
		"enter"							, "Enter",
		"shift"							, "Shift",
		"symbols"						, "Symbols",
		"backspace"						, "Backspace ",
		"number0"						, "0",
		"number1"						, "1",
		"number2"						, "2",
		"number3"						, "3",
		"number4"						, "4",
		"number5"						, "5",
		"number6"						, "6",
		"number7"						, "7",
		"number8"						, "8",
		"number9"						, "9",
		"red"							, "Teletext Red",
		"green"							, "Teletext Green",
		"yellow"						, "Teletext Yellow",
		"blue"							, "Teletext Blue",
	]],

	["Other", [
		"updatelibrary(video)"			, "Update Video Library",
		"updatelibrary(music)"			, "Update Music Library",
		"cleanlibrary(video)"			, "Clean Video Library",
		"cleanlibrary(music)"			, "Clean Music Library",
		"codecinfo"						, "Show codec info",
		"screenshot"					, "Take screenshot",
		"reloadkeymaps"					, "Reload keymaps",
		"increasepar"					, "Increase PAR",
		"decreasepar"					, "Decrease PAR",
		"nextresolution"				, "Change resolution",
		"nextcalibration"				, "Next calibration",
		"resetcalibration"				, "Reset calibration",
		"showpreset"					, "Show current visualisation preset",
		"presetlist"					, "Show visualisation preset list",
		"nextpreset"					, "Next visualisation preset",
		"previouspreset"				, "Previous visualisation preset",
		"lockpreset"					, "Lock current visualisation preset ",
		"randompreset"					, "Switch to a new random preset",
	]],
]

_activate_window = [
	"settings"							, "Settings",
	"picturessettings"					, "Pictures Settings",
	"programssettings"					, "Programs Settings",
	"weathersettings"					, "Weather Settings",
	"musicsettings"						, "Music Settings",
	"systemsettings"					, "System Settings",
	"videossettings"					, "Videos Settings",
	"servicesettings"					, "Service Settings",
	"appearancesettings"				, "Appearance Settings",
	"skinsettings"						, "Skin Settings",
	"addonbrowser"						, "Addon Browser",
	"addonsettings"						, "Addon Settings",
	"profilesettings"					, "Profile Settings",
	"locksettings"						, "Lock Settings",
	"contentsettings"					, "Content Settings",
	"profiles"							, "Profiles",
	"systeminfo"						, "System info",
	"testpattern"						, "Test Pattern",
	"screencalibration"					, "Screen Calibration",
	"loginscreen"						, "Login Screen",
	"filebrowser"						, "Filebrowser",
	"networksetup"						, "Networksetup",
	"accesspoints"						, "Access Points",
	"mediasource"						, "Mediasource Dialog",
	"startwindow"						, "Start",
	"favourites"						, "Favourites",
	"contextmenu"						, "Context Menu",
	"peripherals"						, "Peripheral manager",
	"peripheralsettings"				, "Peripherals settings",
	"mediafilter"						, "Media filter",
	"visualisationpresetlist"			, "Vis. Preset List",
	"filestackingdialog"				, "Filestacking Dialog",
	"smartplaylisteditor"				, "Smart Playlist Editor",
	"smartplaylistrule"					, "Smart Playlist Rule",
	"shutdownmenu"						, "Shutdown Menu",
	"fullscreeninfo"					, "Fullscreen Info",
	"subtitlesearch"					, "Subtitle Search",
	"weather"							, "Weather",
	"screensaver"						, "Screensaver",
	"pictureinfo"						, "Picture Info",
	"addoninformation"					, "Addon Info",
	"musicplaylist"						, "Music Playlist",
	"musicfiles"						, "Music Files",
	"musiclibrary"						, "Music Library",
	"musicplaylisteditor"				, "Music Playlist Editor",
	"musicinformation"					, "Music Info",
	"musicoverlay"						, "Music Overlay",
	"songinformation"					, "Song Info",
	"karaoke"							, "Karaoke Lyrics",
	"karaokeselector"					, "Karaoke Song Selector",
	"karaokelargeselector"				, "Karaoke Selector",
	"movieinformation"					, "Video Info",
	"videofiles"						, "Video Files",
	"videooverlay"						, "Video Overlay",
	"videomenu"							, "Video Menu",
	"videoosd"							, "Video OSD",
	"videotimeseek"						, "Video Time Seek",
	"videobookmarks"					, "Video Bookmarks",
	"videoplaylist"						, "Video Playlist",
	"tvchannels"						, "TV Channels",
	"tvrecordings"						, "TV Recordings",
	"tvguide"							, "TV Guide",
	"tvtimers"							, "TV Timers",
	"tvsearch"							, "TV Search",
	"radiochannels"						, "Radio Channels",
	"radiorecordings"					, "Radio Recordings",
	"radioguide"						, "Radio Guide",
	"radiotimers "						, "Radio Timers",
	"radiosearch"						, "Radio Search",
	"videos,movies"						, "Movies",
	"videos,movietitles"				, "Movie Titles",
	"videos,tvshows "					, "TV Shows",
	"videos,tvshowtitles "				, "TV Show Titles",
	"videos,musicvideos"				, "Music Videos",
	"videos,recentlyaddedmovies"		, "Recently Added Movies",
	"videos,recentlyaddedepisodes"		, "Recently Added Episodes",
	"videos,recentlyaddedmusicvideos"	, "Recently Added Music Videos"
]

_windows = [
	"global"							, "Global",
	"fullscreenvideo"					, "Fullscreen Video",
	"fullscreenlivetv"					, "Fullscreen Live TV",
	"home"								, "Home",
	"programs"							, "Programs",
	"videos"							, "Videos",
	"music"								, "Music",
	"pictures"							, "Pictures",
	"filemanager"						, "File Manager",
	"virtualkeyboard"					, "Virtual Keyboard",
	"playercontrols"					, "Player Controls",
	"seekbar"							, "Seek bar",
	"musicosd"							, "Music OSD",
	"osdvideosettings"					, "Video OSD Settings",
	"osdaudiosettings"					, "Audio OSD Settings",
	"visualisation"						, "Visualisation",
	"slideshow"							, "Slideshow"
]


class KeyEditor(object):

	def __init__(self, defaultkeymap, userkeymap):
		self.WINDOWS = OrderedDict(zip(_windows[0::2], _windows[1::2]))
		self.ACTIONS = self._get_action_dict()
		self.defaultkeymap = defaultkeymap
		self.userkeymap = userkeymap
		self.dirty = False

	@staticmethod
	def rpc(method, **params):
		params = json.dumps(params)
		query = '{"jsonrpc": "2.0", "method": "%s", "params": %s, "id": 1}' % (method, params)
		return json.loads(xbmc.executeJSONRPC(query))

	def start(self):
		while True:
			idx = xbmcgui.Dialog().select(commons.translate(30007), self.WINDOWS.values())
			if idx == -1:
				break
			window = self.WINDOWS.keys()[idx]
			while True:
				idx = xbmcgui.Dialog().select(commons.translate(30008), self.ACTIONS.keys())
				if idx == -1:
					break
				category = self.ACTIONS.keys()[idx]
				while True:
					curr_keymap = self._current_keymap(window, category)
					labels = ["%s - %s" % (name, key) for _, key, name in curr_keymap]
					idx = xbmcgui.Dialog().select(commons.translate(30009), labels)
					if idx == -1:
						break
					action, oldkey, _ = curr_keymap[idx]
					newkey = KeyListener.record_key()
					if newkey is None:
						continue
					old = (window, action, oldkey)
					new = (window, action, newkey)
					if old in self.userkeymap:
						self.userkeymap.remove(old)
					self.userkeymap.append(new)
					if old != new:
						self.dirty = True

	def _current_keymap(self, window, category):
		actions = OrderedDict([(action, "") for action in self.ACTIONS[category].keys()])
		for w, a, k in self.defaultkeymap:
			if w == window:
				if a in actions.keys():
					actions[a] = k
		for w, a, k in self.userkeymap:
			if w == window:
				if a in actions.keys():
					actions[a] = k
		names = self.ACTIONS[category]
		return [(action, key, names[action]) for action, key in actions.iteritems()]

	def action_dict(self, actions, action_names):
		"""
		Create dict of action->name sorted by name
		"""
		return OrderedDict(sorted(zip(actions, action_names), key=lambda t: t[1]))

	def _get_run_addon_actions(self):
		addons = []
		addon_types = ['xbmc.python.pluginsource', 'xbmc.python.script']
		for addon_type in addon_types:
			response = KeyEditor.rpc('Addons.GetAddons', type=addon_type, properties=['name', 'enabled'])
			res = response['result']
			if 'addons' in res:
				addons.extend([a for a in res['addons'] if a['enabled']])
		actions = ['runaddon(%s)' % a['addonid'] for a in addons]
		names = ['Launch %s' % a['name'] for a in addons]
		return self.action_dict(actions, names)


	def _get_activate_window_actions(self):
		all_windows = _activate_window + _windows[2:]
		actions = ["activatewindow(%s)" % w_id for w_id in all_windows[0::2]]
		names = ["Open %s" % w for w in all_windows[1::2]]
		return self.action_dict(actions, names)

	def _get_action_dict(self):
		"""
		Map actions to 'category name'->'action id'->'action name' dict
		"""
		d = OrderedDict()
		for elem in _actions:
			category = elem[0]
			actions = elem[1][0::2]
			names = elem[1][1::2]
			d[category] = OrderedDict(zip(actions, names))
		d["Windows"] = self._get_activate_window_actions()
		d["Add-ons"] = self._get_run_addon_actions()
		return d


class KeyListener(xbmcgui.WindowXMLDialog):
	TIMEOUT = 5

	def __new__(cls):
		return super(KeyListener, cls).__new__(cls, "DialogKaiToast.xml", "")

	def __init__(self):
		self.key = None

	def onInit(self):
		try:
			self.getControl(401).addLabel(commons.translate(30002))
			self.getControl(402).addLabel(commons.translate(30010) % self.TIMEOUT)
		except AttributeError:
			self.getControl(401).setLabel(commons.translate(30002))
			self.getControl(402).setLabel(commons.translate(30010) % self.TIMEOUT)

	def onAction(self, action):
		code = action.getButtonCode()
		self.key = None if code == 0 else str(code)
		self.close()

	@staticmethod
	def record_key():
		dialog = KeyListener()
		timeout = Timer(KeyListener.TIMEOUT, dialog.close)
		timeout.start()
		dialog.doModal()
		timeout.cancel()
		key = dialog.key
		del dialog
		return key


class OrderedDict(dict):
	"""
	Dictionary that remembers insertion order

	An inherited dict maps keys to values.
	The inherited dict provides __getitem__, __len__, __contains__, and get.
	The remaining methods are order-aware.
	Big-O running times for all methods are the same as for regular dictionaries.

	The internal self.__map dictionary maps keys to links in a doubly linked list.
	The circular doubly linked list starts and ends with a sentinel element.
	The sentinel element never gets deleted (this simplifies the algorithm).
	Each link is stored as a list of length three:	[PREV, NEXT, KEY].
	"""

	def __init__(self, *args, **kwds):
		"""
		Initialize an ordered dictionary.	Signature is the same as for
		regular dictionaries, but keyword arguments are not recommended
		because their insertion order is arbitrary.
		"""
		if len(args) > 1:
			raise TypeError('expected at most 1 arguments, got %d' % len(args))
		try:
			self.__root
		except AttributeError:
			self.__root = root = []										 # sentinel node
			root[:] = [root, root, None]
			self.__map = {}
		self.__update(*args, **kwds)

	def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
		"""
		od.__setitem__(i, y) <==> od[i]=y
		Setting a new item creates a new link which goes at the end of the linked
		list, and the inherited dictionary is updated with the new key/value pair.
		:param key:
		:param value:
		:param dict_setitem:
		:return:
		"""
		if key not in self:
			root = self.__root
			last = root[0]
			last[1] = root[0] = self.__map[key] = [last, root, key]
		dict_setitem(self, key, value)

	def __delitem__(self, key, dict_delitem=dict.__delitem__):
		'od.__delitem__(y) <==> del od[y]'
		# Deleting an existing item uses self.__map to find the link which is
		# then removed by updating the links in the predecessor and successor nodes.
		dict_delitem(self, key)
		link_prev, link_next, key = self.__map.pop(key)
		link_prev[1] = link_next
		link_next[0] = link_prev

	def __iter__(self):
		"""
		od.__iter__() <==> iter(od)
		"""
		root = self.__root
		curr = root[1]
		while curr is not root:
			yield curr[2]
			curr = curr[1]

	def __reversed__(self):
		"""
		od.__reversed__() <==> reversed(od)
		"""
		root = self.__root
		curr = root[0]
		while curr is not root:
			yield curr[2]
			curr = curr[0]

	def clear(self):
		"""
		od.clear() -> None.	Remove all items from od.
		"""
		try:
			for node in self.__map.itervalues():
				del node[:]
			root = self.__root
			root[:] = [root, root, None]
			self.__map.clear()
		except AttributeError:
			pass
		dict.clear(self)

	def popitem(self, last=True):
		"""
		od.popitem() -> (k, v), return and remove a (key, value) pair.
		Pairs are returned in LIFO order if last is true or FIFO order if false.
		"""
		if not self:
			raise KeyError('dictionary is empty')
		root = self.__root
		if last:
			link = root[0]
			link_prev = link[0]
			link_prev[1] = root
			root[0] = link_prev
		else:
			link = root[1]
			link_next = link[1]
			root[1] = link_next
			link_next[0] = root
		key = link[2]
		del self.__map[key]
		value = dict.pop(self, key)
		return key, value

	def keys(self):
		"""
		od.keys() -> list of keys in od
		"""
		return list(self)

	def values(self):
		"""
		od.values() -> list of values in od
		"""
		return [self[key] for key in self]


	def items(self):
		"""
		od.items() -> list of (key, value) pairs in od
		"""
		return [(key, self[key]) for key in self]

	def iterkeys(self):
		"""
		od.iterkeys() -> an iterator over the keys in od
		"""
		return iter(self)

	def itervalues(self):
		"""
		od.itervalues -> an iterator over the values in od
		"""
		for k in self:
			yield self[k]

	def iteritems(self):
		"""
		od.iteritems -> an iterator over the (key, value) items in od
		"""
		for k in self:
			yield (k, self[k])

	def update(*args, **kwds):
		"""
		od.update(E, **F) -> None.	Update od from dict/iterable E and F.
		If E is a dict instance, does:					 for k in E: od[k] = E[k]
		If E has a .keys() method, does:				 for k in E.keys(): od[k] = E[k]
		Or if E is an iterable of items, does:	 for k, v in E: od[k] = v
		In either case, this is followed by:		 for k, v in F.items(): od[k] = v
		"""
		if len(args) > 2:
			raise TypeError('update() takes at most 2 positional '
							'arguments (%d given)' % (len(args),))
		elif not args:
			raise TypeError('update() takes at least 1 argument (0 given)')
		self = args[0]
		# Make progressively weaker assumptions about "other"
		other = ()
		if len(args) == 2:
			other = args[1]
		if isinstance(other, dict):
			for key in other:
				self[key] = other[key]
		elif hasattr(other, 'keys'):
			for key in other.keys():
				self[key] = other[key]
		else:
			for key, value in other:
				self[key] = value
		for key, value in kwds.items():
			self[key] = value
	__update = update	# let subclasses override update without breaking __init__
	__marker = object()

	def pop(self, key, default=__marker):
		"""
		od.pop(k[,d]) -> v, remove specified key and return the corresponding value.
		If key is not found, d is returned if given, otherwise KeyError is raised.
		"""
		if key in self:
			result = self[key]
			del self[key]
			return result
		if default is self.__marker:
			raise KeyError(key)
		return default

	def setdefault(self, key, default=None):
		"""
		od.setdefault(k[,d]) -> od.get(k,d), also set od[k]=d if k not in od
		"""
		if key in self:
			return self[key]
		self[key] = default
		return default

	def __repr__(self, _repr_running={}):
		"""
		od.__repr__() <==> repr(od)
		"""
		call_key = id(self), _get_ident()
		if call_key in _repr_running:
			return '...'
		_repr_running[call_key] = 1
		try:
			if not self:
				return '%s()' % (self.__class__.__name__,)
			return '%s(%r)' % (self.__class__.__name__, self.items())
		finally:
			del _repr_running[call_key]

	def __reduce__(self):
		"""
		Return state information for pickling
		"""
		items = [[k, self[k]] for k in self]
		inst_dict = vars(self).copy()
		for k in vars(OrderedDict()):
			inst_dict.pop(k, None)
		if inst_dict:
			return (self.__class__, (items,), inst_dict)
		return self.__class__, (items,)

	def copy(self):
		"""
		od.copy() -> a shallow copy of od
		"""
		return self.__class__(self)

	@classmethod
	def fromkeys(cls, iterable, value=None):
		"""
		OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
		and values equal to v (which defaults to None).
		"""
		d = cls()
		for key in iterable:
			d[key] = value
		return d

	def __eq__(self, other):
		"""
		od.__eq__(y) <==> od==y.	Comparison to another OD is order-sensitive
		while comparison to a regular mapping is order-insensitive.
		"""
		if isinstance(other, OrderedDict):
			return len(self) == len(other) and self.items() == other.items()
		return dict.__eq__(self, other)


	def __ne__(self, other):
		return not self == other

	def viewkeys(self):
		"""
		od.viewkeys() -> a set-like object providing a view on od's keys
		"""
		return KeysView(self)

	def viewvalues(self):
		"""
		od.viewvalues() -> an object providing a view on od's values
		"""
		return ValuesView(self)

	def viewitems(self):
		"""
		od.viewitems() -> a set-like object providing a view on od's items
		"""
		return ItemsView(self)
