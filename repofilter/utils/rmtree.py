import os
import shutil
import stat


def rmtree(path, ignore_errors=False, onerror=None):
    def removeReadOnly(func, path, excinfo):
        # Using os.chmod with stat.S_IWRITE to allow write permissions
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(path, ignore_errors, onerror or removeReadOnly)
