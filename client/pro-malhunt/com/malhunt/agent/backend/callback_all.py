from file.file_api import FileUpdater
from process.proc_api import proc_api
from threading import Thread
import os
import configparser
import pythoncom
import watchdog

def init():
	proc_upd_th = Thread(target = _update_proc)
	file_upd_th = Thread(target = _update_file)
	reg_upd_th = Thread(target = _update_reg)
	proc_upd_th.start()
	file_upd_th.start()
	reg_upd_th.start()
	proc_upd_th.join()
	file_upd_th.join()
	reg_upd_th.join()

def _update_file():
	config = configparser.ConfigParser()
	config.readfp(open(os.path.dirname(__file__) + '/config/mhprop.ini'))
	paths = (config['DEFAULT']['file_watch_directories']).split(',')
	file_updater = FileUpdater()
	print "Initiating file update....."
	file_updater.setObserver(paths)

def _update_proc():
	'''
	Creates a threads for process updates
	'''

	print("Initiating process update.....")
	pythoncom.CoInitialize()
	proc_obj = proc_api()
	proc_obj.add_proc_callbacks()

def _update_reg():
	pass

	
if __name__ == '__main__':
	init()