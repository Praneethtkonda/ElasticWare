from threading import Thread
import unittest
import sys
sys.path.insert('../')
from process.proc_api import proc_api
import time
from com.malhunt.agent.backend.db.ElasticsearchController import ESController
import wmi


class proc_api:
	'''
	proc_api checks for running processes agent to access process related operations
	'''
	
	
	@classmethod
	def setUpClass(cls):
		cls.proc_obj = proc_api()
		cls.creat_th = Thread(cls.proc_obj.proc_api)
		cls.creat_th.start()
		time.sleep(5)
		
	def setUp(self):
		self.proc_obj = proc_api()
		self.wmi_obj = wmi.WMI()
	
	def tearDownClass(cls):
		cls.creat_th._stop()

	def test_check_for_all_proc(self):
		for process in self.wmi_obj.Win32_Process():
			self.assertTrue(self.proc_obj.check_process(process.Name))
	
	def test_new_process(self):
		process_id, return_value = self.proc_obj.Win32_Process.Create(CommandLine="notepad.exe")
		time.sleep(1)
		self.proc_obj.check_process("notepad.exe")
		self.assertTrue(self.proc_obj.check_process('notepad.exe'))
		for process in self.wmi_obj.Win32_Process(ProcessId=process_id):
			result = process.Terminate ()
