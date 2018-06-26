import os
import fnmatch
import FileSystemWatcher
import time
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class FileHandler(PatternMatchingEventHandler):
    patterns = ["*.*"]

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        if event.event_type == 'moved':
            print event.src_path + " renamed/moved to " + event.dest_path, event.event_type  # print now only for degug
        else:
            print event.src_path, event.event_type

    def on_moved(self, event):
        self.process(event)

    def on_deleted(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)


class Filelist:
    """ Lists all the files present in the given path """

    def filenames(self, path):
        configfiles = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path) for f in
                       fnmatch.filter(files, '*.*')]
        with open(r"C:\Users\ganesh.vernekar\Documents\python_progs\wfile.txt", 'w') as fp:
            for files in configfiles:
                fp.write(files + "\n")


class UpdatedFilelist:
    """ Monitors hardisks for addition, deletion and rename of files """

    def filenames(self, path_list):

        observer = Observer()
        thread = []
        for path in path_list:
            observer.schedule(FileHandler(), path, recursive=True)
            thread.append(observer)

        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()


if __name__ == '__main__':
    path = "C://"
    path2 = "C://Users/qauser/Documents/a"  # ive given this only to test because changing it to C:// will output a lot of changes
    path3 = "C://Users/qauser/Documents/b"
    #obj1 = Filelist()
    obj2 = UpdatedFilelist()
    print " initiating "
    obj2.filenames([path2, path3])
