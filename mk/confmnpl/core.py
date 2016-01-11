#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import shutil
from colortext import *
from variables import *

def path(list):
	str = '.'
	for s in list:
		str +=  '/' + s
	return str

def title(str): 	return color(str, title_color)
def decl(str):		return color(str, decl_color)
def good(str): 		return color(str, good_color)
def bad(str): 		return color(str, bad_color)

def current_name():
	return open(path([curdir, profile])).read();

def current_name_set(name):
	try:
		open(path([curdir, profile]), 'w').write(name);
	except:
		print(bad("I cant set profilename 0_o"))
		exit()

def echo_copytree(src, dst):
	print(yellow("copytree ") + src + ' ' +dst)
	try:
		shutil.copytree(src, dst)
	except:
		print bad("copytree error")
		exit()
		
from datetime import datetime

def echo_rmtree(tree):
	print (yellow("delete ") + tree)
	if not os.path.exists(cm_basket):
		os.mkdir(cm_basket)
	now = datetime.now()

	str = datetime.strftime(datetime.now(), "%Y.%m.%d_%H:%M:%S")
	shutil.copytree(tree, path([cm_basket, str]))
	dirs=[]
	dirst = []
	while len(dirs) > 20:
		dirs = os.listdir(cm_basket)
		dirst = []
		for d in dirs:
			dirst.append([d, os.path.getmtime('.cm_basket/' + d)])
		l = sorted(dirst, key=lambda dirst: dirst[1])
		shutil.rmtree(path([cm_basket, l[0][0]]))
		#print (sorted(dirst, key = dirst[1])[-1])
		pass
	try:
		shutil.rmtree(tree)
	except:
		try:
			os.rmdir(tree)
		except:
			print (tree + " is not exist. do nothing")
			return
	
def save_ex(name):
	return os.path.exists(path([savedir, name]))

def super_ex(name):
	return os.path.exists(path([superdir, name]))

def cur_ex():
	return os.path.exists(path([curdir]))

def are_you_sure():
	print("Are you sure?")
	if raw_input() == 'y' or raw_input() == 'Y':
		return
	else:
		exit() 
