from file.file_api import UpdatedFilelist
from process.proc_api import proc_api
from threading import Thread

def init():
	proc_upd_th = Thread(self._update_proc)
	file_upd_th = Thread(self._update_file)
	reg_upd_th = Thread(self._update_reg)
	proc_upd_th.start()
	file_upd_th.start()
	reg_upd_th.start()
	proc_upd_th.join()
	file_upd_th.join()
	reg_upd_th.join()

def _update_file(self):
	pass
	
def _update_proc(self):
	'''
	Creates a threads for process updates
	'''
	
	proc_obj = proc_api()
	proc_obj.add_proc_callbacks()

def _update_reg(self):
	pass

	
if __name__ == '__main__':
	init()