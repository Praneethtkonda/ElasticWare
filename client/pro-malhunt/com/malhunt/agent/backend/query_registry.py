import os
import re

'''
SAMPLE FILE TO STORE REGISTRY KEYS
FOR NOW WE'LL USE FILE INSTEAD OF DB
'''


def search_registry(key):
	'''
	Searches the registry database (for now file) and returns if key is present
	
	key(str): key_name
	'''
	
	storage_fname = 'all_keys.txt'
	search_regex = '[^\\]+'
	
	# Will be replaced with function call to refer DB
	# Reads through storage_fname and tells if key exists
	with open(storage_fname) as fp:
		registry = fp.read()
		a = re.findall(r".*{}$".format(key), registry, flags = re.MULTILINE)
		return len(a) != 0

if __name__ == '__main__':
	print(search_registry('Elements'))