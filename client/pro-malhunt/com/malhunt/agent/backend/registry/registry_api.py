from threading import Thread
import winreg
import os
import time

# TODO: Remove on elastic search
import re


class registry_api:
	file_name = 'registry_db.txt'
	key_path_pairs = [
		(winreg.HKEY_LOCAL_MACHINE, "Computer\\HKEY_LOCAL_MACHINE"),
		(winreg.HKEY_USERS, "Computer\\HKEY_USERS"),
		(winreg.HKEY_CURRENT_USER, "Computer\\HKEY_CURRENT_USER"),
		(winreg.HKEY_CLASSES_ROOT, "Computer\\HKEY_CLASSES_ROOT"),
		(winreg.HKEY_PERFORMANCE_DATA, "Computer\\HKEY_PERFORMANCE_DATA"),
		(winreg.HKEY_CURRENT_CONFIG, "Computer\\HKEY_CURRENT_CONFIG")
	]
	def __init__(self):
		with open(self.file_name, 'w+') as fw:
			fw.truncate()
	
	def add_registry(self, registry_key):
		'''
		Adds registry entries to database
		
		registry_key: registry key to be stored
		'''
		
		# TODO Change to elastic search and add further features for values
		with open(self.file_name, 'a+', encoding = 'utf-8') as fw:
			fw.write('{}'.format(registry_key))
			fw.write(os.linesep)
	
	def rem_registry(self, registry_key):
		'''
		Adds registry entries to database
		
		registry_key: registry key to be stored
		'''
		
		# TODO Change to elastic search
		with open(self.file_name, 'a+') as fw:
			fw.write('-{}'.format(registry_key))
			fw.write(os.linesep)
	
	def check_registry(self, registry_key):
		'''
		Queries in a database and checks if process name exists
		
		'''
		
		# TODO Change to elastic search
		try:
			with open(self.file_name, 'r+') as fw:
				all_keys = fw.read()
				key = re.finditer(r".*{}$".format(registry_key), all_keys, flags = re.MULTILINE)
				key_name = next(key)
				return True
		except StopIteration:
			return False
	
	def list_all_keys(self, key, key_name):
		'''
		list_all_keys: list<string>
		
		key : opened key handle, closed after recursion
		key_name: string name of key
		'''
		
		ctr = 0
		while True:
			try:
				subkey = winreg.EnumKey(key, ctr)
				subkey_name = "{}\\{}".format(key_name, subkey)
				self.add_registry(subkey_name)
				key_handle = winreg.OpenKey(key, subkey)
				self.list_all_keys(key_handle, subkey_name)
				key_handle.Close()
				ctr += 1
			except OSError:
				break

	
	def fill_keys(self):
		'''
		Enumerates all the currently existing processes and adds to db
		
		'''
		
		for key, path in self.key_path_pairs:
			self.list_all_keys(key, path)

	def add_rem_key_callback(self):
		'''
		Watches for registries added or removed
		'''
		pass

	def mod_key_callback(self):
		'''
		Watches for registry values modified
		'''
		pass
		

	def registry_api(self):
		'''
		Starts up the entire process filling and updating task
		
		'''

		self.fill_keys()
		# self.add_rem_key_callback()

if __name__ == '__main__':
	registry_obj = registry_api()
	registry_obj.registry_api()