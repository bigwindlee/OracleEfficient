#!/usr/bin/env python

import sys, webbrowser, re


for bugno in sys.argv[1:]:
	if not re.compile(r'[0-9]{8}').match(bugno):
		print('Bad bugno: ' + bugno)
		continue
	url = 'https://bug.oraclecorp.com/pls/bug/webbug_edit.edit_info_top?rptno=' + bugno
	webbrowser.open_new_tab(url)
	
