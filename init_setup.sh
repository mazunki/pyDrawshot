DS_SHORTCUT="+ctrl +shift +f12"
BUTTON="1"

dconf dump / >~/.config/dconf/user.conf
/usr/bin/python3 ./get_next_custom_kb_value.py $DS_SHORTCUT
dconf load / <~/.config/dconf/user.conf

xsetwacom --set 20 button $BUTTON key $DS_SHORTCUT