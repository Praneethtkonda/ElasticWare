import os
import fnmatch
import FileSystemWatcher
import sys
import time
import configparser
from elasticsearch import NotFoundError
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from com.malhunt.agent.backend.db.ElasticsearchController import ESController
from com.malhunt.agent.backend.utils.md5calc import md5


class FileEventsHandler(PatternMatchingEventHandler):
    #TODO: See if this change shows up on CR's application
    #Again and again
    es_handle = ESController()

    def __init__(self):
        super(FileEventsHandler, self).__init__(ignore_patterns=set(['*Elastic\\Elasticsearch*']))

    def on_moved(self, event):
        self.process_event(event)

    def on_deleted(self, event):
        self.process_event(event)

    def on_created(self, event):
        self.process_event(event)

    def on_modified(self, event):
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
            self.add_file(filepath=event.src_path, md5=md5(event.src_path))
        elif event.event_type == 'deleted':
            self.remove_file(filepath=event.src_path)
        elif event.event_type == 'moved':
            self.remove_file(filepath=event.src_path)
            self.add_file(filepath=event.dest_path, md5=md5(event.dest_path))
        elif event.event_type == 'modified':
            self.add_file(filepath=event.src_path, md5=md5(event.src_path))

    def add_file(self, filepath, md5):
        ''' Insert file record into ES '''
        self.es_handle.insertItem(name=filepath, type='file', md5=md5)

    def remove_file(self, filepath):
        ''' Remove file record from ES '''
        try:
            self.es_handle.purgeItem(name=filepath, type='file')
        except NotFoundError:
            '''print 'Couldnot delete: Record for file {} not found!'.format(filepath)'''
            pass

    def get_files(self, name_regex):
        ''' Get file records from ES whose names match the specified regex '''
        return self.es_handle.fuzzyGetItem(regex=name_regex, type='file')

    def check_files(self, name_regex):
        ''' Check if file records in ES whose names match the specified regex '''
        return self.es_handle.fuzzyCheckItem(regex=name_regex, type='file')


class Filelist:
    """ Lists all the files present in the given path """
    es_handle = ESController()
    def filenames(self, path):
        for dirpath, dirnames, files in os.walk(path):
            for f in fnmatch.filter(files, '*.*'):
                filepath = os.path.join(dirpath, f)
                self.es_handle.insertItem(name=filepath, type='file', md5=md5(filepath))


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

    Filelist().filenames("C:\\")
    # config = configparser.ConfigParser()
    # config.readfp(open(os.path.dirname(__file__) + '/../config/mhprop.ini'))
    # paths = (config['DEFAULT']['file_watch_directories']).split(',')
    # file_updater = FileUpdater()
    # print "Initiating..."
    # file_updater.setObserver(paths)
