from threading import Thread
import wmi
import os
import time
import pythoncom
from com.malhunt.agent.backend.db.ElasticsearchController import ESController

class proc_api:
	'''
	proc_api allows agent to access process related operations
	'''
	es_handle = ESController()

	def __init__(self):
		self.wmi_obj = wmi.WMI()
	
	def add_process(self, pid, proc_name):
		'''
		Adds process entries to database
		
		pid: process_id of process to be added
		proc_name: process name of process to be added
		'''
		
		# TODO: Unit-testing and Logging
		#print 'Adding process: pid- {}, name-'.format(pid,proc_name)
		print self.es_handle.insertItem(name=proc_name, type='proc', id=str(pid))
	
	def rem_process(self, pid, proc_name):
		'''
		Removes process entries from database
		
		pid: process_id of process to be removed
		proc_name: process name of process to be removed
		'''
		
		# TODO: Unit-testing and Logging
		try:
			print self.es_handle.purgeItem(name=proc_name, type='proc', id=str(pid))
		except Exception:
			print "Coudn't remove process {}".format(proc_name)
	
	def check_process(self, process_name):
		'''
		Queries ES and checks if process name exists
		
		'''
		return self.es_handle.fuzzyCheckItem(regex=process_name, type='proc')

	def get_process(self, process_name):
		'''
        Queries ES and gets the matching processes exists
        '''
		return self.es_handle.fuzzyGetItem(regex=process_name, type='proc')
	
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
			self.add_process(new_proc.ProcessId, new_proc.Caption)

	def delet_proc_callback(self):
		'''
		Watches for deleted processes and removes from database
		
		'''
		
		pythoncom.CoInitialize()
		wmi_obj_th = wmi.WMI()
		proc_watcher = wmi_obj_th.Win32_Process.watch_for("deletion")
		while True:
			new_proc = proc_watcher()
			self.rem_process(new_proc.ProcessId, new_proc.Caption)

	def add_proc_callbacks(self):
		'''
		Creates separate threads to monitor creations and deletions of processes
		'''
		
		proc_creat_th = Thread(target = self.creat_proc_callback)
		proc_delet_th = Thread(target = self.delet_proc_callback)
		proc_creat_th.start()
		proc_delet_th.start()
		proc_creat_th.join()
		proc_delet_th.join()
	
	def proc_api(self):
		'''
		Starts up the entire process filling and updating task
		
		'''
	
		self.fill_process()
		self.add_proc_callbacks()

if __name__ == '__main__':
	proc_obj = proc_api()
	proc_obj.proc_api()
	#proc_obj.add_proc_callbacks()