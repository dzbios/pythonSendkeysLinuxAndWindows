#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
if os.name == 'nt':
	# Windows
	import win32com.client
	shell = win32com.client.Dispatch("WScript.Shell")
elif os.name == 'posix':
	# Linux
	import Xlib.display
	import Xlib.X
	import Xlib.XK
	import Xlib.protocol.event
	import Xlib.ext.xtest

	display = Xlib.display.Display()

	ctrlkey=display.keysym_to_keycode(Xlib.XK.XK_Control_L)
	altkey=display.keysym_to_keycode(Xlib.XK.XK_Alt_L)
	shiftkey=display.keysym_to_keycode(Xlib.XK.XK_Shift_L)

	specialKeys = (
	("BACKSPACE",Xlib.XK.XK_BackSpace),
	("BS",Xlib.XK.XK_BackSpace),
	("BKSP",Xlib.XK.XK_BackSpace),
	("BREAK",Xlib.XK.XK_Break),
	("CAPSLOCK",Xlib.XK.XK_Caps_Lock),
	("DELETE",Xlib.XK.XK_Delete),
	("DEL",Xlib.XK.XK_Delete),
	("DOWN",Xlib.XK.XK_Down),
	("END",Xlib.XK.XK_End),
	("ENTER",Xlib.XK.XK_KP_Enter),
	("ESC",Xlib.XK.XK_Escape),
	("HELP",Xlib.XK.XK_Help),
	("HOME",Xlib.XK.XK_KP_Home),
	("INSERT",Xlib.XK.XK_KP_Insert),
	("INS",Xlib.XK.XK_KP_Insert),
	("LEFT",Xlib.XK.XK_Left),
	("NUMLOCK",Xlib.XK.XK_Num_Lock),
	("PGDN",Xlib.XK.XK_KP_Page_Down),
	("PGUP",Xlib.XK.XK_KP_Page_Up),
	("PRTSC",Xlib.XK.XK_Print),
	("RIGHT",Xlib.XK.XK_Right),
	("SCROLLLOCK",Xlib.XK.XK_Scroll_Lock),
	("TAB",Xlib.XK.XK_Tab),
	("UP",Xlib.XK.XK_Up),
	("F1",Xlib.XK.XK_F1),
	("F2",Xlib.XK.XK_F2),
	("F3",Xlib.XK.XK_F3),
	("F4",Xlib.XK.XK_F4),
	("F5",Xlib.XK.XK_F5),
	("F6",Xlib.XK.XK_F6),
	("F7",Xlib.XK.XK_F7),
	("F8",Xlib.XK.XK_F8),
	("F9",Xlib.XK.XK_F9),
	("F10",Xlib.XK.XK_F10),
	("F11",Xlib.XK.XK_F11),
	("F12",Xlib.XK.XK_F12),
	("F13",Xlib.XK.XK_F13),
	("F14",Xlib.XK.XK_F14),
	("F15",Xlib.XK.XK_F15),
	("F16",Xlib.XK.XK_F16)
	)

def getSpecialkeycode(keyname):
	for speciealKey in specialKeys :
		if speciealKey[0] == keyname :
			return display.keysym_to_keycode(speciealKey[1])
	return 0

special_X_keysyms = {
	' ' : "space",
	'\t' : "Tab",
	'\n' : "Return",  # for some reason this needs to be cr, not lf
	'\r' : "Return",
	'\e' : "Escape",
	'!' : "exclam",
	'#' : "numbersign",
	'%' : "percent",
	'$' : "dollar",
	'&' : "ampersand",
	'"' : "quotedbl",
	'\'' : "apostrophe",
	'(' : "parenleft",
	')' : "parenright",
	'*' : "asterisk",
	'=' : "equal",
	'+' : "plus",
	',' : "comma",
	'-' : "minus",
	'.' : "period",
	'/' : "slash",
	':' : "colon",
	';' : "semicolon",
	'<' : "less",
	'>' : "greater",
	'?' : "question",
	'@' : "at",
	'[' : "bracketleft",
	']' : "bracketright",
	'\\' : "backslash",
	'^' : "asciicircum",
	'_' : "underscore",
	'`' : "grave",
	'{' : "braceleft",
	'|' : "bar",
	'}' : "braceright",
	'~' : "asciitilde"
}

def get_keysym(ch) :
	keysym = Xlib.XK.string_to_keysym(ch)
	if keysym == 0 :

		# Unfortunately, although this works to get the correct keysym
		# i.e. keysym for '#' is returned as "numbersign"
		# the subsequent display.keysym_to_keycode("numbersign") is 0.
		keysym = Xlib.XK.string_to_keysym(special_X_keysyms[ch])

	return keysym

def char_to_keycode(ch) :
	keysym = get_keysym(ch)
	keycode = display.keysym_to_keycode(keysym)
	keysym2=display.keycode_to_keysym(keycode,0)
	if keysym != keysym2 :
		return keycode , True
	else :
		return keycode , False

def pushkey(keycode,shift,ctrl,alt):

	# Press Shift Alt Ctrl key
	if ctrl :
		Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, ctrlkey)

	if shift :
		Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, shiftkey)

	if alt :
		Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, altkey)

	# Release Shift Alt Ctrl key
	Xlib.ext.xtest.fake_input(display, Xlib.X.KeyPress, keycode)
	Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, keycode)

	# Release special key
	if alt :
		Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, altkey)

	if shift :
		Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, shiftkey)

	if ctrl :
		Xlib.ext.xtest.fake_input(display, Xlib.X.KeyRelease, ctrlkey)

	# sync
	try:
		display.sync()
	except KeyboardInterrupt:
		pass

def sendkeysLinux(strings):

	groupFlag=False
	groupString = ""

	shift = ctrl = alt = False

	for ch in list(strings):

		if ch == '{':
			if not groupFlag :
				groupString = ""
				groupFlag = True 
				continue
		elif ch == '}':
			if groupString != "" :
				groupFlag = False
				ch = ''

		if groupFlag :
			groupString += ch
			continue
				
		if ch == '+':
			shift = True
			continue
		elif ch == '^':
			ctrl = True
			continue
		elif ch == '%':
			alt = True
			continue
				
		# ----- keycode Scan
		if groupString != "" and len(groupString)!=1:
			# Group Mode

			keycode = getSpecialkeycode(groupString)
			isNeedShift = False
			groupString = ""

		else :
			if groupString!="":
				chs = list(groupString)
				ch = chs[0]
				keycode,isNeedShift = char_to_keycode(ch)
			elif ch=='~':
				keycode = getSpecialkeycode("ENTER")
				isNeedShift = False
			else:
				keycode,isNeedShift = char_to_keycode(ch)

		if isNeedShift:
			shift = True
			ctrl  = False
			alt   = False

		# ----- keycode pushkey
		pushkey(keycode,shift,ctrl,alt)

		shift = False
		ctrl  = False
		alt   = False
		isNeedShift = False
		groupString = ""
		
def sendkeys(strings):

	if os.name == 'nt':
		#windows
		shell.SendKeys(strings, 0)
	elif os.name == 'posix':
		#linux
		sendkeysLinux(strings)
		


if __name__ == "__main__":

	keybuff = "dir~+dir-{+}{{}{}}{^}{%}{~}{(}{)} {BS}TAB -={+};*:!\"#$%&'()=|"

	print (keybuff)

	sendkeys(keybuff)

