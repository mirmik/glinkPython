#!/usr/bin/python
# -*- coding: UTF-8 -*-

#import variables

def color(str, ccolor):
	if ccolor == 0: return str
	return "\033[1;" + repr(ccolor) + "m" + str + "\033[1;m"

cpurple = 35
cred = 31
cblue = 34
cgreen = 32
cyellow = 33
nocolor = 0

def purple(str): 	return color(str, cpurple)
def yellow(str): 	return color(str, cyellow)
def red(str):   	return color(str, cred)
def green(str): 	return color(str, cgreen)
def blue(str):  	return color(str, cblue)
