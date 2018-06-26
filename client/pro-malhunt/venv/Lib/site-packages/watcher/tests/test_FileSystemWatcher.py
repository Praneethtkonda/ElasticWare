# See if we can use unittest2 first if we're on 3.1.
# 3.2 has the same features so we can fall back there.
try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    import queue
except ImportError:
    import Queue as queue

import os
import tempfile
import shutil
import time

import FileSystemWatcher


class TestFSWInitialization(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_default(self):
        fsw = FileSystemWatcher.FileSystemWatcher(self.dir)
        self.assertEqual(fsw.Path, self.dir)
        self.assertEqual(fsw.Filter, "*.*")

    def test_bad_dir(self):
        # Hopefully "hurfdurf" doesn't exist...
        with self.assertRaises(ValueError):
            fsw = FileSystemWatcher.FileSystemWatcher("hurfdurf")

    def test_custom_filter(self):
        fsw = FileSystemWatcher.FileSystemWatcher(self.dir, "blarga.lol")
        self.assertEqual(fsw.Filter, "blarga.lol")

    def test_no_NotifyFilter(self):
        # ERE should raise AttributeError if we have no flags set.
        # If no flags get through, the underlying extension fails in a
        # separate thread and it's not easy to handle.
        fsw = FileSystemWatcher.FileSystemWatcher(self.dir)
        with self.assertRaises(AttributeError):
            fsw.EnableRaisingEvents = True

    def test_bad_NotifyFilter(self):
        fsw = FileSystemWatcher.FileSystemWatcher(self.dir)
        fsw.NotifyFilter = 123456789
        fsw.EnableRaisingEvents = True
        time.sleep(0.01)
        self.assertFalse(fsw.EnableRaisingEvents)


class TestBasics(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.fsw = FileSystemWatcher.FileSystemWatcher(self.dir)
 
        self.names = [os.path.join(self.dir, n) for n in ("hu.rf", "du.rf")]
        self._queue = queue.Queue()

    def tearDown(self):
        # Doesn't hurt to call this twice.
        self.fsw.EnableRaisingEvents = False
        shutil.rmtree(self.dir)

    def _callback(self, event):
        self._queue.put(event)

    def add_files(self):        
        for name in self.names:
            with open(name, "w") as file:
                pass

    def test_add_and_remove_files(self):
        self.fsw.NotifyFilter = FileSystemWatcher.NotifyFilters.FileName
        self.fsw.Created += self._callback
        self.fsw.Deleted += self._callback
        self.fsw.EnableRaisingEvents = True
        self.assertTrue(self.fsw.EnableRaisingEvents)

        self.add_files()
        for name in self.names:
            try:
                event = self._queue.get(timeout=1)
            except queue.Empty:
                self.fail("Unable to get event")

            self.assertEqual(event.ChangeType,
                             FileSystemWatcher.WatcherChangeTypes.Created)
            self.assertEqual(event.FullPath, os.path.join(self.dir, name))
            self.assertEqual(event.Name, os.path.basename(name))
            self._queue.task_done()

        for name in self.names:
            os.remove(name)
            try:
                event = self._queue.get(timeout=1)
            except queue.Empty:
                self.fail("Unable to get event")

            self.assertEqual(event.ChangeType,
                             FileSystemWatcher.WatcherChangeTypes.Deleted)
            self.assertEqual(event.FullPath, os.path.join(self.dir, name))
            self.assertEqual(event.Name, os.path.basename(name))
            self._queue.task_done()

    def test_modify_files(self):
        self.fsw.NotifyFilter = FileSystemWatcher.NotifyFilters.LastWrite
        self.fsw.Changed += self._callback
        self.fsw.EnableRaisingEvents = True
        self.assertTrue(self.fsw.EnableRaisingEvents)

        # Won't pick up events for the add.
        self.add_files()

        for name in self.names:
            with open(name, "a") as file:
                file.write("lol")
        
        for name in self.names:
            try:
                event = self._queue.get(timeout=1)
            except queue.Empty:
                self.fail("Unable to get event")

            self.assertEqual(event.ChangeType,
                             FileSystemWatcher.WatcherChangeTypes.Changed)
            self.assertEqual(event.FullPath, os.path.join(self.dir, name))
            self.assertEqual(event.Name, os.path.basename(name))
            self._queue.task_done()

    def test_rename_files(self):
        self.fsw.NotifyFilter = FileSystemWatcher.NotifyFilters.FileName
        self.fsw.Renamed += self._callback
        self.fsw.EnableRaisingEvents = True
        self.assertTrue(self.fsw.EnableRaisingEvents)

        # Won't pick up events for the add.
        self.add_files()
        
        new_name = "new.name"
        os.rename(self.names[0],
                  os.path.join(self.dir, new_name))

        try:
            event = self._queue.get(timeout=1)
        except queue.Empty:
            self.fail("Unable to get event")

        self.assertEqual(event.ChangeType,
                         FileSystemWatcher.WatcherChangeTypes.Renamed)
        self.assertEqual(event.FullPath, os.path.join(self.dir, new_name))
        self.assertEqual(event.Name, new_name)
        self.assertEqual(event.OldFullPath, self.names[0])
        self.assertEqual(event.OldName, os.path.basename(self.names[0]))
        self._queue.task_done()


class TestFilters(unittest.TestCase):
    pass


class TestRecursiveChanges(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
