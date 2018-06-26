# See if we can use unittest2 first if we're on 3.1.
# 3.2 has the same features so we can fall back there.
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import os
import tempfile

import watcher

class TestWatcherInitialization(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def callback(self):
        pass

    @unittest.skip("")
    def test_bytes_path(self):
        # Eventually this will be supported.
        with self.assertRaises(TypeError):
            w = watcher.Watcher(os.getcwdb(), self.callback)

    def test_bad_callback(self):
        with self.assertRaises(TypeError):
            w = watcher.Watcher(self.dir, 12345)

    def test_no_args(self):
        w = watcher.Watcher(self.dir, self.callback)

    def test_args(self):
        w = watcher.Watcher(self.dir, self.callback, 1, 2, 3)

    def test_kwargs(self):
        w = watcher.Watcher(self.dir, self.callback, lol="rofl")


class TestAttributes(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.callback = lambda: 1
        self._watcher = watcher.Watcher(self.dir, self.callback)

    def test_flag(self):
        self._watcher.flags = watcher.FILE_NOTIFY_CHANGE_FILE_NAME
        self.assertEqual(self._watcher.flags,
                         watcher.FILE_NOTIFY_CHANGE_FILE_NAME)

    def test_multiple_flags(self):
        all_flags = (watcher.FILE_NOTIFY_CHANGE_FILE_NAME |
                     watcher.FILE_NOTIFY_CHANGE_DIR_NAME)
        
        self._watcher.flags = all_flags
        self.assertEqual(self._watcher.flags, all_flags)

    def test_recursive(self):
        self.assertFalse(self._watcher.recursive)
        self._watcher.recursive = True
        self.assertTrue(self._watcher.recursive)


if __name__ == "__main__":
    unittest.main()

