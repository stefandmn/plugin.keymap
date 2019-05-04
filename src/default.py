# -*- coding: utf-8 -*-

import os
import sys
import shutil
import commons
from editor import KeyEditor
import xml.etree.ElementTree as ET

if hasattr(sys.modules["__main__"], "xbmc"):
	xbmc = sys.modules["__main__"].xbmc
else:
	import xbmc

if hasattr(sys.modules["__main__"], "xbmcgui"):
	xbmcgui = sys.modules["__main__"].xbmcgui
else:
	import xbmcgui


class KeymapEditor:

	def __init__(self):
		self.userdata = xbmc.translatePath('special://userdata/keymaps')
		self.userkeymapfile = os.path.join(self.userdata, 'gen.xml')
		self.userkeymap = []
		self.syskeymapfile = xbmc.translatePath('special://xbmc/system/keymaps/keyboard.xml')
		self.syskeymap = []
		try:
			if not os.path.exists(self.userdata):
				os.makedirs(self.userdata)
			else:
				# make sure there are no user defined keymaps
				for name in os.listdir(self.userdata):
					if name.endswith('.xml') and name != os.path.basename(self.userkeymapfile):
						src = os.path.join(self.userdata, name)
						for i in xrange(100):
							dst = os.path.join(self.userdata, "%s.bak.%d" % (name, i))
							if os.path.exists(dst):
								continue
							shutil.move(src, dst)
							# successfully renamed
							break
		except Exception as ex:
			KeyEditor.rpc('GUI.ShowNotification', title="Keymap Editor", message=commons.translate(30011), image='error')
			commons.debug("Failed to remove old keymap file: %s" %str(ex))
		# load system keymap
		if os.path.exists(self.syskeymapfile):
			try:
				self.syskeymap = self.getKeymap(self.syskeymapfile)
			except Exception as ex:
				KeyEditor.rpc('GUI.ShowNotification', title="Keymap Editor", message=commons.translate(30012), image='error')
				commons.error("Failed to load system keymap file: %s" %str(ex))
		# load user keymap
		if os.path.exists(self.userkeymapfile):
			try:
				self.userkeymap = self.getKeymap(self.userkeymapfile)
			except Exception as ex:
				KeyEditor.rpc('GUI.ShowNotification', title="Keymap Editor", message=commons.translate(30013), image='error')
				commons.error("Failed to load user keymap file: %s" %str(ex))

	def getKeymap(self, filename):
		ret = []
		with open(filename, 'r') as xml:
			tree = ET.iterparse(xml)
			for _, keymap in tree:
				for context in keymap:
					for device in context:
						for mapping in device:
							key = mapping.get('id') or mapping.tag
							action = mapping.text
							if action:
								ret.append((context.tag.lower(), action.lower(), key.lower()))
		return ret

	def setKeymap(self, keymap, filename):
		contexts = list(set([c for c, a, k in keymap]))
		builder = ET.TreeBuilder()
		builder.start("keymap", {})
		for context in contexts:
			builder.start(context, {})
			builder.start("keyboard", {})
			for c, a, k in keymap:
				if c == context:
					builder.start("key", {"id": k})
					builder.data(a)
					builder.end("key")
			builder.end("keyboard")
			builder.end(context)
		builder.end("keymap")
		element = builder.close()
		ET.ElementTree(element).write(filename, 'utf-8')

	def execute(self):
		confirm_discard = False
		while True:
			idx = xbmcgui.Dialog().select(commons.translate(30000), [commons.translate(30003), commons.translate(30004), commons.translate(30005)])
			if idx == 0:
				# edit
				editor = KeyEditor(self.syskeymap, self.userkeymap)
				editor.start()
				confirm_discard = editor.dirty
			elif idx == 1:
				# reset
				confirm_discard = bool(self.userkeymap)
				self.userkeymap = []
			elif idx == 2:
				# save
				if os.path.exists(self.userkeymapfile):
					shutil.copyfile(self.userkeymapfile, self.userkeymapfile + ".old")
				self.setKeymap(self.userkeymap, self.userkeymapfile)
				xbmc.executebuiltin("action(reloadkeymaps)")
				break
			elif idx == -1 and confirm_discard:
				if xbmcgui.Dialog().yesno(commons.translate(30000), commons.translate(30006)) == 1:
					break
			else:
				break
		sys.modules.clear()


if __name__ == "__main__":
	editor = KeymapEditor()
	editor.execute()
	del editor
