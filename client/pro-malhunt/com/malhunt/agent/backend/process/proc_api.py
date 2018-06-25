from threading import Thread
import wmi
import os
import time
import pythoncom

# TODO: Remove on elastic search
import re


class proc_api:
	file_name = 'process_db.txt'
	def __init__(self):
		self.wmi_obj = wmi.WMI()
		with open(self.file_name, 'w+') as fw:
			fw.truncate()
	
	def add_process(self, pid, proc_name):
		'''
		Adds process entries to database
		
		pid: process_id of process to be added
		proc_name: process name of process to be added
		'''
		
		# TODO Change to elastic search
		with open(self.file_name, 'a+') as fw:
			fw.write('{} {}'.format(pid, proc_name))
			fw.write(os.linesep)
	
	def rem_process(self, pid, proc_name):
		'''
		Removes process entries from database
		
		pid: process_id of process to be removed
		proc_name: process name of process to be removed
		'''
		
		# TODO Change to elastic search
		with open(self.file_name, 'a+') as fw:
			fw.write('-{} {}'.format(pid, proc_name))
			fw.write(os.linesep)
	
	def check_process(process_name):
		'''
		Queries in a database and checks if process name exists
		
		'''
		
		# TODO Change to elastic search
		try:
			with open(self.file_name, 'r+') as fw:
				all_proc = fw.read()
				proc = re.finditer(r".*{}$".format(process_name), all_proc, flags = re.MULTILINE)
				proc_name = next(proc)
				return True
		except StopIteration:
			return False
	
	def fill_process(self):
		'''
		Enumerates all the currently existing processes and adds to db
		
		'''
		for process in self.wmi_obj.Win32_Process():
			self.add_process(process.ProcessId, process.Name)

	def creat_proc_callback(self):
		'''
		Watches for new processes and adds to database
		
		'''
		
		pythoncom.CoInitialize()
		wmi_obj_th = wmi.WMI()
		proc_watcher = wmi_obj_th.Win32_Process.watch_for("creation")
		while True:
			new_proc = proc_watcher()
			self.add_process(new_proc.ProcessId, new_proc.Name)

	def delet_proc_callback(self):
		'''
		Watches for deleted processes and removes from database
		
		'''
		
		pythoncom.CoInitialize()
		wmi_obj_th = wmi.WMI()
		proc_watcher = wmi_obj_th.Win32_Process.watch_for("deletion")
		while True:
			new_proc = proc_watcher()
			self.rem_process(new_proc.ProcessId, new_proc.Name)

	def proc_api(self):
		'''
		Starts up the entire process filling and updating task
		
		'''
	
		self.fill_process()
		proc_creat_th = Thread(target = self.creat_proc_callback)
		proc_delet_th = Thread(target = self.delet_proc_callback)
		proc_creat_th.start()
		proc_delet_th.start()
		
		proc_creat_th.join()
		proc_delet_th.join()

if __name__ == '__main__':
	proc_obj = proc_api()
	proc_obj.proc_api()