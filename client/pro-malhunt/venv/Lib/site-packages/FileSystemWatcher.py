"""FileSystemWatcher.py -- a ripoff of the .NET class of the same name.
Uses the Watcher class, built on top of ReadDirectoryChangesW for Win32.

See the following for more details:
http://msdn.microsoft.com/en-us/library/system.io.filesystemwatcher.aspx
"""

__version__ = "0.2.1"


try:
    from queue import Queue
except ImportError:
    from Queue import Queue

import os
import threading
import re

from watcher import _watcher


class _HandlerDict(dict):
    """An dictionary that functions like FileSystemWatcher `event`
       objects, e.g., FileSystemWatcher.Changed. They support += and -=
       operators to allow you attach and detach callbacks for the given
       events. This will store callable objects with their keys and values
       being the same."""
    def __iadd__(self, value):
        self.__setitem__(value, value)
        return self

    def __isub__(self, value):
        self.__delitem__(value)
        return self


# The following classes are passed as the argument to appropriate callbacks.
class FileSystemEventArgs(object):
    __slots__ = ("ChangeType", "FullPath", "Name")


# This should probably inherit from FileSystemEventArgs
class RenamedEventArgs(object):
    __slots__ =  ("ChangeType", "FullPath", "Name", "OldFullPath", "OldName")


"""
Some common scenarios and how they play out in terms of NotifyFilters (NF)
and WatcherChangesTypes (WCT).

Moving a file
    1. You'll get a WCT.Deleted update removing the original file name.
    2. You'll get a WCT.Created update creating the original file under
       the new name.
    3. You'll get a WCT.Modified update for the directory where the new
       file lives.
    4. You'll get a WCT.Modified update for the new file itself.

Deleting a directory
    1. You'll get a WCT.Deleted update for each file within the directory.
    2. You'll get a WCT.Deleted update for the directory itself.

Renaming a directory
    This is the exact same as renaming a file. You DO NOT get updates per-file.
"""

class NotifyFilters(object):
    FileName = _watcher.FILE_NOTIFY_CHANGE_FILE_NAME
    DirectoryName = _watcher.FILE_NOTIFY_CHANGE_DIR_NAME
    Attributes = _watcher.FILE_NOTIFY_CHANGE_ATTRIBUTES
    Size = _watcher.FILE_NOTIFY_CHANGE_SIZE
    LastWrite = _watcher.FILE_NOTIFY_CHANGE_LAST_WRITE
    LastAccess = _watcher.FILE_NOTIFY_CHANGE_LAST_ACCESS
    CreationTime = _watcher.FILE_NOTIFY_CHANGE_CREATION
    Security = _watcher.FILE_NOTIFY_CHANGE_SECURITY


class WatcherChangeTypes(object):
    Created = _watcher.FILE_ACTION_ADDED
    Deleted = _watcher.FILE_ACTION_REMOVED
    Changed = _watcher.FILE_ACTION_MODIFIED
    Renamed = (_watcher.FILE_ACTION_RENAMED_OLD_NAME |
               _watcher.FILE_ACTION_RENAMED_NEW_NAME)


class FileSystemWatcher(object):
    def __init__(self, directory, filter="*.*"):
        """path: The directory to monitor.
           filter: The type of files to watch.
        
        To monitor one specific file, specify `path` as the parent
        directory and `filter` as the exact file name."""
        if os.path.exists(directory) and os.path.isdir(directory):
            self._directory = directory
        else:
            raise ValueError("%s must be a directory" % directory)

        self._filter = filter
        self._watcher = _watcher.Watcher(self._directory, self._callback)

        # Events to be latched onto.
        self.Changed = _HandlerDict()
        self.Created = _HandlerDict()
        self.Deleted = _HandlerDict()
        self.Renamed = _HandlerDict()
        
        self._queue = Queue()
        self._callback_consumer = threading.Thread(
                                            target=self._handle_callbacks)
        # Set this as a daemon so it runs as long as _watcher is running.
        self._callback_consumer.setDaemon(True)
        self._callback_consumer.start()
        
        # Renaming fires off two events: one for what the old name was
        # and one for what the new name is. Since we only get one at a time,
        # store the last old name we get and pair it up with the next
        # new name we get. As far as I can see, this should work.
        self._old_name = None

    def _compile_filter(self, filter):
        # Convert commonly accepted filter formats into regex for matching.
        pattern = filter.replace(".", "\.").replace("*", "(.)+")
        return re.compile(pattern)

    @property
    def EnableRaisingEvents(self):
        return self._watcher.running

    @EnableRaisingEvents.setter
    def EnableRaisingEvents(self, enable):
        # TODO: Do some type of paramter validation that not only is flags
        # non-zero, but that it only contains flags that make sense.
        if enable and (self._watcher.flags is 0):
            raise AttributeError("NotifyFilter cannot be None")
        self._filter_regex = self._compile_filter(self._filter)
        self._watcher.start() if enable else self._watcher.stop()

    @property
    def IncludeSubdirectories(self):
        return self._watcher.recursive

    @IncludeSubdirectories.setter
    def IncludeSubdirectories(self, value):
        self._watcher.recursive = value

    # NOTE: NotifyFilter cannot be None. ReadDirectoryChangesW will return 0
    # and GetLastError will be 87, meaning "The parameter is incorrect".
    @property
    def NotifyFilter(self):
        return self._watcher.flags

    @NotifyFilter.setter
    def NotifyFilter(self, value):
        self._watcher.flags = value

    @property
    def Filter(self):
        return self._filter

    @Filter.setter
    def Filter(self, value):
        if not os.path.isdir(value):
            raise ValueError("%s must be a directory" % value)
        self._filter = value

    @property
    def Path(self):
        return self._directory

    @Path.setter
    def Path(self, value):
        self._directory = value

    def _callback(self, action, path):
        """Called from Watcher with an action value and relative path.
           If the updates become too frequent, which is often the case,
           this will become backed up and _watcher can't successfully call
           into here. For that reason, we put the update in a queue and get
           out of the way. See _handle_callbacks."""
        self._queue.put((action, path))
    
    def _handle_callbacks(self):
        while True:
            action, path = self._queue.get()
            
            # Should evalute this and see if it's safe to move inside
            # _callback. If we can skip out on queueing up useless updates,
            # we absolutely should.
            if not self._filter_regex.match(path):
                continue

            # There's no documentation stating what events should be let
            # through based on what filters, but this seems to be correct
            # based on usage of _watcher by itself.
            if (action == _watcher.FILE_ACTION_ADDED and
                (self.NotifyFilter & NotifyFilters.FileName or
                 self.NotifyFilter & NotifyFilters.DirectoryName)):
                callbacks = self.Created
            elif (action == _watcher.FILE_ACTION_REMOVED and
                  (self.NotifyFilter & NotifyFilters.FileName or
                   self.NotifyFilter & NotifyFilters.DirectoryName)):
                callbacks = self.Deleted
            elif (action == _watcher.FILE_ACTION_MODIFIED and
                  (self.NotifyFilter & NotifyFilters.Attributes or
                   self.NotifyFilter & NotifyFilters.Size or
                   self.NotifyFilter & NotifyFilters.LastWrite or
                   self.NotifyFilter & NotifyFilters.LastAccess or
                   self.NotifyFilter & NotifyFilters.CreationTime or
                   self.NotifyFilter & NotifyFilters.Security)):
                callbacks = self.Changed
            elif (action == _watcher.FILE_ACTION_RENAMED_OLD_NAME and
                  (self.NotifyFilter & NotifyFilters.FileName or
                   self.NotifyFilter & NotifyFilters.DirectoryName)):
                # Only store the old name and wait for the new one
                # to notify via callbacks.
                self._old_name = path
                continue
            elif (action == _watcher.FILE_ACTION_RENAMED_NEW_NAME and
                  (self.NotifyFilter & NotifyFilters.FileName or
                   self.NotifyFilter & NotifyFilters.DirectoryName)):
                callbacks = self.Renamed
            else:
                raise ValueError("Received unknown action")

            if callbacks != self.Renamed:
                update = FileSystemEventArgs()
            else:
                update = RenamedEventArgs()
                update.OldFullPath = os.path.join(self._directory,
                                                  self._old_name)
                update.OldName = os.path.basename(self._old_name)

            update.ChangeType = action
            update.FullPath = os.path.join(self._directory, path)
            update.Name = os.path.basename(path)

            for cb in callbacks.values():
                cb(update)

