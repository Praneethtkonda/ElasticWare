import os
import fnmatch
import FileSystemWatcher
import sys
import time
import configparser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from com.malhunt.agent.backend.db.ElasticsearchController import ESController


class FileEventsHandler(PatternMatchingEventHandler):
    es_handle = ESController()

    def on_moved(self, event):
        self.process_event(event)

    def on_deleted(self, event):
        self.process_event(event)

    def on_created(self, event):
        self.process_event(event)

    def process_event(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        if event.event_type == 'created':
            self.add_file(filepath=event.src_path)
        elif event.event_type == 'deleted':
            self.remove_file(filepath=event.src_path)
        elif event.event_type == 'moved':
            self.remove_file(filepath=event.src_path)
            self.add_file(filepath=event.dest_path)

    def add_file(self, filepath):
        ''' Insert file record into ES '''
        self.es_handle.insertItem(name=filepath, type='file')

    def remove_file(self, filepath):
        ''' Remove file record from ES '''
        self.es_handle.purgeItem(name=filepath, type='file')

    def get_files(self, name_regex):
        ''' Get file records from ES whose names match the specified regex '''
        return self.es_handle.fuzzyGetItem(name_regex)

    def check_files(self, name_regex):
        ''' Check if file records in ES whose names match the specified regex '''
        return self.es_handle.fuzzyCheckItem(name_regex)


class Filelist:
    """ Lists all the files present in the given path """

    def filenames(self, path):
        configfiles = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(path) for f in
                       fnmatch.filter(files, '*.*')]
        with open(r"C:\Users\ganesh.vernekar\Documents\python_progs\wfile.txt", 'w') as fp:
            for files in configfiles:
                fp.write(files + "\n")


class FileUpdater:
    """ Monitors hardisks for addition, deletion and rename of files """

    def setObserver(self, path_list):
        observer = Observer()
        thread = []
        for path in path_list:
            observer.schedule(FileEventsHandler(), path, recursive=True)
            thread.append(observer)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.readfp(open(os.path.dirname(__file__) + '/../config/mhprop.ini'))
    paths = (config['DEFAULT']['file_watch_directories']).split(',')
    file_updater = FileUpdater()
    print "Initiating..."
    file_updater.setObserver(paths)
