"""
	Searches for the last keyboard shortcut definded by the user, and outputs its next value
	to 	the standard output of the program. Called upon by init_setup.sh, 
	
	(--
	which then uses `$?` to access its value.
	Since we are only interested in a number, this works, as long as there is no more 
	than 255 user-defined shortcuts. 
	--)

	and this script creates the file now.

	An alternative, possibly better, as Python might not be intstalled, 
	way would be to use `sed`.
"""

import re
from sys import argv
#SHORTCUT = "<Primary><Shift>F12"  # <Primary> is <Control> in Linux, and <Command> in MacOS, usually.
SHORTCUT = " ".join(argv[1:])

from os.path import expanduser
home = expanduser("~")
dconf_location = "{}/.config/dconf/user.conf".format(home)

with open(dconf_location, "r") as f:
	f_str = f.read()


matches = re.findall("\[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom[0-9]*\]", f_str)

last_saved = None
for shortcut_dir in matches:
	found_digit = re.search("\d", shortcut_dir)
	if last_saved is not None and found_digit > last_saved:  # shouldn't be necessary as dconf already sorts it
		last_saved = found_digit
if last_saved == None:  # if user hasn't defined anything
	last_saved = 0

new_shortuct_script = """[org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom{}]
binding='{}'
command='/usr/bin/python3 /home/mazunki/pyDrawshot/main.py'
name='pyDrawShot window'
""".format(last_saved, SHORTCUT)
with open(dconf_location, "a") as f:  # never change modus to `w`, this would delete all recorded shortcuts
	f.write(new_shortuct_script)
print("Created shortuct {} for the script!".format(SHORTCUT))