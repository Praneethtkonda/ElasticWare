try:
    import unittest2 as unittest
except ImportError:
    import unittest

from .test_watcher import *
from .test_FileSystemWatcher import *

if __name__ == "__main__":
    unittest.main()

