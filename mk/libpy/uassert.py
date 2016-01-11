#!/usr/bin/python
# -*- coding: UTF-8 -*-

import colortext

def uassert(condition, message):
	if not condition:
		print(colortext.red(message))
		exit()
